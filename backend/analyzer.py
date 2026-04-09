"""
Core data analysis engine
"""
import os
import uuid
import pandas as pd
import numpy as np
import plotly.express as px
from typing import Dict, Any, List, Optional
from langchain_ollama import OllamaLLM


def convert_to_serializable(obj: Any) -> Any:
    """Convert numpy types to Python native types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj  # Return dataframe as-is
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) if k != 'data' else v for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    return obj
from utils import (
    extract_columns_from_query,
    get_numeric_and_categorical_columns,
    fuzzy_match_column
)


class DataAnalyzer:
    """Core data analysis engine"""
    
    def __init__(self):
        """Initialize the analyzer"""
        self.llm = None
        self.llm_available = False
        
        try:
            self.llm = OllamaLLM(model="mistral")
            self.llm_available = True
            print("✅ LLM initialized successfully")
        except Exception as e:
            print(f"⚠️ LLM initialization failed: {e}")
            print("⚠️ System will work without AI insights")
            self.llm_available = False
        
        self.chart_dir = "charts"
        os.makedirs(self.chart_dir, exist_ok=True)
    
    # ========== DATA CLEANING ==========
    
    def clean_missing_values(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Remove missing values from dataset"""
        try:
            before_rows = len(df)
            df_cleaned = df.dropna()
            after_rows = len(df_cleaned)
            
            return {
                "status": "success",
                "message": "Missing values removed",
                "rows_before": before_rows,
                "rows_after": after_rows,
                "rows_removed": before_rows - after_rows,
                "data": df_cleaned
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error removing missing values: {str(e)}"
            }
    
    def clean_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Remove duplicate rows from dataset"""
        try:
            before_rows = len(df)
            df_cleaned = df.drop_duplicates()
            after_rows = len(df_cleaned)
            
            return {
                "status": "success",
                "message": "Duplicates removed",
                "rows_before": before_rows,
                "rows_after": after_rows,
                "rows_removed": before_rows - after_rows,
                "data": df_cleaned
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error removing duplicates: {str(e)}"
            }
    
    # ========== STATISTICAL ANALYSIS ==========
    
    def analyze_statistics(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Perform statistical analysis based on query"""
        try:
            numeric_cols, _ = get_numeric_and_categorical_columns(df)
            
            query_lower = query.lower()
            
            # ===== COUNT/TOTAL OPERATIONS =====
            if any(word in query_lower for word in ["count", "total", "how many", "number of"]):
                results = {
                    "total_rows": len(df),
                    "total_columns": len(df.columns),
                    "column_names": df.columns.tolist()
                }
                
                # Check for specific column count (e.g., "count passengers", "total rows")
                for col in df.columns:
                    if col.lower() in query_lower or col.lower() in query_lower.replace(" ", "_"):
                        results[f"{col}_count"] = int(df[col].count())
                        results[f"{col}_non_null"] = int(df[col].notna().sum())
                        results[f"{col}_null"] = int(df[col].isna().sum())
                
                return {
                    "status": "success",
                    "message": "Count analysis completed",
                    "data": results
                }
            
            # ===== UNIQUE/DISTINCT OPERATIONS =====
            if any(word in query_lower for word in ["unique", "distinct"]):
                results = {}
                for col in df.columns:
                    if col.lower() in query_lower or col.lower() in query_lower.replace(" ", "_"):
                        results[f"{col}_unique_count"] = int(df[col].nunique())
                        results[f"{col}_unique_values"] = df[col].dropna().unique().tolist()[:10]
                
                return {
                    "status": "success",
                    "message": "Unique value analysis completed",
                    "data": results
                }
            
            if not numeric_cols:
                return {
                    "status": "error",
                    "error": "No numeric columns available for statistics"
                }
            
            # Try to extract column from query
            selected_col = fuzzy_match_column(query, numeric_cols)
            
            # If no column found, use first numeric column
            if not selected_col:
                selected_col = numeric_cols[0]
            
            # Full summary
            if "summary" in query_lower:
                return {
                    "status": "success",
                    "data": df[numeric_cols].describe().to_dict(),
                    "message": "Summary statistics generated"
                }
            
            # Min value
            if any(word in query_lower for word in ["min", "minimum"]):
                return {
                    "status": "success",
                    "data": {f"Minimum {selected_col}": float(df[selected_col].min())},
                    "message": f"Minimum value calculated for {selected_col}"
                }
            
            # Max value
            if any(word in query_lower for word in ["max", "maximum"]):
                return {
                    "status": "success",
                    "data": {f"Maximum {selected_col}": float(df[selected_col].max())},
                    "message": f"Maximum value calculated for {selected_col}"
                }
            
            # Mean
            if any(word in query_lower for word in ["mean", "average"]):
                return {
                    "status": "success",
                    "data": {f"Mean {selected_col}": float(df[selected_col].mean())},
                    "message": f"Mean calculated for {selected_col}"
                }
            
            # Sum
            if "sum" in query_lower:
                return {
                    "status": "success",
                    "data": {f"Sum {selected_col}": float(df[selected_col].sum())},
                    "message": f"Sum calculated for {selected_col}"
                }
            
            # Median
            if "median" in query_lower:
                return {
                    "status": "success",
                    "data": {f"Median {selected_col}": float(df[selected_col].median())},
                    "message": f"Median calculated for {selected_col}"
                }
            
            # Standard Deviation
            if any(word in query_lower for word in ["std", "standard deviation"]):
                return {
                    "status": "success",
                    "data": {f"Standard Deviation {selected_col}": float(df[selected_col].std())},
                    "message": f"Standard deviation calculated for {selected_col}"
                }
            
            # Default: return all stats for the column
            return {
                "status": "success",
                "data": df[[selected_col]].describe().to_dict(),
                "message": f"Statistics for {selected_col}"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error performing statistical analysis: {str(e)}"
            }
    
    # ========== STUDENT/RECORD ANALYSIS ==========
    
    def find_max_student(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Find the student/record with maximum value in a numeric column"""
        try:
            numeric_cols, _ = get_numeric_and_categorical_columns(df)
            
            if not numeric_cols:
                return {
                    "status": "error",
                    "error": "No numeric columns available"
                }
            
            query_lower = query.lower()
            
            # Extract which column to find max for
            selected_col = fuzzy_match_column(query, numeric_cols)
            if not selected_col:
                selected_col = numeric_cols[0]
            
            # Find row with maximum value
            max_idx = df[selected_col].idxmax()
            max_row = df.loc[max_idx].to_dict()
            max_value = df.loc[max_idx, selected_col]
            
            # Convert numpy types to Python native types
            max_row = convert_to_serializable(max_row)
            max_value = convert_to_serializable(max_value)
            
            return {
                "status": "success",
                "data": {
                    "max_record": max_row,
                    "max_column": selected_col,
                    "max_value": max_value
                },
                "message": f"Student/Record with maximum {selected_col}: {max_value}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error finding maximum student: {str(e)}"
            }
    
    def find_min_student(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Find the student/record with minimum value in a numeric column"""
        try:
            numeric_cols, _ = get_numeric_and_categorical_columns(df)
            
            if not numeric_cols:
                return {
                    "status": "error",
                    "error": "No numeric columns available"
                }
            
            query_lower = query.lower()
            
            # Extract which column to find min for
            selected_col = fuzzy_match_column(query, numeric_cols)
            if not selected_col:
                selected_col = numeric_cols[0]
            
            # Find row with minimum value
            min_idx = df[selected_col].idxmin()
            min_row = df.loc[min_idx].to_dict()
            min_value = df.loc[min_idx, selected_col]
            
            # Convert numpy types to Python native types
            min_row = convert_to_serializable(min_row)
            min_value = convert_to_serializable(min_value)
            
            return {
                "status": "success",
                "data": {
                    "min_record": min_row,
                    "min_column": selected_col,
                    "min_value": min_value
                },
                "message": f"Student/Record with minimum {selected_col}: {min_value}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error finding minimum student: {str(e)}"
            }
    
    def list_students(self, df: pd.DataFrame, query: str = None) -> Dict[str, Any]:
        """List all students/records in the dataset"""
        try:
            total_students = len(df)
            students_list = df.to_dict('records')
            
            # Convert numpy types to Python native types
            students_list = convert_to_serializable(students_list)
            
            return {
                "status": "success",
                "data": {
                    "total_count": total_students,
                    "students": students_list
                },
                "message": f"Total students/records: {total_students}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error listing students: {str(e)}"
            }
    
    # ========== INTELLIGENT VISUALIZATION SYSTEM ==========
    
    def _suggest_best_visualization(self, df: pd.DataFrame, query: str, numeric_cols: List[str], categorical_cols: List[str]) -> tuple:
        """
        Intelligently suggest the best visualization type based on data characteristics and user query
        Returns: (chart_type, x_col, y_col, reason)
        """
        query_lower = query.lower()
        n_rows = len(df)
        n_numeric = len(numeric_cols)
        n_categorical = len(categorical_cols)
        
        # Check for explicit user requests
        if "pie" in query_lower and n_categorical >= 1:
            return ("pie", categorical_cols[0], None, "Pie chart requested for categorical data")
        
        if "box" in query_lower or "boxplot" in query_lower:
            if n_numeric >= 1:
                x_col = categorical_cols[0] if categorical_cols else None
                y_col = numeric_cols[0]
                return ("box", x_col, y_col, "Box plot requested for distribution analysis")
        
        if "line" in query_lower and n_numeric >= 2:
            return ("line", numeric_cols[0], numeric_cols[1], "Line chart requested for trend analysis")
        
        if "area" in query_lower and n_numeric >= 2:
            return ("area", numeric_cols[0], numeric_cols[1], "Area chart requested")
        
        if "scatter" in query_lower and n_numeric >= 2:
            return ("scatter", numeric_cols[0], numeric_cols[1], "Scatter plot requested for correlation analysis")
        
        if "bar" in query_lower or "histogram" in query_lower:
            if n_categorical >= 1 and n_numeric >= 1:
                return ("bar", categorical_cols[0], numeric_cols[0], "Bar chart requested for comparison")
            elif n_numeric >= 1:
                return ("histogram", numeric_cols[0], None, "Histogram requested for distribution")
        
        if "heatmap" in query_lower and n_numeric >= 2:
            return ("heatmap", numeric_cols[0], numeric_cols[1], "Heatmap requested for correlation matrix")
        
        if "violin" in query_lower and n_numeric >= 1:
            return ("violin", categorical_cols[0] if categorical_cols else None, numeric_cols[0], "Violin plot requested")
        
        # Auto-suggest based on data characteristics
        
        # Rule 1: If user asks about distribution/spread/variation
        if any(word in query_lower for word in ["distribution", "spread", "variance", "spread"]):
            if n_numeric >= 1:
                return ("histogram", numeric_cols[0], None, "Histogram best for distribution analysis")
        
        # Rule 2: If user asks about relationship/correlation/comparison between two numeric
        if any(word in query_lower for word in ["relationship", "correlation", "compare", "vs", "against"]) and n_numeric >= 2:
            return ("scatter", numeric_cols[0], numeric_cols[1], "Scatter plot best for correlation analysis")
        
        # Rule 3: If user asks about trends/over time/change
        if any(word in query_lower for word in ["trend", "over time", "change", "growth", "decline"]) and n_numeric >= 2:
            return ("line", numeric_cols[0], numeric_cols[1], "Line chart best for trend analysis")
        
        # Rule 4: If user asks about categories/groups/breakdown
        if any(word in query_lower for word in ["by", "category", "group", "breakdown", "segment", "pie"]) and categorical_cols and n_numeric >= 1:
            if "pie" in query_lower or n_categorical == 1:
                return ("pie", categorical_cols[0], None, "Pie chart best for categorical breakdown")
            else:
                return ("bar", categorical_cols[0], numeric_cols[0], "Bar chart best for grouped comparison")
        
        # Rule 5: Default smart selection based on data shape
        if n_numeric >= 2 and n_categorical == 0:
            # Two or more numeric columns, no categorical
            return ("scatter", numeric_cols[0], numeric_cols[1], "Scatter plot for multi-numeric analysis")
        
        if n_categorical >= 1 and n_numeric >= 1:
            # Mix of categorical and numeric
            if len(df[categorical_cols[0]].unique()) <= 10:  # If few categories
                return ("bar", categorical_cols[0], numeric_cols[0], "Bar chart for categorical vs numeric")
            else:
                return ("box", categorical_cols[0], numeric_cols[0], "Box plot for many categories")
        
        if n_numeric >= 1:
            # Only numeric columns
            return ("histogram", numeric_cols[0], None, "Histogram for single numeric analysis")
        
        if categorical_cols:
            # Only categorical
            return ("pie", categorical_cols[0], None, "Pie chart for categorical distribution")
        
        return ("bar", None, None, "Default bar chart")
    
    def create_visualization(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Intelligently create visualization based on query and data characteristics"""
        try:
            numeric_cols, categorical_cols = get_numeric_and_categorical_columns(df)
            columns = df.columns.tolist()
            
            if not numeric_cols and not categorical_cols:
                return {
                    "status": "error",
                    "error": "No suitable columns for visualization"
                }
            
            # Try to extract specific columns from query
            x_col, y_col = extract_columns_from_query(query, columns)
            
            # If user specified columns, use them
            if x_col:
                # Suggest chart type based on the columns they specified
                chart_type, suggested_x, suggested_y, reason = self._suggest_best_visualization(
                    df[x_col:x_col+1] if x_col and not y_col else df, 
                    query, 
                    numeric_cols, 
                    categorical_cols
                )
            else:
                # No columns specified, let AI suggest everything
                chart_type, x_col, y_col, reason = self._suggest_best_visualization(
                    df, query, numeric_cols, categorical_cols
                )
            
            # Validate and fix columns
            if x_col and x_col not in columns:
                x_col = numeric_cols[0] if numeric_cols else categorical_cols[0]
            
            if y_col and y_col not in columns:
                y_col = numeric_cols[1] if len(numeric_cols) > 1 else (numeric_cols[0] if numeric_cols else None)
            
            # Create the figure based on chart type
            fig = None
            title = f"Data Visualization: {query[:40]}..."
            
            try:
                if chart_type == "histogram":
                    fig = px.histogram(df, x=x_col, nbins=30, title=f"Distribution of {x_col}")
                
                elif chart_type == "scatter" and x_col and y_col:
                    fig = px.scatter(df, x=x_col, y=y_col, title=f"Correlation: {x_col} vs {y_col}")
                
                elif chart_type == "bar" and x_col and y_col:
                    if x_col in categorical_cols:
                        fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                    else:
                        fig = px.bar(df, x=y_col, title=f"Distribution of {y_col}")
                
                elif chart_type == "line" and x_col and y_col:
                    fig = px.line(df, x=x_col, y=y_col, title=f"Trend: {x_col} vs {y_col}", markers=True)
                
                elif chart_type == "area" and x_col and y_col:
                    fig = px.area(df, x=x_col, y=y_col, title=f"Area: {x_col} vs {y_col}")
                
                elif chart_type == "pie" and x_col:
                    if x_col in categorical_cols:
                        fig = px.pie(df, names=x_col, title=f"Distribution of {x_col}")
                    else:
                        fig = px.pie(df, values=x_col, title=f"Distribution of {x_col}")
                
                elif chart_type == "box" and x_col and y_col:
                    fig = px.box(df, x=x_col if x_col in categorical_cols else None, y=y_col, 
                                title=f"Distribution: {y_col}")
                
                elif chart_type == "violin" and y_col:
                    fig = px.violin(df, x=x_col if x_col in categorical_cols else None, y=y_col, 
                                   title=f"Violin: {y_col}")
                
                elif chart_type == "heatmap" and x_col and y_col:
                    # Create correlation heatmap for numeric columns
                    corr_matrix = df[numeric_cols].corr()
                    fig = px.imshow(corr_matrix, text_auto=True, 
                                   title="Correlation Heatmap of Numeric Columns")
                
                else:
                    # Fallback to scatter or histogram
                    if x_col and y_col:
                        fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
                    elif x_col:
                        fig = px.histogram(df, x=x_col, title=f"Distribution of {x_col}")
                
                if fig is None:
                    raise ValueError("Could not create figure")
            
            except Exception as e:
                print(f"Error creating {chart_type}: {e}. Falling back to histogram.")
                if numeric_cols:
                    fig = px.histogram(df, x=numeric_cols[0], title=f"Distribution of {numeric_cols[0]}")
                else:
                    return {
                        "status": "error",
                        "error": f"Could not create visualization: {str(e)}"
                    }
            
            # Update layout for professional appearance
            fig.update_layout(
                width=900,
                height=600,
                template="plotly_white",
                font=dict(size=11, family="Arial"),
                title_font_size=16,
                hovermode="closest",
                plot_bgcolor="rgba(240,240,240,0.5)"
            )
            
            # Save chart as PNG
            filename = f"chart_{uuid.uuid4().hex}.png"
            filepath = os.path.join(self.chart_dir, filename)
            
            try:
                fig.write_image(filepath, width=900, height=600)
            except Exception as e:
                print(f"PNG export failed: {e}. Falling back to HTML.")
                filename = f"chart_{uuid.uuid4().hex}.html"
                filepath = os.path.join(self.chart_dir, filename)
                fig.write_html(filepath)
            
            # Generate AI insight
            insight = self._generate_insight(df, chart_type, x_col, y_col)
            
            return {
                "status": "success",
                "chart_path": filepath,
                "chart_type": chart_type,
                "x_column": x_col,
                "y_column": y_col,
                "insight": insight,
                "recommendation": f"Using {chart_type.upper()} - {reason}",
                "message": f"✨ {chart_type.capitalize()} visualization created"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error creating visualization: {str(e)}"
            }
    
    # ========== AI ANALYSIS ==========
    
    def generate_ai_analysis(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Generate AI-based insights for general queries"""
        try:
            if not self.llm_available:
                return {
                    "status": "error",
                    "error": "LLM service not available"
                }
            
            preview_data = df.head().to_string()
            
            prompt = f"""
You are a professional data analyst.

Dataset Preview:
{preview_data}

User Query:
{query}

Provide clear, actionable insights based on the data and query.
Keep the response concise and professional.
            """
            
            response = self.llm.invoke(prompt)
            
            return {
                "status": "success",
                "data": {"insight": response},
                "message": "AI analysis generated"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error generating AI analysis: {str(e)}"
            }
    
    def _generate_insight(self, df: pd.DataFrame, chart_type: str, x_col: str, y_col: Optional[str] = None) -> str:
        """Generate AI insight for a visualization"""
        try:
            if not self.llm_available:
                return f"Chart generated successfully. {chart_type.capitalize()} showing {x_col}."
            
            preview_data = df.head().to_string()
            
            if y_col:
                prompt = f"""
You are a professional data analyst. Briefly explain the {chart_type} chart showing {x_col} vs {y_col}.

Dataset preview:
{preview_data}

Provide 2-3 key insights about the relationship or distribution. Keep it concise.
                """
            else:
                prompt = f"""
You are a professional data analyst. Briefly explain the {chart_type} showing the distribution of {x_col}.

Dataset preview:
{preview_data}

Provide 2-3 key insights. Keep it concise.
                """
            
            insight = self.llm.invoke(prompt)
            return insight
        
        except Exception as e:
            return f"Chart generated successfully. Unable to generate AI insight: {str(e)}"
