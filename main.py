import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=os.getenv('GEMINI_API_KEY'), max_tokens=1000)

def summary(df): 
    messages = [
    ("system", "You are a Data Science Expert"),
    ("human", '''Given the following dataset sample, provide a very short concise pointed summary of what it might represent or be related to. 
     Suggesting a possible use case or domain for the data based on the feature names and their data types.
     Dataset sample : \n {datasample} ''')]
    prompt_template = ChatPromptTemplate.from_messages(messages)
    chain = prompt_template | model | StrOutputParser()
    result = chain.invoke({"datasample": df.head(10).to_string(index=False)})
    return result

def analysis_for_graphs(df):
    metadata = {col: {
        "dtype": "categorical" if df[col].dtype == "object" else "numerical",
        "unique_values": df[col].nunique(),
        "missing_values": df[col].isna().sum()
    }
    for col in df.columns
    }
    
    messages = [
    ("system", "You are an expert in Exploratory Data Analysis (EDA)."),
    ("human", '''
     
    ### **Guidelines:**
    - **Categorical Data (object, low unique counts < 30):** Use `"Bar Chart"` or `"Pie Chart"`.
    - **Numerical Data (continuous):** Use `"Histogram"` for distribution, `"Box Plot"` for outliers.
    - **Time Series Data:** Use `"Line Chart"`.
    - **Correlation Analysis:** Use `"Scatter Plot"` for relationships between two numerical columns.
    - If the column is not relevant for visualization, return `"No Visualization Needed"`.

    ### **Column Names:**
    {column_names}

    ### **Metadata:**
    {metadata}
     
    ### **Retunrn the out strictly in below mentioned format no extra output is required:**

    ```json
    {{
    "column 1": "Visualization Type",
    "column 2": "Visualization Type",
    "column 3": "Visualization Type"
     till 
    "column n": "Visualization Type"

    }}''')]
    prompt_template = ChatPromptTemplate.from_messages(messages)
    chain = prompt_template | model | StrOutputParser()
    result = chain.invoke({'column_names':str(df.columns.to_list()),'metadata':str(metadata)})
    return result


def main():
    st.title("Auto EDA")
    st.sidebar.title("Auto EDA")
    st.sidebar.title("Upload Dataset")

    file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])
    
    if file is not None:
        df = pd.read_csv(file)
        st.write("### AI Summary")
        st.write(summary(df))
        st.write("### Dataset Preview:")
        st.dataframe(df.head())
        st.write("### Column Names:")
        st.write(", ".join(df.columns))
        st.write("### Data Types:")
        dtypes_df = pd.DataFrame(df.dtypes).reset_index()
        dtypes_df.columns = ['Feature', 'Data Type']
        st.dataframe(dtypes_df.style.hide(axis="index"), use_container_width=True, height=200)
        st.write("### Summary Statistics:")
        st.dataframe(df.describe(),use_container_width=True)
        st.write("### Shape:")
        st.write(df.shape)
        st.write("### Missing Values:")
        st.dataframe(df.isnull().sum(),use_container_width=True)
        st.write(analysis_for_graphs(df))
    else:
        st.write("Upload a CSV file to get started!")

if __name__ == "__main__":
    main()