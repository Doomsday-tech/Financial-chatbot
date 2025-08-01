# app.py
import streamlit as st
import pandas as pd
import openai
import numpy as np

# Rule-based chatbot function
def simple_chatbot(user_query):
    rules = {
        "What is the total revenue?": "The total revenue for 2022 (example) is $290 million.",
        "How has net income changed over the last year?": "Net income increased by $5 million from 2021 to 2022.",
        "What were Tesla's total assets in 2022?": "Tesla's total assets in 2022 were $150 million.",
        "What were Apple's total liabilities in 2022?": "Apple's total liabilities in 2022 were $110 million.",
        "What was Microsoft's cash flow in 2022?": "Microsoft's cash flow from operating activities in 2022 was $40 million."
    }
    return rules.get(user_query, None)

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

# Financial analysis function
def analyze_financial_data(df):
    df['Revenue_YoY_Change'] = df['Total Revenue'].pct_change() * 100
    df['Net_Income_YoY_Change'] = df['Net Income'].pct_change() * 100
    df['Total_Assets_YoY_Change'] = df['Total Assets'].pct_change() * 100
    df['Total_Liabilities_YoY_Change'] = df['Total Liabilities'].pct_change() * 100
    df['Cash_Flow_YoY_Change'] = df['Cash Flow from Operating Activities'].pct_change() * 100
    return df

@st.cache_data
def load_sample_data():
    try:
        return pd.read_csv("Financial_Data_Bhargavi_Sisode.csv")
    except:
        return pd.DataFrame()

# Page setup
st.set_page_config(page_title="Financial AI Chatbot", layout="wide")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.session_state.dark_mode = st.checkbox("Toggle Dark Mode", value=st.session_state.dark_mode)
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.markdown("---")
    st.header("Upload Financial CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    df = pd.read_csv(uploaded_file) if uploaded_file else load_sample_data()

# Custom dark/light mode CSS
base_color = "#f0f2f6" if not st.session_state.dark_mode else "#1e1e1e"
text_color = "#000" if not st.session_state.dark_mode else "#f5f5f5"
widget_bg = "#fff" if not st.session_state.dark_mode else "#333"

custom_css = f"""
<style>
body, .main, .stApp {{
    background-color: {base_color};
    color: {text_color};
}}
input, textarea {{
    background-color: {widget_bg} !important;
    color: {text_color} !important;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Main App
st.title("\U0001F4B8 Financial AI Chatbot")
st.write("Ask about revenue, net income, assets, liabilities, and more!")

if not df.empty:
    st.subheader("Uploaded Financial Data")
    st.dataframe(df)

    st.subheader("Financial Insights (YoY Change)")
    analyzed_df = analyze_financial_data(df.copy())
    st.dataframe(analyzed_df)
else:
    st.warning("No financial data loaded. Upload a valid CSV to view analysis.")

st.subheader("Chat with the Financial Bot")
user_query = st.text_input("Enter your question")
if user_query:
    response = simple_chatbot(user_query) or gpt_chatbot(user_query, api_key)
    st.success(response)

# Calculators
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
        emi = loan_amount * monthly_rate * ((1 + monthly_rate)**num_months) / (((1 + monthly_rate)**num_months) - 1) if monthly_rate else loan_amount / num_months
        st.success(f"Monthly EMI: ${emi:.2f}")

# Footer
st.markdown("---")
st.markdown("<center>Made by Bhargavi Sisode | Financial GenAI Project</center>", unsafe_allow_html=True)
