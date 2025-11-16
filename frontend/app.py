import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Campaign Reporting Copilot",
    page_icon="📊",
    layout="wide"
)

# API endpoint
API_URL = "http://localhost:8000"

# Title and description
st.title("📊 Campaign Reporting Copilot")
st.markdown("**AI-powered campaign analysis with storytelling and actionable insights**")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Campaign CSV",
        type=["csv"],
        help="Upload your Meta/Google/GA4 campaign export"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df["week_start_date"] = pd.to_datetime(df["week_start_date"])
            
            st.success(f"✅ Loaded {len(df)} rows")
            
            # Date range selection
            min_date = df["week_start_date"].min().date()
            max_date = df["week_start_date"].max().date()
            
            st.subheader("📅 Period Selection")
            
            # Default to last 4 weeks
            default_start = max_date - timedelta(days=28)
            
            date_range = st.date_input(
                "Current Period",
                value=(default_start, max_date),
                min_value=min_date,
                max_value=max_date,
                help="Select the period you want to analyze"
            )
            
            # Comparison mode
            compare_mode = st.selectbox(
                "Comparison Mode",
                options=["WoW", "YoY"],
                help="WoW: Week over Week, YoY: Year over Year"
            )
            
            # Analyze button
            analyze_button = st.button("🚀 Analyze Campaigns", type="primary", use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            uploaded_file = None

# Main content area
if uploaded_file is None:
    # Welcome screen
    st.info("👈 Please upload a campaign CSV file to get started")
    
    st.markdown("### 📋 Expected CSV Format")
    st.markdown("""
    Your CSV should contain the following columns:
    - `week_start_date`: Week start date (YYYY-MM-DD)
    - `platform`: Meta, Google, YouTube, etc.
    - `campaign_name`: Campaign name
    - `impressions`, `clicks`, `cost`, `conversions`, `revenue`
    - Calculated metrics: `ctr`, `cpc`, `cpm`, `cvr`, `cpa`, `roas`
    """)
    
    st.markdown("### 🎯 What This Tool Does")
    st.markdown("""
    1. **Analyzes** your campaign data across periods (WoW/YoY)
    2. **Identifies** key trends and problem areas
    3. **Provides** actionable recommendations with priorities
    4. **Tells a story** in human-readable format
    """)

else:
    # Show data preview
    with st.expander("📊 Data Preview", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", len(df))
        with col2:
            st.metric("Platforms", df["platform"].nunique())
        with col3:
            st.metric("Campaigns", df["campaign_name"].nunique())
        with col4:
            st.metric("Date Range", f"{min_date} to {max_date}")
    
    # Analyze campaigns
    if analyze_button:
        if len(date_range) != 2:
            st.error("⚠️ Please select both start and end dates")
        else:
            current_start, current_end = date_range
            
            with st.spinner("🤖 AI is analyzing your campaigns..."):
                try:
                    # Prepare payload - convert timestamps to strings
                    df_copy = df.copy()
                    df_copy["week_start_date"] = df_copy["week_start_date"].dt.strftime("%Y-%m-%d")
                    
                    payload = {
                        "metrics": df_copy.to_dict(orient="records"),
                        "current_period": {
                            "start": str(current_start),
                            "end": str(current_end)
                        },
                        "compare_mode": compare_mode
                    }
                    
                    # Call API
                    response = requests.post(f"{API_URL}/analyze", json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Store in session state
                        st.session_state["analysis_result"] = data
                        st.session_state["analysis_period"] = f"{current_start} to {current_end}"
                        st.session_state["compare_mode"] = compare_mode
                        
                        st.success("✅ Analysis complete!")
                        st.rerun()
                        
                    else:
                        st.error(f"❌ API Error: {response.status_code} - {response.text}")
                        
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timed out. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Cannot connect to API. Make sure the backend is running on port 8000.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Display analysis results
    if "analysis_result" in st.session_state:
        data = st.session_state["analysis_result"]
        
        st.markdown("---")
        st.header("📈 Analysis Results")
        st.markdown(f"**Period:** {st.session_state['analysis_period']} | **Mode:** {st.session_state['compare_mode']}")
        
        # Summary section
        st.subheader("📝 Executive Summary")
        summary_container = st.container()
        with summary_container:
            for item in data.get("summary", []):
                st.markdown(f"• {item['text']}")
        
        st.markdown("---")
        
        # Two columns layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("⚠️ Problem Areas")
            if data.get("problem_areas"):
                for item in data["problem_areas"]:
                    st.warning(f"🔴 {item['text']}")
            else:
                st.success("✅ No major problems detected!")
        
        with col2:
            st.subheader("🎯 Next Best Actions")
            actions = data.get("next_best_actions", [])
            
            if actions:
                # Sort by priority
                priority_order = {"high": 0, "medium": 1, "low": 2}
                sorted_actions = sorted(actions, key=lambda x: priority_order.get(x["priority"].lower(), 3))
                
                for action in sorted_actions:
                    priority = action["priority"].upper()
                    
                    # Priority badge color
                    if priority == "HIGH":
                        badge = "🔴 HIGH"
                        color = "#ff4b4b"
                    elif priority == "MEDIUM":
                        badge = "🟡 MEDIUM"
                        color = "#ffa500"
                    else:
                        badge = "🟢 LOW"
                        color = "#00cc00"
                    
                    st.markdown(
                        f"""
                        <div style="padding: 15px; border-left: 4px solid {color}; background-color: #f0f2f6; margin-bottom: 10px; border-radius: 5px;">
                            <strong style="color: {color};">{badge}</strong> | <strong>{action['area']}</strong><br/>
                            <span style="color: #31333F;">{action['description']}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("No specific actions recommended at this time.")
        
        st.markdown("---")
        
        # Data visualization section
        st.subheader("📊 Campaign Performance Overview")
        
        # Filter data for selected period
        current_start, current_end = date_range
        period_df = df[
            (df["week_start_date"] >= pd.to_datetime(current_start)) &
            (df["week_start_date"] <= pd.to_datetime(current_end))
        ]
        
        if not period_df.empty:
            # Aggregate by campaign
            campaign_summary = period_df.groupby(["campaign_name", "platform"]).agg({
                "cost": "sum",
                "revenue": "sum",
                "conversions": "sum",
                "impressions": "sum",
                "clicks": "sum"
            }).reset_index()
            
            campaign_summary["roas"] = campaign_summary["revenue"] / campaign_summary["cost"]
            campaign_summary["ctr"] = campaign_summary["clicks"] / campaign_summary["impressions"]
            campaign_summary["cvr"] = campaign_summary["conversions"] / campaign_summary["clicks"]
            campaign_summary["cpa"] = campaign_summary["cost"] / campaign_summary["conversions"]
            
            # Create tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["💰 Cost & Revenue", "📈 ROAS Performance", "🎯 Efficiency Metrics", "📊 Data Table"])
            
            with tab1:
                # Dual axis chart for Cost vs Revenue (different scales)
                fig = go.Figure()
                
                # Add Cost bars on primary y-axis
                fig.add_trace(go.Bar(
                    name="Cost",
                    x=campaign_summary["campaign_name"],
                    y=campaign_summary["cost"],
                    marker_color="#ff4b4b",
                    yaxis="y",
                    text=campaign_summary["cost"].apply(lambda x: f"₺{x:,.0f}"),
                    textposition="outside"
                ))
                
                # Add Revenue bars on secondary y-axis
                fig.add_trace(go.Bar(
                    name="Revenue",
                    x=campaign_summary["campaign_name"],
                    y=campaign_summary["revenue"],
                    marker_color="#00cc00",
                    yaxis="y2",
                    text=campaign_summary["revenue"].apply(lambda x: f"₺{x:,.0f}"),
                    textposition="outside"
                ))
                
                fig.update_layout(
                    title="Cost vs Revenue by Campaign (Dual Scale)",
                    xaxis_title="Campaign",
                    yaxis=dict(
                        title=dict(text="Cost (TL)", font=dict(color="#ff4b4b")),
                        tickfont=dict(color="#ff4b4b"),
                        side="left"
                    ),
                    yaxis2=dict(
                        title=dict(text="Revenue (TL)", font=dict(color="#00cc00")),
                        tickfont=dict(color="#00cc00"),
                        overlaying="y",
                        side="right"
                    ),
                    barmode="group",
                    height=500,
                    hovermode="x unified",
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Add ROAS as efficiency indicator
                col1, col2, col3 = st.columns(3)
                with col1:
                    total_cost = campaign_summary["cost"].sum()
                    st.metric("Total Cost", f"₺{total_cost:,.2f}")
                with col2:
                    total_revenue = campaign_summary["revenue"].sum()
                    st.metric("Total Revenue", f"₺{total_revenue:,.2f}")
                with col3:
                    overall_roas = total_revenue / total_cost if total_cost > 0 else 0
                    st.metric("Overall ROAS", f"{overall_roas:.2f}x")
            
            with tab2:
                # ROAS with benchmark line
                fig = go.Figure()
                
                # Sort by ROAS
                roas_sorted = campaign_summary.sort_values("roas", ascending=True)
                
                # Color based on ROAS threshold
                colors = roas_sorted["roas"].apply(
                    lambda x: "#00cc00" if x >= 3 else "#ffa500" if x >= 1 else "#ff4b4b"
                )
                
                fig.add_trace(go.Bar(
                    x=roas_sorted["roas"],
                    y=roas_sorted["campaign_name"],
                    orientation="h",
                    marker_color=colors,
                    text=roas_sorted["roas"].apply(lambda x: f"{x:.2f}x"),
                    textposition="outside",
                    customdata=roas_sorted[["platform", "cost", "revenue"]],
                    hovertemplate="<b>%{y}</b><br>" +
                                  "ROAS: %{x:.2f}x<br>" +
                                  "Platform: %{customdata[0]}<br>" +
                                  "Cost: ₺%{customdata[1]:,.0f}<br>" +
                                  "Revenue: ₺%{customdata[2]:,.0f}<br>" +
                                  "<extra></extra>"
                ))
                
                # Add benchmark line at ROAS = 1
                fig.add_vline(x=1, line_dash="dash", line_color="gray", 
                             annotation_text="Break-even", annotation_position="top")
                
                fig.update_layout(
                    title="ROAS by Campaign (Return on Ad Spend)",
                    xaxis_title="ROAS (Revenue / Cost)",
                    yaxis_title="",
                    height=max(400, len(campaign_summary) * 40),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # ROAS legend
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("🟢 **Excellent** (ROAS ≥ 3.0)")
                with col2:
                    st.markdown("🟡 **Good** (1.0 ≤ ROAS < 3.0)")
                with col3:
                    st.markdown("🔴 **Poor** (ROAS < 1.0)")
            
            with tab3:
                # Multi-metric comparison
                col1, col2 = st.columns(2)
                
                with col1:
                    # CTR by Campaign
                    fig_ctr = go.Figure()
                    ctr_sorted = campaign_summary.sort_values("ctr", ascending=True)
                    
                    fig_ctr.add_trace(go.Bar(
                        x=ctr_sorted["ctr"] * 100,
                        y=ctr_sorted["campaign_name"],
                        orientation="h",
                        marker_color="#1f77b4",
                        text=ctr_sorted["ctr"].apply(lambda x: f"{x*100:.2f}%"),
                        textposition="outside"
                    ))
                    
                    fig_ctr.update_layout(
                        title="Click-Through Rate (CTR)",
                        xaxis_title="CTR (%)",
                        yaxis_title="",
                        height=400,
                        showlegend=False
                    )
                    st.plotly_chart(fig_ctr, use_container_width=True)
                
                with col2:
                    # CPA by Campaign
                    fig_cpa = go.Figure()
                    cpa_sorted = campaign_summary.sort_values("cpa", ascending=True)
                    
                    fig_cpa.add_trace(go.Bar(
                        x=cpa_sorted["cpa"],
                        y=cpa_sorted["campaign_name"],
                        orientation="h",
                        marker_color="#ff7f0e",
                        text=cpa_sorted["cpa"].apply(lambda x: f"₺{x:.2f}"),
                        textposition="outside"
                    ))
                    
                    fig_cpa.update_layout(
                        title="Cost per Acquisition (CPA)",
                        xaxis_title="CPA (TL)",
                        yaxis_title="",
                        height=400,
                        showlegend=False
                    )
                    st.plotly_chart(fig_cpa, use_container_width=True)
                
                # CVR by Campaign
                fig_cvr = go.Figure()
                cvr_sorted = campaign_summary.sort_values("cvr", ascending=False)
                
                fig_cvr.add_trace(go.Bar(
                    x=cvr_sorted["campaign_name"],
                    y=cvr_sorted["cvr"] * 100,
                    marker_color="#2ca02c",
                    text=cvr_sorted["cvr"].apply(lambda x: f"{x*100:.2f}%"),
                    textposition="outside"
                ))
                
                fig_cvr.update_layout(
                    title="Conversion Rate (CVR) by Campaign",
                    xaxis_title="Campaign",
                    yaxis_title="CVR (%)",
                    height=400,
                    showlegend=False
                )
                st.plotly_chart(fig_cvr, use_container_width=True)
            
            with tab4:
                # Enhanced metrics table with color formatting
                st.dataframe(
                    campaign_summary[["campaign_name", "platform", "cost", "revenue", "conversions", 
                                     "roas", "ctr", "cvr", "cpa"]].style.format({
                        "cost": "₺{:,.2f}",
                        "revenue": "₺{:,.2f}",
                        "roas": "{:.2f}x",
                        "ctr": "{:.2%}",
                        "cvr": "{:.2%}",
                        "cpa": "₺{:.2f}",
                        "conversions": "{:.0f}"
                    }).background_gradient(subset=["roas"], cmap="RdYlGn", vmin=0, vmax=5),
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #888;">
        <small>Campaign Reporting Copilot | Powered by AI</small>
    </div>
    """,
    unsafe_allow_html=True
)

