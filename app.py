# app.py
import streamlit as st
import pandas as pd
import openai
import numpy as np

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
        return None

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

# Dark mode toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

with st.sidebar:
    st.header("Settings")
    st.session_state.dark_mode = st.checkbox("Toggle Dark Mode", value=st.session_state.dark_mode)
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.markdown("---")
    st.header("Upload Financial CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        df = load_sample_data()

# Apply colorful style with dark/light toggle
if st.session_state.dark_mode:
    style = """
        <style>
        body {
            background-color: #121212;
            color: #e0e0e0;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > textarea {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #444;
        }
        .css-1d391kg, .stButton>button {
            background-color: #1f1f1f;
            color: #ffcc00;
            border-radius: 10px;
        }
        </style>
    """
else:
    style = """
        <style>
        body {
            background: linear-gradient(to right, #ffe4e1, #e0ffff);
            color: #333333;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > textarea {
            background-color: #fff0f5;
            color: #000000;
            border: 1px solid #ffb6c1;
        }
        .css-1d391kg, .stButton>button {
            background-color: #c1e1c1;
            color: #003366;
            border-radius: 10px;
        }
        </style>
    """
st.markdown(style, unsafe_allow_html=True)

st.title("\U0001F4B8 Financial AI Chatbot")
st.write("Ask about revenue, net income, assets, liabilities, and more!")

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

# Calculators Section
st.markdown("---")
st.subheader("\U0001F9EE Financial Calculators")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Compound Interest Calculator")
    principal = st.number_input("Principal Amount", min_value=0.0)
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
    time = st.number_input("Time (Years)", min_value=0.0)
    compoundings = st.number_input("Compoundings per Year", min_value=1)

    if st.button("Calculate Compound Interest"):
        amount = principal * (1 + rate / (100 * compoundings))**(compoundings * time)
        st.success(f"Future Value: ${amount:.2f}")

with col2:
    st.markdown("### Loan EMI Calculator")
    loan_amount = st.number_input("Loan Amount", min_value=0.0)
    annual_rate = st.number_input("Interest Rate (%)", min_value=0.0)
    loan_term = st.number_input("Loan Term (Years)", min_value=0.0)

    if st.button("Calculate EMI"):
        monthly_rate = annual_rate / (12 * 100)
        num_months = loan_term * 12
        if monthly_rate > 0:
            emi = loan_amount * monthly_rate * ((1 + monthly_rate)**num_months) / (((1 + monthly_rate)**num_months) - 1)
        else:
            emi = loan_amount / num_months
        st.success(f"Monthly EMI: ${emi:.2f}")

# Footer
st.markdown("---")
st.markdown("Made by Bhargavi Sisode | Financial GenAI Project")

