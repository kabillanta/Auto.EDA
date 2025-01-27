import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st 
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
    else:
        st.write("Upload a CSV file to get started!")

if __name__ == "__main__":
    main()