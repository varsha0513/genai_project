from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import pandas as pd
import matplotlib.pyplot as plt
import uuid
import os

# LLM
from langchain_ollama import OllamaLLM

# Initialize LLM
llm = OllamaLLM(model="mistral")

app = FastAPI()

# Global dataset
df = None


# ------------------------------
# ROOT
# ------------------------------
@app.get("/")
def home():
    return {"message": "API is running successfully 🚀"}


# ------------------------------
# 1️⃣ Upload CSV (RAW DATA)
# ------------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global df

    df = pd.read_csv(file.file)

    return {
        "message": "File uploaded successfully (raw data)",
        "columns": list(df.columns),
        "rows": len(df)
    }


# ------------------------------
# 2️⃣ Preview Data
# ------------------------------
@app.get("/preview")
def preview():
    if df is None:
        return {"error": "No data uploaded"}

    clean_df = df.copy()

    # Fix JSON issues
    clean_df.replace([float("inf"), float("-inf")], None, inplace=True)
    clean_df = clean_df.where(pd.notnull(clean_df), None)

    return clean_df.head().to_dict(orient="records")


# ------------------------------
# 3️⃣ Dataset Info
# ------------------------------
@app.get("/info")
def info():
    if df is None:
        return {"error": "No data uploaded"}

    return {
        "columns": list(df.columns),
        "shape": df.shape,
        "missing_values": df.isnull().sum().to_dict()
    }


# ------------------------------
# 4️⃣ SMART AI QUERY SYSTEM
# ------------------------------
@app.post("/query")
def query_data(query: str):
    global df

    if df is None:
        return {"error": "Upload dataset first"}

    query_lower = query.lower()

    # --------------------------
    # 🧹 CLEANING ACTIONS
    # --------------------------
    if "missing" in query_lower:
        df.dropna(inplace=True)
        return {"message": "Missing values removed"}

    if "duplicate" in query_lower:
        df.drop_duplicates(inplace=True)
        return {"message": "Duplicates removed"}

    # --------------------------
    # 📊 CHART DETECTION
    # --------------------------
    if "plot" in query_lower or "chart" in query_lower or "graph" in query_lower:

        columns = df.columns.tolist()
        words = query_lower.split()

        x_col = None
        y_col = None

        # Better column detection
        for col in columns:
            if col.lower() in words:
                if x_col is None:
                    x_col = col
                else:
                    y_col = col

        if x_col is None or y_col is None:
            return {
                "error": f"Could not detect columns. Available columns: {columns}"
            }

        # Ensure numeric for plotting
        if not pd.api.types.is_numeric_dtype(df[y_col]):
            return {"error": f"{y_col} must be numeric for plotting"}

        # Create chart
        plt.figure()
        plt.plot(df[x_col], df[y_col])

        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f"{y_col} vs {x_col}")

        # Save chart
        os.makedirs("charts", exist_ok=True)
        filename = f"chart_{uuid.uuid4().hex}.png"
        filepath = os.path.join("charts", filename)

        plt.savefig(filepath)
        plt.close()

        # AI insight
        data_preview = df[[x_col, y_col]].head().to_string()

        prompt = f"""
        You are a data analyst.

        Data:
        {data_preview}

        Explain the trend between {x_col} and {y_col}.
        """

        insight = llm.invoke(prompt)

        return {
            "chart": filepath,
            "insight": insight
        }

    # --------------------------
    # 🧠 NORMAL AI ANALYSIS
    # --------------------------
    data_preview = df.head().to_string()

    prompt = f"""
    You are a data analyst assistant.

    Dataset preview:
    {data_preview}

    User question:
    {query}

    Give a clear answer with insights.
    """

    response = llm.invoke(prompt)

    return {"response": response}


# ------------------------------
# 5️⃣ DOWNLOAD EXCEL
# ------------------------------
@app.get("/download")
def download_file():
    global df

    if df is None:
        return {"error": "No data available"}

    file_path = "cleaned_data.xlsx"
    df.to_excel(file_path, index=False)

    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="cleaned_data.xlsx"
    )