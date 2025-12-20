import os
import io
import json
import base64
import re
from typing import List, Dict, Any

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from google.api_core.exceptions import ResourceExhausted

# 1. Server Configuration
# 'Agg' backend is required for server-side plotting (non-GUI)
matplotlib.use('Agg')

load_dotenv()

app = FastAPI(title="Auto EDA Backend")

# 2. CORS Setup (Crucial for Next.js communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://autoeda.kabillanta.me"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Initialize AI Model
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

model = ChatGoogleGenerativeAI(model="models/gemini-flash-lite-latest", api_key=api_key)

# --- Helper Functions ---

def load_data_from_file(file: UploadFile) -> pd.DataFrame:
    """Reads uploaded file into a Pandas DataFrame."""
    try:
        contents = file.file.read()
        buffer = io.BytesIO(contents)
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension == "csv":
            df = pd.read_csv(buffer)
        elif file_extension in ["xls", "xlsx"]:
            df = pd.read_excel(buffer, engine="openpyxl")
        elif file_extension == "json":
            df = pd.read_json(buffer)
        elif file_extension == "parquet":
            df = pd.read_parquet(buffer)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Reset file pointer for safety
        file.file.seek(0)
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

def plot_to_base64(fig) -> str:
    """Converts a Matplotlib figure to a Base64 string for the frontend."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig) # Close explicitly to avoid memory leaks
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def clean_json_response(response: str) -> Dict:
    """Cleans Markdown code blocks from AI response and parses JSON."""
    clean_str = re.sub(r"```json|```", "", response).strip()
    try:
        return json.loads(clean_str)
    except json.JSONDecodeError:
        return {}

# --- Core AI Logic (Refactored from Streamlit) ---

def get_ai_summary(df: pd.DataFrame) -> str:
    # 1. We define {dataset_sample} as a placeholder for LangChain
    messages = [
        ("system", "You are a Data Science Expert"),
        ("human", "Given the following dataset sample, provide a very short, concise summary.\n\nDataset sample:\n{dataset_sample}")
    ]
    
    # 2. We pass the actual data in .invoke()
    chain = ChatPromptTemplate.from_messages(messages) | model | StrOutputParser()
    return chain.invoke({"dataset_sample": df.head(10).to_string(index=False)})

def get_visualization_suggestions(df: pd.DataFrame) -> Dict[str, str]:
    metadata = {col: {
        "dtype": "categorical" if df[col].dtype == "object" else "numerical",
        "unique_values": df[col].nunique()
    } for col in df.columns}

    # 1. Use double curly braces {{ }} for literal JSON examples
    # 2. Use single curly braces {metadata} for the variable input
    messages = [
        ("system", "You are an EDA Expert. Output ONLY valid JSON."),
        ("human", """
        Suggest visualizations for these columns based on metadata.
        Options: "Bar Chart", "Pie Chart", "Histogram", "Box Plot", "Line Chart", "Scatter Plot", "No Visualization Needed".
        
        Metadata:
        {metadata}
        
        Return format:
        {{ "col_name": "Visualization Type" }}
        """)
    ]
    
    chain = ChatPromptTemplate.from_messages(messages) | model | StrOutputParser()
    
    # We pass the metadata dictionary as a string here. 
    # LangChain fills it in safely, ignoring any curly braces inside the data itself.
    return clean_json_response(chain.invoke({"metadata": str(metadata)}))

def get_pairwise_suggestions(df: pd.DataFrame, summary_text: str) -> Dict[str, list]:
    messages = [
        ("system", "You are an expert in data visualization. Output ONLY valid JSON."),
        ("human", """
        Suggest top 5 meaningful feature pairs for visualization.
        
        Columns: {columns}
        Summary: {summary}
        
        Return format: 
        {{
            "pair_1": ["feature_x", "feature_y", "Visualization Type"],
            "pair_2": ["feature_x", "feature_y", "Visualization Type"]
        }}
        Options: Scatter Plot, Line Chart, Box Plot, Violin Plot, Stacked Bar Chart.
        """)
    ]
    
    chain = ChatPromptTemplate.from_messages(messages) | model | StrOutputParser()
    
    return clean_json_response(chain.invoke({
        "columns": str(df.columns.to_list()),
        "summary": summary_text
    }))

@app.post("/api/analyze")
async def analyze_dataset(file: UploadFile = File(...)):
    """
    Main orchestrator: 
    1. Loads Data
    2. Gets AI Summary
    3. Generates Univariate Graphs
    4. Generates Pairwise Graphs
    5. Returns everything as JSON
    """
    
    # 1. Load Data
    df = load_data_from_file(file)
    
    if len(df) > 5000:
        df = df.sample(5000)

    # 2. AI Summary
    summary_text = get_ai_summary(df)

    # 3. Univariate Analysis (Generating Graphs)
    univariate_graphs = []
    suggestions = get_visualization_suggestions(df)

    for col, plot_type in suggestions.items():
        if plot_type == "No Visualization Needed" or col not in df.columns:
            continue
        
        try:
            fig, ax = plt.subplots(figsize=(6, 4))
            
            if plot_type == "Histogram":
                sns.histplot(df[col], bins=20, kde=True, ax=ax)
            elif plot_type == "Box Plot":
                sns.boxplot(y=df[col], ax=ax)
            elif plot_type == "Bar Chart":
                # Limit bars for clean UI
                top_counts = df[col].value_counts().head(15)
                sns.barplot(x=top_counts.index, y=top_counts.values, ax=ax)
                plt.xticks(rotation=45)
            elif plot_type == "Pie Chart":
                df[col].value_counts().head(5).plot.pie(autopct='%1.1f%%', ax=ax)
                ax.set_ylabel("")
            elif plot_type == "Line Chart":
                # Basic line plot (using index as x-axis if not time series)
                df[col].plot(kind='line', ax=ax)
            
            ax.set_title(f"{plot_type}: {col}")
            img_base64 = plot_to_base64(fig)
            univariate_graphs.append({
                "id": col,
                "title": f"{plot_type} of {col}",
                "image": f"data:image/png;base64,{img_base64}"
            })
        except Exception as e:
            print(f"Skipping {col}: {e}")
            continue

    # 4. Pairwise Analysis
    pairwise_graphs = []
    pairs = get_pairwise_suggestions(df, summary_text)

    for key, val in pairs.items():
        try:
            if len(val) < 3: continue
            x_feat, y_feat, plot_type = val[0], val[1], val[2]
            
            if x_feat not in df.columns or y_feat not in df.columns:
                continue

            fig, ax = plt.subplots(figsize=(6, 4))

            if plot_type == "Scatter Plot":
                sns.scatterplot(x=df[x_feat], y=df[y_feat], ax=ax)
            elif plot_type == "Box Plot":
                sns.boxplot(x=df[x_feat], y=df[y_feat], ax=ax)
            elif plot_type == "Violin Plot":
                sns.violinplot(x=df[x_feat], y=df[y_feat], ax=ax)
            elif plot_type == "Stacked Bar Chart":
                ct = pd.crosstab(df[x_feat], df[y_feat]).head(10) # Limit size
                ct.plot(kind='bar', stacked=True, ax=ax)
            
            ax.set_xlabel(x_feat)
            ax.set_ylabel(y_feat)
            ax.set_title(f"{plot_type}: {x_feat} vs {y_feat}")
            
            img_base64 = plot_to_base64(fig)
            pairwise_graphs.append({
                "id": key,
                "title": f"{plot_type}: {x_feat} vs {y_feat}",
                "image": f"data:image/png;base64,{img_base64}"
            })
        except Exception as e:
            print(f"Skipping pair {key}: {e}")
            continue
        except ResourceExhausted:
            raise HTTPException(
            status_code=429,
            detail="AI quota exceeded. Please try again in a minute.")
          
          
    column_details = []
    for col in df.columns:
        column_details.append({
            "name": col,
            "type": str(df[col].dtype),
            "missing_values": int(df[col].isnull().sum()),
            "unique_values": int(df[col].nunique())
        })
    
    numerical_stats = df.describe().round(2).to_dict()
    preview_data = df.head().fillna("").to_dict(orient='records')

    # 5. Return JSON payload
    return {
        "filename": file.filename,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "summary": summary_text,
        "column_details": column_details,   
        "numerical_stats": numerical_stats, 
        "preview_data": preview_data,
        "univariate_graphs": univariate_graphs,
        "pairwise_graphs": pairwise_graphs
    }


@app.get("/health")
async def health_check():
    return 'OK'


@app.post("/chat")
async def ai_check(a :str):
    api_key = os.getenv("GOOGLE_API_KEY")
    model = ChatGoogleGenerativeAI(model="models/gemini-flash-lite-latest", api_key=api_key)
    resp = model.invoke(a)
    print(resp.content)
    return resp.content
