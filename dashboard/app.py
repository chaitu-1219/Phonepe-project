import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="PhonePe Insights", layout="wide")

st.title("📊 PhonePe Transaction Insights Dashboard")

# -------------------------
# DB Connection
# -------------------------
@st.cache_data
def load_data():
    conn = sqlite3.connect("data/phonepe.db")

    trans = pd.read_sql("SELECT * FROM aggregated_transaction", conn)
    users = pd.read_sql("SELECT * FROM user_data", conn)
    ins = pd.read_sql("SELECT * FROM insurance_data", conn)

    conn.close()
    return trans, users, ins

df, user_df, ins_df = load_data()

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("🔍 Filters")

state = st.sidebar.selectbox("Select State", df["state"].unique())
year = st.sidebar.selectbox("Select Year", sorted(df["year"].unique()))

filtered_df = df[(df["state"] == state) & (df["year"] == year)]

# -------------------------
# KPI Section
# -------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Amount", f"{filtered_df['amount'].sum():,.0f}")
col2.metric("Total Transactions", f"{filtered_df['count'].sum():,.0f}")
col3.metric("Avg Transaction", f"{filtered_df['amount'].mean():,.0f}")

# -------------------------
# Tabs
# -------------------------
tab1, tab2, tab3 = st.tabs(["💳 Transactions", "📱 Users", "🛡 Insurance"])

# =========================
# TAB 1: TRANSACTIONS
# =========================
with tab1:

    st.subheader("Transaction Type Distribution")

    type_df = filtered_df.groupby("type")["amount"].sum().reset_index()

    fig1 = px.bar(type_df, x="type", y="amount", color="type")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Year-wise Growth")

    year_df = df.groupby("year")["amount"].sum().reset_index()

    fig2 = px.line(year_df, x="year", y="amount", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Top 10 States")

    state_df = df.groupby("state")["amount"].sum().reset_index()\
        .sort_values(by="amount", ascending=False).head(10)

    fig3 = px.bar(state_df, x="state", y="amount", color="amount")
    st.plotly_chart(fig3, use_container_width=True)

# =========================
# TAB 2: USERS
# =========================
with tab2:

    st.subheader("Top Device Brands")

    brand_df = user_df.groupby("brand")["registeredUsers"].sum().reset_index()\
        .sort_values(by="registeredUsers", ascending=False).head(10)

    fig4 = px.bar(brand_df, x="brand", y="registeredUsers", color="brand")
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("User Growth Over Years")

    user_growth = user_df.groupby("year")["registeredUsers"].sum().reset_index()

    fig5 = px.line(user_growth, x="year", y="registeredUsers", markers=True)
    st.plotly_chart(fig5, use_container_width=True)

# =========================
# TAB 3: INSURANCE
# =========================
with tab3:

    st.subheader("Insurance Growth")

    ins_growth = ins_df.groupby("year")["amount"].sum().reset_index()

    fig6 = px.line(ins_growth, x="year", y="amount", markers=True)
    st.plotly_chart(fig6, use_container_width=True)

    st.subheader("Top States (Insurance)")

    ins_state = ins_df.groupby("state")["amount"].sum().reset_index()\
        .sort_values(by="amount", ascending=False).head(10)

    fig7 = px.bar(ins_state, x="state", y="amount", color="amount")
    st.plotly_chart(fig7, use_container_width=True)

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.write("🚀 Developed by ponna chaitanya")