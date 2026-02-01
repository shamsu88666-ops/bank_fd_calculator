import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Professional FD Calculator", page_icon="🏦", layout="wide")

# Custom CSS for Professional UI and fixing overflow
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 30px;
    }
    /* Simple fix for Metric overflow */
    [data-testid="stMetricValue"] {
        font-size: 1.8vw !important;
        color: #ffffff;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.1vw !important;
    }
    .stButton > button {
        width: 100%;
        background-color: #2E5BFF;
        color: white;
        border-radius: 8px;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# Improved Indian Currency Formatting (Fixes the ValueError)
def format_indian_currency(num):
    num = round(num, 2)
    s = str(num)
    if '.' in s:
        integer_part, decimal_part = s.split('.')
    else:
        integer_part, decimal_part = s, '00'
    
    if len(decimal_part) == 1: decimal_part += '0'
    
    last_three = integer_part[-3:]
    others = integer_part[:-3]
    if others != '':
        res = ''
        while len(others) > 2:
            res = ',' + others[-2:] + res
            others = others[:-2]
        formatted_int = others + res + ',' + last_three
    else:
        formatted_int = last_three
        
    return f"₹{formatted_int}.{decimal_part}"

st.markdown('<p class="main-header">Professional FD Return Calculator</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Investment Details")
    principal = st.number_input("Principal Amount (₹)", min_value=0, value=0, step=1000)
    interest_rate = st.number_input("Interest Rate (% p.a.)", min_value=0.0, value=0.0, step=0.05)
    
    st.subheader("Tenure")
    c_y, c_m = st.columns(2)
    with c_y:
        years = st.number_input("Years", min_value=0, value=0)
    with c_m:
        months = st.number_input("Months", min_value=0, value=0)
    
    comp_freq = st.selectbox("Compounding Frequency", ["Monthly", "Quarterly", "Half-Yearly", "Yearly"], index=1)
    
    calculate = st.button("Calculate Now")

# logic
if calculate:
    if principal > 0 and interest_rate > 0 and (years > 0 or months > 0):
        # Compounding frequency map
        freq_map = {"Monthly": 12, "Quarterly": 4, "Half-Yearly": 2, "Yearly": 1}
        n = freq_map[comp_freq]
        t = years + (months / 12)
        r = interest_rate / 100
        
        # Formula
        m_value = principal * (1 + r/n)**(n * t)
        i_earned = m_value - principal

        # Results with better spacing
        st.write("### Summary")
        m1, m2, m3 = st.columns(3)
        m1.metric("Invested Amount", format_indian_currency(principal))
        m2.metric("Total Interest", format_indian_currency(i_earned))
        m3.metric("Maturity Value", format_indian_currency(m_value))
        
        st.divider()

        col1, col2 = st.columns([1, 1])
        with col1:
            st.write("#### Detailed Breakdown")
            data = {
                "Description": ["Principal Amount", "Rate of Interest", "Tenure", "Compounding", "Maturity Amount"],
                "Details": [
                    format_indian_currency(principal),
                    f"{interest_rate}%",
                    f"{years}y {months}m",
                    comp_freq,
                    format_indian_currency(m_value)
                ]
            }
            st.table(pd.DataFrame(data))
            
        with col2:
            st.write("#### Asset Allocation")
            chart_df = pd.DataFrame({"Label": ["Principal", "Interest"], "Value": [principal, i_earned]})
            st.bar_chart(chart_df.set_index("Label"))
    else:
        st.error("Please enter all required fields with values greater than zero.")
else:
    st.info("Input your investment details and click 'Calculate Now'.")