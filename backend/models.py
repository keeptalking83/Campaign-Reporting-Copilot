from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime


class CampaignMetric(BaseModel):
    """Individual campaign metric data point"""
    week_start_date: str
    year_week: str
    platform: str
    channel: str
    country: str
    campaign_name: str
    objective: str
    impressions: float
    clicks: float
    cost: float
    conversions: float
    revenue: float
    ctr: float = 0
    cpc: float = 0
    cpm: float = 0
    cvr: float = 0
    cpa: float = 0
    roas: float = 0


class AnalyzeRequest(BaseModel):
    """Request model for campaign analysis"""
    metrics: List[CampaignMetric]
    current_period: Dict[str, str] = Field(
        ...,
        description="Current period dates with 'start' and 'end' keys in YYYY-MM-DD format"
    )
    compare_mode: str = Field(
        default="WoW",
        description="Comparison mode: 'WoW' (Week over Week) or 'YoY' (Year over Year)"
    )


class BulletPoint(BaseModel):
    """Single bullet point for summary or problem areas"""
    text: str


class ActionItem(BaseModel):
    """Action item with priority"""
    area: str = Field(..., description="Campaign or channel name")
    description: str = Field(..., description="Specific actionable recommendation")
    priority: str = Field(..., description="Priority level: high, medium, or low")


class AnalysisResponse(BaseModel):
    """Response model containing analysis results"""
    summary: List[BulletPoint]
    problem_areas: List[BulletPoint]
    next_best_actions: List[ActionItem]

