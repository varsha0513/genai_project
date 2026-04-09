"""
AI-Powered Smart Data Analyst System - Main FastAPI Backend
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uuid
import os
import numpy as np
from typing import Dict, Optional

from schemas import (
    QueryRequest, UploadResponse, PreviewResponse, 
    DatasetInfoResponse, QueryResponse, ChartResponse
)
from analyzer import DataAnalyzer
from utils import detect_query_intent

# ========== INITIALIZATION ==========

app = FastAPI(
    title="AI Data Analyst API",
    description="Natural Language Data Analysis System",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer (with fallback support)
try:
    analyzer = DataAnalyzer()
    print("✅ DataAnalyzer initialized")
except Exception as e:
    print(f"❌ Failed to initialize DataAnalyzer: {e}")
    analyzer = None

# Session storage (dataset storage by session ID)
datasets: Dict[str, pd.DataFrame] = {}

# ========== UTILITY FUNCTIONS ==========

def get_or_create_session() -> str:
    """Generate session ID (future: implement proper session management)"""
    return "default_session"


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataframe for API output"""
    df_clean = df.copy()
    df_clean.replace([np.inf, -np.inf], None, inplace=True)
    df_clean = df_clean.where(pd.notnull(df_clean), None)
    return df_clean


# ========== ROOT ENDPOINT ==========

@app.get("/", tags=["Health"])
def home():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "AI Data Analyst API is running 🚀",
        "version": "1.0.0"
    }


# ========== FILE UPLOAD ==========

@app.post("/upload", response_model=UploadResponse, tags=["Dataset"])
async def upload_file(file: UploadFile = File(...)):
    """Upload a CSV dataset"""
    try:
        # Validate file extension
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        # Read file contents
        contents = await file.read()
        file_size = len(contents)
        
        # Validate file size (max 100MB)
        if file_size > 100 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File size exceeds 100MB limit")
        
        # Validate file not empty
        if file_size == 0:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        # Read CSV from bytes
        try:
            import io
            df = pd.read_csv(io.BytesIO(contents))
        except pd.errors.EmptyDataError:
            raise HTTPException(status_code=400, detail="CSV file is empty or has no columns")
        except pd.errors.ParserError as e:
            raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Cannot parse CSV: {str(e)}")
        
        # Validate dataset
        if df.empty or len(df.columns) == 0:
            raise HTTPException(status_code=400, detail="Dataset is empty or has no columns")
        
        # Store in session
        session_id = get_or_create_session()
        datasets[session_id] = df
        
        return UploadResponse(
            message="File uploaded successfully",
            columns=list(df.columns),
            rows=len(df),
            file_id=session_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# ========== DATASET PREVIEW ==========

@app.get("/preview", response_model=PreviewResponse, tags=["Dataset"])
def preview():
    """Get preview of uploaded dataset"""
    try:
        session_id = get_or_create_session()
        
        if session_id not in datasets or datasets[session_id] is None:
            raise HTTPException(status_code=400, detail="No dataset uploaded. Please upload a CSV file first.")
        
        df = datasets[session_id]
        df_clean = clean_dataframe(df)
        
        return PreviewResponse(
            data=df_clean.head().to_dict(orient="records"),
            rows=len(df)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview failed: {str(e)}")


# ========== DATASET INFORMATION ==========

@app.get("/info", response_model=DatasetInfoResponse, tags=["Dataset"])
def get_info():
    """Get dataset metadata and statistics"""
    try:
        session_id = get_or_create_session()
        
        if session_id not in datasets or datasets[session_id] is None:
            raise HTTPException(status_code=400, detail="No dataset uploaded")
        
        df = datasets[session_id]
        
        return DatasetInfoResponse(
            columns=list(df.columns),
            shape=df.shape,
            missing_values=df.isnull().sum().to_dict(),
            numeric_columns=df.select_dtypes(include=np.number).columns.tolist(),
            categorical_columns=df.select_dtypes(exclude=np.number).columns.tolist()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Info retrieval failed: {str(e)}")


# ========== SMART QUERY PROCESSING ==========

@app.post("/query", tags=["Analysis"])
def process_query(request: QueryRequest):
    """
    Process natural language query and perform analysis.
    
    Supports:
    - Data cleaning: "remove missing", "remove duplicates"
    - Statistics: "minimum salary", "mean age", "summary"
    - Visualization: "histogram age", "scatter plot salary vs experience", "bar chart"
    - General analysis: "What are the trends in this data?"
    """
    try:
        # Check if analyzer is available
        if analyzer is None:
            raise HTTPException(status_code=500, detail="Analyzer not initialized. Please check backend logs.")
        
        session_id = get_or_create_session()
        
        if session_id not in datasets or datasets[session_id] is None:
            raise HTTPException(status_code=400, detail="No dataset uploaded")
        
        query = request.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        df = datasets[session_id]
        query_lower = query.lower()
        
        # ========== HANDLE COMPOUND QUERIES ==========
        # Check if there's a cleaning operation first
        if any(word in query_lower for word in ["remove", "delete", "drop", "clean"]):
            # Track what operations have been done
            results_summary = {
                "status": "success",
                "operations": [],
                "final_data": df
            }
            
            # Handle missing values
            if any(word in query_lower for word in ["missing", "null", "nan"]):
                result = analyzer.clean_missing_values(df)
                if result.get("status") == "success":
                    results_summary["final_data"] = result.pop("data")
                    results_summary["operations"].append({
                        "type": "missing",
                        "message": result.get("message", "Missing values removed"),
                        "rows_before": int(result["rows_before"]),
                        "rows_after": int(result["rows_after"]),
                        "rows_removed": int(result["rows_removed"])
                    })
            
            # Handle duplicates
            if any(word in query_lower for word in ["duplicate"]):
                result = analyzer.clean_duplicates(results_summary["final_data"])
                if result.get("status") == "success":
                    results_summary["final_data"] = result.pop("data")
                    results_summary["operations"].append({
                        "type": "duplicate",
                        "message": result.get("message", "Duplicates removed"),
                        "rows_before": int(result["rows_before"]),
                        "rows_after": int(result["rows_after"]),
                        "rows_removed": int(result["rows_removed"])
                    })
            
            # Update session dataset
            datasets[session_id] = results_summary["final_data"]
            
            # Check if there are stats/count operations needed (e.g., "and count", "and total", "and show total")
            if any(word in query_lower for word in ["count", "total", "how many", "number", "show"]):
                stats_result = analyzer.analyze_statistics(results_summary["final_data"], query)
                if stats_result.get("status") == "success":
                    results_summary["statistics"] = stats_result.get("data", {})
            
            # Build response message
            if results_summary["operations"]:
                response_text = "✅ **Data Cleaning Complete**\n\n"
                for op in results_summary["operations"]:
                    response_text += f"**{op['message']}:**\n"
                    response_text += f"  • Before: {op['rows_before']} rows\n"
                    response_text += f"  • After: {op['rows_after']} rows\n"
                    response_text += f"  • Removed: {op['rows_removed']} rows\n\n"
                
                if "statistics" in results_summary:
                    response_text += "**Final Statistics:**\n"
                    for key, value in results_summary["statistics"].items():
                        if not isinstance(value, dict):
                            response_text += f"  • {key}: {value}\n"
                
                # Return structured response
                return {
                    "status": "success",
                    "message": response_text,
                    "operations": results_summary["operations"],
                    "statistics": results_summary.get("statistics", {})
                }
            else:
                return {
                    "status": "error",
                    "error": "Cleaning operation not recognized. Try 'remove missing' or 'remove duplicates'"
                }
        
        # ========== HANDLE STUDENT MAX/MIN/LIST QUERIES ==========
        # For queries like "show the maximum scored student and minimum scored student and give the total number of student list"
        has_max = any(word in query_lower for word in ["maximum", "max", "highest"])
        has_min = any(word in query_lower for word in ["minimum", "min", "lowest"])
        has_student = any(word in query_lower for word in ["student", "records", "list"])
        has_show_all = any(word in query_lower for word in ["show", "list", "all", "display"])
        
        # Route to student analysis if: (max/min + student) OR (show/list + student)
        if ((has_max or has_min) and has_student) or (has_student and has_show_all and not has_max and not has_min):
            student_analysis = {
                "status": "success",
                "message": "",
                "data": {}
            }
            
            # Build response message
            response_text = "📊 **Student Analysis**\n\n"
            
            # Get maximum student (if requested)
            if has_max:
                max_result = analyzer.find_max_student(df, query)
                if max_result.get("status") == "success":
                    max_data = max_result.get("data", {})
                    student_analysis["data"]["max_student"] = max_data.get("max_record")
                    
                    response_text += "🏆 **Student with Maximum Score:**\n"
                    max_record = max_data.get("max_record", {})
                    for key, value in max_record.items():
                        response_text += f"  • {key}: {value}\n"
                    response_text += "\n"
            
            # Get minimum student (if requested)
            if has_min:
                min_result = analyzer.find_min_student(df, query)
                if min_result.get("status") == "success":
                    min_data = min_result.get("data", {})
                    student_analysis["data"]["min_student"] = min_data.get("min_record")
                    
                    response_text += "📍 **Student with Minimum Score:**\n"
                    min_record = min_data.get("min_record", {})
                    for key, value in min_record.items():
                        response_text += f"  • {key}: {value}\n"
                    response_text += "\n"
            
            # Get total student count and list
            if has_student:
                list_result = analyzer.list_students(df, query)
                if list_result.get("status") == "success":
                    list_data = list_result.get("data", {})
                    total_count = list_data.get("total_count", 0)
                    student_analysis["data"]["total_students"] = total_count
                    student_analysis["data"]["student_list"] = list_data.get("students", [])
                    
                    response_text += f"👥 **Total Number of Students: {total_count}**\n\n"
                    
                    # Include student list if requested explicitly or when max/min queries request it
                    if has_show_all or (has_max or has_min):
                        response_text += "**Student List:**\n"
                        for idx, student in enumerate(list_data.get("students", []), 1):
                            response_text += f"\n{idx}. {student}\n"
            
            student_analysis["message"] = response_text
            return student_analysis
        
        # Detect query intent for non-cleaning queries
        intent = detect_query_intent(query)
        
        # ========== STATISTICAL ANALYSIS ==========
        if intent == "statistics":
            result = analyzer.analyze_statistics(df, query)
            return result
        
        # ========== VISUALIZATION ==========
        elif intent == "visualization":
            result = analyzer.create_visualization(df, query)
            return result
        
        # ========== GENERAL AI ANALYSIS ==========
        else:
            result = analyzer.generate_ai_analysis(df, query)
            return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


# ========== SERVE CHART IMAGES ==========

@app.get("/chart/{chart_filename}", tags=["Charts"])
def get_chart(chart_filename: str):
    """Serve chart image or HTML files"""
    try:
        import mimetypes
        from pathlib import Path
        
        # Security: ensure filename is valid
        if ".." in chart_filename or "/" in chart_filename or "\\" in chart_filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        # Use the analyzer's chart directory
        chart_path = os.path.join(analyzer.chart_dir, chart_filename)
        
        if not os.path.exists(chart_path):
            raise HTTPException(status_code=404, detail="Chart not found")
        
        # Determine media type
        if chart_filename.endswith('.png'):
            media_type = "image/png"
        elif chart_filename.endswith('.jpg') or chart_filename.endswith('.jpeg'):
            media_type = "image/jpeg"
        elif chart_filename.endswith('.html'):
            media_type = "text/html"
        else:
            media_type = "application/octet-stream"
        
        return FileResponse(chart_path, media_type=media_type)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving chart: {str(e)}")


# ========== DOWNLOAD DATASET ==========

@app.get("/download", tags=["Dataset"])
def download_dataset():
    """Download processed dataset as Excel file"""
    try:
        session_id = get_or_create_session()
        
        if session_id not in datasets or datasets[session_id] is None:
            raise HTTPException(status_code=400, detail="No dataset available")
        
        df = datasets[session_id]
        
        # Create Excel file
        file_path = f"processed_data_{session_id}.xlsx"
        df.to_excel(file_path, index=False)
        
        return FileResponse(
            file_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="processed_data.xlsx"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


# ========== ADVANCED: MULTIPLE CHARTS ==========

@app.post("/analyze/multiple-charts", tags=["Analysis"])
def analyze_multiple_charts(request: QueryRequest):
    """
    Generate multiple visualizations in one request.
    
    Example: "show me histogram age, scatter salary vs experience, bar chart department"
    """
    try:
        session_id = get_or_create_session()
        
        if session_id not in datasets or datasets[session_id] is None:
            raise HTTPException(status_code=400, detail="No dataset uploaded")
        
        df = datasets[session_id]
        query = request.query
        
        # Split by common separators
        queries = [q.strip() for q in query.split(",")]
        
        charts = []
        for sub_query in queries:
            result = analyzer.create_visualization(df, sub_query)
            if result.get("status") == "success":
                charts.append(result)
        
        if not charts:
            return {
                "status": "error",
                "error": "No charts could be generated"
            }
        
        return {
            "status": "success",
            "charts": charts,
            "total_charts": len(charts),
            "message": f"Generated {len(charts)} visualization(s)"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multiple chart analysis failed: {str(e)}")


# ========== ERROR HANDLERS ==========

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle value errors"""
    return {
        "status": "error",
        "error": str(exc)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)