"""
Utility functions for data analysis and column matching
"""
import difflib
from typing import List, Optional, Tuple
import pandas as pd
import numpy as np


# Configuration
FUZZY_MATCH_THRESHOLD = 0.6


def fuzzy_match_column(query: str, columns: List[str]) -> Optional[str]:
    """
    Find the best matching column using fuzzy string matching.
    
    Args:
        query: User query string
        columns: List of available columns
        
    Returns:
        Best matching column name or None
    """
    if not columns:
        return None
    
    # Try exact case-insensitive match first
    query_lower = query.lower()
    for col in columns:
        if col.lower() == query_lower:
            return col
    
    # Use difflib for fuzzy matching
    matches = difflib.get_close_matches(
        query_lower, 
        [col.lower() for col in columns], 
        n=1, 
        cutoff=FUZZY_MATCH_THRESHOLD
    )
    
    if matches:
        # Find original column name (preserves case)
        matched_col_lower = matches[0]
        for col in columns:
            if col.lower() == matched_col_lower:
                return col
    
    return None


def extract_columns_from_query(query: str, columns: List[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract X and Y column references from a query using fuzzy matching.
    
    Returns:
        Tuple of (x_column, y_column) or (x_column, None)
    """
    x_col = None
    y_col = None
    
    # Split query by common separators
    words = query.lower().split()
    
    # Look for columns in the query
    for word in words:
        matched_col = fuzzy_match_column(word, columns)
        if matched_col:
            if x_col is None:
                x_col = matched_col
            elif y_col is None and matched_col != x_col:
                y_col = matched_col
    
    return (x_col, y_col)


def get_numeric_and_categorical_columns(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    Detect numeric and categorical columns in dataframe.
    
    Returns:
        Tuple of (numeric_columns, categorical_columns)
    """
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()
    
    return (numeric_cols, categorical_cols)


def detect_query_intent(query: str) -> str:
    """
    Detect the intent of a query using intelligent natural language understanding.
    
    Returns:
        One of: 'cleaning', 'statistics', 'visualization', 'analysis', 'unknown'
    """
    query_lower = query.lower()
    
    # Cleaning intents - highest priority
    if any(word in query_lower for word in ['remove', 'delete', 'drop', 'clean', 'duplicate', 'missing']):
        return 'cleaning'
    
    # Statistics intents (count/aggregate operations)
    if any(word in query_lower for word in ['min', 'max', 'mean', 'average', 'sum', 'median', 'std', 'standard deviation', 'summary', 'statistics', 'count', 'total', 'how many', 'number of', 'unique', 'distinct']):
        return 'statistics'
    
    # Visualization intents - expanded list for natural language
    visualization_keywords = [
        'plot', 'chart', 'graph', 'visualize', 'visualization',
        'histogram', 'scatter', 'bar', 'pie', 'line', 'area', 'box', 'violin', 'heatmap',
        'show', 'display', 'represent', 'see', 'view', 'picture',
        'trend', 'distribution', 'comparison', 'breakdown', 'correlation', 'relationship',
        'pattern', 'analyze visually', 'visual', 'diagram',
        'versus', 'vs', 'over time', 'by', 'across'
    ]
    
    if any(word in query_lower for word in visualization_keywords):
        return 'visualization'
    
    # Check for visualization-like intent even without explicit keywords
    # If query mentions multiple words that could be columns or analysis type
    viz_hint_words = ['how', 'what', 'analyze', 'compare', 'look at', 'examine', 'observe']
    analysis_words = ['data', 'distribution', 'pattern', 'trend', 'relationship']
    
    if any(hint in query_lower for hint in viz_hint_words) and any(analysis in query_lower for analysis in analysis_words):
        return 'visualization'
    
    # Default to general analysis
    return 'analysis'


def validate_column_exists(column: str, columns: List[str]) -> bool:
    """Check if a column exists (case-insensitive)"""
    column_lower = column.lower()
    return any(col.lower() == column_lower for col in columns)


def get_column_by_name(column: str, columns: List[str]) -> Optional[str]:
    """Get actual column name (preserves case)"""
    column_lower = column.lower()
    for col in columns:
        if col.lower() == column_lower:
            return col
    return None
