import os
import re
import json
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
    # This line removes code block markers (```python and ```) which we got from AI 
    result = re.sub(r"```[\s\S]*?\n|\n```", "", result)
    result_dict = json.loads(result)
    return result_dict

def suggest_feature_pairs(df):
    messages = [
        ("system", "You are an expert in data visualization and EDA."),
        ("human", '''
        Based on the dataset summary and column names, suggest the **top 5 most meaningful feature pairs** for visualization.
        
        ### **Guidelines:**
        - **Numerical vs Numerical:** Use `"Scatter Plot"` or `"Line Chart"` if time-based.
        - **Categorical vs Numerical:** Use `"Box Plot"` or `"Violin Plot"`.
        - **Categorical vs Categorical:** Use `"Stacked Bar Chart"`.

        ### **Column Names:**
        {column_names}

        ### **Summary:**
        {summary}

        ### **Expected JSON Output:**
        ```json
        {{
            "pair_1": ["feature_x", "feature_y", "Visualization Type"],
            "pair_2": ["feature_x", "feature_y", "Visualization Type"],
            "pair_3": ["feature_x", "feature_y", "Visualization Type"],
            "pair_4": ["feature_x", "feature_y", "Visualization Type"],
            "pair_5": ["feature_x", "feature_y", "Visualization Type"]
        }}
        ```
        ''')
    ]

    prompt_template = ChatPromptTemplate.from_messages(messages)
    chain = prompt_template | model | StrOutputParser()
    result = chain.invoke({"column_names": str(df.columns.to_list()), "summary": summary(df)})

    # Clean AI response and convert JSON to dictionary
    result = re.sub(r"```[\s\S]*?\n|\n```", "", result)
    result_dict = json.loads(result)

    return result_dict

def show_graphs(df):
    visualizations = analysis_for_graphs(df) 
    for column, plot_type in visualizations.items():
        fig, ax = plt.subplots(figsize=(8, 5))
        
        if plot_type == "Histogram":
            sns.histplot(df[column], bins=20, kde=True, color="blue", ax=ax)
            ax.set_xlabel(column)
            ax.set_ylabel("Frequency")

        elif plot_type == "Box Plot":
            sns.boxplot(y=df[column], palette="coolwarm", ax=ax)
            ax.set_ylabel(column)

        elif plot_type == "Bar Chart":
            sns.countplot(x=df[column], palette="viridis", ax=ax)
            ax.set_xlabel(column)
            ax.set_ylabel("Count")

        elif plot_type == "Pie Chart":
            df[column].value_counts().plot.pie(autopct='%1.1f%%', cmap="viridis", ax=ax)
            ax.set_ylabel("")

        elif plot_type == "Line Chart":
            df[column].plot(kind='line', ax=ax)
            ax.set_xlabel("Index")
            ax.set_ylabel(column)

        elif plot_type == "Scatter Plot":
            num_cols = df.select_dtypes(include=['number']).columns
            if len(num_cols) >= 2:
                sns.scatterplot(x=df[num_cols[0]], y=df[num_cols[1]], ax=ax)
                ax.set_xlabel(num_cols[0])
                ax.set_ylabel(num_cols[1])

        else:
            st.write(f"🚫 No Visualization Needed for {column}")
            continue  

        ax.set_title(f"{plot_type} of {column}")
        plt.xticks(rotation=45) 

        st.pyplot(fig)

def show_pairwise_graphs(df):
    feature_pairs = suggest_feature_pairs(df)

    for key, (x_feature, y_feature, plot_type) in feature_pairs.items():
        fig, ax = plt.subplots(figsize=(8, 5))

        if plot_type == "Scatter Plot":
            sns.scatterplot(x=df[x_feature], y=df[y_feature], ax=ax)
            ax.set_xlabel(x_feature)
            ax.set_ylabel(y_feature)

        elif plot_type == "Line Chart":
            df.plot(x=x_feature, y=y_feature, kind='line', ax=ax)
            ax.set_xlabel(x_feature)
            ax.set_ylabel(y_feature)

        elif plot_type == "Box Plot":
            sns.boxplot(x=df[x_feature], y=df[y_feature], ax=ax)

        elif plot_type == "Violin Plot":
            sns.violinplot(x=df[x_feature], y=df[y_feature], ax=ax)

        elif plot_type == "Stacked Bar Chart":
            cross_tab = pd.crosstab(df[x_feature], df[y_feature])
            cross_tab.plot(kind='bar', stacked=True, colormap='viridis', ax=ax)

        else:
            st.write(f"🚫 No Visualization Needed for {x_feature} vs {y_feature}")
            continue  

        ax.set_title(f"{plot_type} of {x_feature} vs {y_feature}")
        plt.xticks(rotation=45)

        st.pyplot(fig)


def main():

    st.set_page_config(page_title="Auto.EDA", page_icon="📊")  
    st.title("Auto EDA")
    st.sidebar.title("Auto EDA")
    st.sidebar.title("Upload Dataset")


    file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

    with st.sidebar.container():
        st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)  
        st.markdown("---") 
        st.markdown("**Disclaimer:** Some parts of this app are AI-generated and may not be 100% accurate.")  

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
        st.write("### Feature Pair Analysis:")
        show_pairwise_graphs(df)
        st.write("Univariate Analysis:")
        show_graphs(df)
    else:
        st.write("Upload a CSV file to get started!")

if __name__ == "__main__":
    main()