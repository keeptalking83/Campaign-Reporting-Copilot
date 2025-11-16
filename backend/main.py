from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional
import os
from openai import OpenAI

from models import AnalyzeRequest, AnalysisResponse, BulletPoint, ActionItem

app = FastAPI(title="Campaign Reporting Copilot API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def calculate_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate derived metrics from raw data"""
    df = df.copy()
    
    # Avoid division by zero
    df["ctr"] = df.apply(lambda x: x["clicks"] / x["impressions"] if x["impressions"] > 0 else 0, axis=1)
    df["cpc"] = df.apply(lambda x: x["cost"] / x["clicks"] if x["clicks"] > 0 else 0, axis=1)
    df["cpm"] = df.apply(lambda x: (x["cost"] * 1000) / x["impressions"] if x["impressions"] > 0 else 0, axis=1)
    df["cvr"] = df.apply(lambda x: x["conversions"] / x["clicks"] if x["clicks"] > 0 else 0, axis=1)
    df["cpa"] = df.apply(lambda x: x["cost"] / x["conversions"] if x["conversions"] > 0 else 0, axis=1)
    df["roas"] = df.apply(lambda x: x["revenue"] / x["cost"] if x["cost"] > 0 else 0, axis=1)
    
    return df


def get_previous_period_dates(start_date: datetime, end_date: datetime, mode: str):
    """Calculate previous period dates based on comparison mode"""
    delta = end_date - start_date
    
    if mode == "WoW":
        # Week over week
        prev_end = start_date - timedelta(days=1)
        prev_start = prev_end - delta
    elif mode == "YoY":
        # Year over year
        prev_start = start_date - timedelta(days=365)
        prev_end = end_date - timedelta(days=365)
    else:
        raise ValueError(f"Invalid comparison mode: {mode}")
    
    return prev_start, prev_end


def aggregate_period_data(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Filter and aggregate data for a specific period"""
    # Filter by date range
    period_df = df[
        (df["week_start_date"] >= start_date) & 
        (df["week_start_date"] <= end_date)
    ].copy()
    
    if period_df.empty:
        return pd.DataFrame()
    
    # Aggregate by campaign
    group_cols = ["campaign_name", "platform"]
    
    agg_df = period_df.groupby(group_cols).agg({
        "impressions": "sum",
        "clicks": "sum",
        "cost": "sum",
        "conversions": "sum",
        "revenue": "sum"
    }).reset_index()
    
    # Recalculate derived metrics
    agg_df = calculate_derived_metrics(agg_df)
    
    return agg_df


def compare_periods(current_df: pd.DataFrame, previous_df: pd.DataFrame) -> pd.DataFrame:
    """Compare current and previous period metrics"""
    if previous_df.empty:
        # No previous data to compare
        compare_df = current_df.copy()
        compare_df["cost_change_pct"] = 0
        compare_df["revenue_change_pct"] = 0
        compare_df["roas_change_pct"] = 0
        compare_df["conversions_change_pct"] = 0
        return compare_df
    
    # Merge dataframes
    compare_df = current_df.merge(
        previous_df,
        on=["campaign_name", "platform"],
        suffixes=("_cur", "_prev"),
        how="left"
    )
    
    # Calculate percentage changes
    compare_df["cost_change_pct"] = compare_df.apply(
        lambda x: ((x["cost_cur"] - x["cost_prev"]) / x["cost_prev"] * 100) 
        if pd.notna(x["cost_prev"]) and x["cost_prev"] > 0 else 0,
        axis=1
    )
    
    compare_df["revenue_change_pct"] = compare_df.apply(
        lambda x: ((x["revenue_cur"] - x["revenue_prev"]) / x["revenue_prev"] * 100)
        if pd.notna(x["revenue_prev"]) and x["revenue_prev"] > 0 else 0,
        axis=1
    )
    
    compare_df["roas_change_pct"] = compare_df.apply(
        lambda x: ((x["roas_cur"] - x["roas_prev"]) / x["roas_prev"] * 100)
        if pd.notna(x["roas_prev"]) and x["roas_prev"] > 0 else 0,
        axis=1
    )
    
    compare_df["conversions_change_pct"] = compare_df.apply(
        lambda x: ((x["conversions_cur"] - x["conversions_prev"]) / x["conversions_prev"] * 100)
        if pd.notna(x["conversions_prev"]) and x["conversions_prev"] > 0 else 0,
        axis=1
    )
    
    return compare_df


def extract_insights(compare_df: pd.DataFrame) -> dict:
    """Extract key insights from comparison data"""
    insights = {
        "top_spenders": [],
        "top_roas": [],
        "red_flags": [],
        "funnel_issues": []
    }
    
    if compare_df.empty:
        return insights
    
    # Top 3 spenders
    top_cost = compare_df.nlargest(3, "cost_cur")
    insights["top_spenders"] = [
        {
            "campaign": row["campaign_name"],
            "platform": row["platform"],
            "cost": row["cost_cur"],
            "roas": row["roas_cur"]
        }
        for _, row in top_cost.iterrows()
    ]
    
    # Top 3 ROAS performers
    top_roas = compare_df.nlargest(3, "roas_cur")
    insights["top_roas"] = [
        {
            "campaign": row["campaign_name"],
            "platform": row["platform"],
            "roas": row["roas_cur"],
            "revenue": row["revenue_cur"]
        }
        for _, row in top_roas.iterrows()
    ]
    
    # Red flags: ROAS decreasing but cost increasing
    red_flags = compare_df[
        (compare_df["roas_change_pct"] < -10) & 
        (compare_df["cost_change_pct"] > 10)
    ]
    insights["red_flags"] = [
        {
            "campaign": row["campaign_name"],
            "platform": row["platform"],
            "roas_change": row["roas_change_pct"],
            "cost_change": row["cost_change_pct"],
            "current_roas": row["roas_cur"]
        }
        for _, row in red_flags.iterrows()
    ]
    
    # Funnel issues: High CTR but low CVR
    funnel_issues = compare_df[
        (compare_df["ctr_cur"] > 0.02) & 
        (compare_df["cvr_cur"] < 0.03)
    ]
    insights["funnel_issues"] = [
        {
            "campaign": row["campaign_name"],
            "platform": row["platform"],
            "ctr": row["ctr_cur"],
            "cvr": row["cvr_cur"]
        }
        for _, row in funnel_issues.iterrows()
    ]
    
    return insights


def generate_llm_prompt(compare_df: pd.DataFrame, insights: dict, compare_mode: str) -> str:
    """Generate prompt for LLM analysis"""
    
    # Overall metrics
    total_cost_cur = compare_df["cost_cur"].sum()
    total_revenue_cur = compare_df["revenue_cur"].sum()
    total_conversions_cur = compare_df["conversions_cur"].sum()
    overall_roas = total_revenue_cur / total_cost_cur if total_cost_cur > 0 else 0
    
    # Calculate changes if previous data exists
    if "cost_prev" in compare_df.columns:
        total_cost_prev = compare_df["cost_prev"].sum()
        total_revenue_prev = compare_df["revenue_prev"].sum()
        cost_change = ((total_cost_cur - total_cost_prev) / total_cost_prev * 100) if total_cost_prev > 0 else 0
        revenue_change = ((total_revenue_cur - total_revenue_prev) / total_revenue_prev * 100) if total_revenue_prev > 0 else 0
    else:
        cost_change = 0
        revenue_change = 0
    
    prompt = f"""You are a digital marketing analyst expert. Analyze the following campaign performance data and provide insights in a structured format.

**Comparison Mode:** {compare_mode}

**Overall Performance:**
- Total Cost: {total_cost_cur:.2f} TL (Change: {cost_change:+.1f}%)
- Total Revenue: {total_revenue_cur:.2f} TL (Change: {revenue_change:+.1f}%)
- Total Conversions: {total_conversions_cur:.0f}
- Overall ROAS: {overall_roas:.2f}

**Top Spenders:**
"""
    
    for spender in insights["top_spenders"]:
        prompt += f"- {spender['campaign']} ({spender['platform']}): {spender['cost']:.2f} TL, ROAS: {spender['roas']:.2f}\n"
    
    prompt += "\n**Top ROAS Performers:**\n"
    for performer in insights["top_roas"]:
        prompt += f"- {performer['campaign']} ({performer['platform']}): ROAS {performer['roas']:.2f}, Revenue: {performer['revenue']:.2f} TL\n"
    
    if insights["red_flags"]:
        prompt += "\n**Red Flags (ROAS declining, cost increasing):**\n"
        for flag in insights["red_flags"]:
            prompt += f"- {flag['campaign']} ({flag['platform']}): ROAS {flag['roas_change']:+.1f}%, Cost {flag['cost_change']:+.1f}%, Current ROAS: {flag['current_roas']:.2f}\n"
    
    if insights["funnel_issues"]:
        prompt += "\n**Potential Funnel Issues (High CTR, Low CVR):**\n"
        for issue in insights["funnel_issues"]:
            prompt += f"- {issue['campaign']} ({issue['platform']}): CTR {issue['ctr']:.2%}, CVR {issue['cvr']:.2%}\n"
    
    prompt += """

Please provide your analysis in the following JSON format:
{
  "summary": [
    {"text": "Summary point 1"},
    {"text": "Summary point 2"},
    {"text": "Summary point 3"}
  ],
  "problem_areas": [
    {"text": "Problem area description"}
  ],
  "next_best_actions": [
    {
      "area": "Campaign/Channel name",
      "description": "Specific actionable recommendation",
      "priority": "high|medium|low"
    }
  ]
}

Requirements:
- Write 3-5 bullet points for summary
- Identify key problem areas
- Provide specific, actionable recommendations with priority levels
- Focus on what the marketer should DO next
- Be concise and direct

Return ONLY the JSON, no additional text.
"""
    
    return prompt


async def call_llm_analysis(prompt: str) -> dict:
    """Call OpenAI API for analysis"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a digital marketing analytics expert. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM API error: {str(e)}")


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_campaigns(request: AnalyzeRequest):
    """Main endpoint to analyze campaign data"""
    try:
        # Convert metrics to DataFrame
        df = pd.DataFrame([metric.model_dump() for metric in request.metrics])
        
        # Convert date strings to datetime
        df["week_start_date"] = pd.to_datetime(df["week_start_date"])
        
        # Parse period dates
        current_start = datetime.strptime(request.current_period["start"], "%Y-%m-%d")
        current_end = datetime.strptime(request.current_period["end"], "%Y-%m-%d")
        
        # Get current period data
        current_df = aggregate_period_data(df, current_start, current_end)
        
        if current_df.empty:
            raise HTTPException(status_code=400, detail="No data found for the current period")
        
        # Get previous period data
        prev_start, prev_end = get_previous_period_dates(current_start, current_end, request.compare_mode)
        previous_df = aggregate_period_data(df, prev_start, prev_end)
        
        # Compare periods
        compare_df = compare_periods(current_df, previous_df)
        
        # Extract insights
        insights = extract_insights(compare_df)
        
        # Generate LLM prompt
        prompt = generate_llm_prompt(compare_df, insights, request.compare_mode)
        
        # Call LLM
        llm_response = await call_llm_analysis(prompt)
        
        # Parse and validate response
        analysis_response = AnalysisResponse(
            summary=[BulletPoint(**item) for item in llm_response.get("summary", [])],
            problem_areas=[BulletPoint(**item) for item in llm_response.get("problem_areas", [])],
            next_best_actions=[ActionItem(**item) for item in llm_response.get("next_best_actions", [])]
        )
        
        return analysis_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

