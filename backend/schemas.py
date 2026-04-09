"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class QueryRequest(BaseModel):
    """Query request model"""
    query: str


class UploadResponse(BaseModel):
    """Upload response model"""
    message: str
    columns: List[str]
    rows: int
    file_id: str


class PreviewResponse(BaseModel):
    """Preview response model"""
    data: List[Dict[str, Any]]
    rows: int


class DatasetInfoResponse(BaseModel):
    """Dataset info response model"""
    columns: List[str]
    shape: tuple
    missing_values: Dict[str, int]
    numeric_columns: List[str]
    categorical_columns: List[str]


class QueryResponse(BaseModel):
    """Generic query response model"""
    status: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    message: Optional[str] = None


class ChartResponse(BaseModel):
    """Chart response model"""
    status: str
    chart_path: str
    insight: str
    chart_type: str
