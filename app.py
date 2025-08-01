# app.py
import streamlit as st
import pandas as pd
import openai

# Rule-based chatbot function
def simple_chatbot(user_query):
    if user_query == "What is the total revenue?":
        return "The total revenue for 2022 (example) is $290 million."
    elif user_query == "How has net income changed over the last year?":
        return "Net income increased by $5 million from 2021 to 2022."
    elif user_query == "What were Tesla's total assets in 2022?":
        return "Tesla's total assets in 2022 were $150 million."
    elif user_query == "What were Apple's total liabilities in 2022?":
        return "Apple's total liabilities in 2022 were $110 million."
    elif user_query == "What was Microsoft's cash flow in 2022?":
        return "Microsoft's cash flow from operating activities in 2022 was $40 million."
    else:
        return None  # return None so we can try OpenAI fallback

# Fallback GPT chatbot using OpenAI API
def gpt_chatbot(user_query, api_key):
    if not api_key:
        return "Please enter a valid OpenAI API key in the sidebar."
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial analysis assistant. Answer financial questions clearly."},
                {"role": "user", "content": user_query}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error using OpenAI API: {e}"

# Data-driven financial analysis function
def analyze_financial_data(df):
    df['Revenue_YoY_Change'] = df['Total Revenue'].pct_change() * 100
    df['Net_Income_YoY_Change'] = df['Net Income'].pct_change() * 100
    df['Total_Assets_YoY_Change'] = df['Total Assets'].pct_change() * 100
    df['Total_Liabilities_YoY_Change'] = df['Total Liabilities'].pct_change() * 100
    df['Cash_Flow_YoY_Change'] = df['Cash Flow from Operating Activities'].pct_change() * 100
    return df

# Load sample data
@st.cache_data
def load_sample_data():
    try:
        df = pd.read_csv("Financial_Data_Bhargavi_Sisode.csv")
        return df
    except:
        return pd.DataFrame()

# Streamlit app layout
st.set_page_config(page_title="Financial AI Chatbot", layout="wide")
st.title("\U0001F4B8 Financial AI Chatbot")
st.write("Ask about revenue, net income, assets, liabilities, and more!")

# Sidebar for API key and file upload
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.markdown("---")
    st.header("Upload Financial CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        df = load_sample_data()

# Show data and analysis
if not df.empty:
    st.subheader("Uploaded Financial Data")
    st.dataframe(df)

    st.subheader("Financial Insights (YoY Change)")
    analyzed_df = analyze_financial_data(df.copy())
    st.dataframe(analyzed_df)
else:
    st.warning("No financial data loaded. Upload a valid CSV to view analysis.")

# Chatbot section
st.subheader("Chat with the Financial Bot")
user_query = st.text_input("Enter your question")

if user_query:
    response = simple_chatbot(user_query)
    if response is None:
        response = gpt_chatbot(user_query, api_key)
    st.success(response)

# Footer
st.markdown("---")
st.markdown("Made by Bhargavi Sisode | Financial GenAI Project")
