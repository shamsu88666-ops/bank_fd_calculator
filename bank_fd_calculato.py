import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="FD Return Calculator", page_icon="🏦", layout="centered")

# Custom CSS for Mobile Friendly UI
st.markdown("""
    <style>
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 20px;
    }
    [data-testid="stMetricValue"] {
        font-size: 24px !important;
    }
    .stButton > button {
        width: 100%;
        background-color: #2E5BFF;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    /* Mobile friendly adjustments */
    @media (max-width: 640px) {
        [data-testid="stMetricValue"] {
            font-size: 20px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

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

st.markdown('<p class="main-header">FD Return Calculator</p>', unsafe_allow_html=True)

# Main Screen Inputs (No Sidebar for better mobile visibility)
st.subheader("Investment Details")
principal = st.number_input("Principal Amount (₹)", min_value=0, value=0, step=1000)

col_r, col_f = st.columns(2)
with col_r:
    interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, value=0.0, step=0.1)
with col_f:
    comp_freq = st.selectbox("Compounding", ["Monthly", "Quarterly", "Half-Yearly", "Yearly"], index=1)

st.write("**Tenure**")
c_y, c_m = st.columns(2)
with c_y:
    years = st.number_input("Years", min_value=0, value=0)
with c_m:
    months = st.number_input("Months", min_value=0, value=0)

calculate = st.button("Calculate Now")

if calculate:
    if principal > 0 and interest_rate > 0 and (years > 0 or months > 0):
        freq_map = {"Monthly": 12, "Quarterly": 4, "Half-Yearly": 2, "Yearly": 1}
        n = freq_map[comp_freq]
        t = years + (months / 12)
        r = interest_rate / 100
        
        m_value = principal * (1 + r/n)**(n * t)
        i_earned = m_value - principal

        st.divider()
        st.write("### Summary")
        m1, m2, m3 = st.columns(3)
        m1.metric("Invested", format_indian_currency(principal))
        m2.metric("Interest", format_indian_currency(i_earned))
        m3.metric("Maturity", format_indian_currency(m_value))
        
        st.divider()
        st.write("#### Growth Analysis")
        chart_df = pd.DataFrame({"Label": ["Principal", "Interest"], "Value": [principal, i_earned]})
        st.bar_chart(chart_df.set_index("Label"))
        
        st.table(pd.DataFrame({
            "Description": ["Maturity Amount", "Compounding"],
            "Details": [format_indian_currency(m_value), comp_freq]
        }))
    else:
        st.error("Please fill all fields.")
else:
    st.info("Fill the details and click 'Calculate Now'.")
