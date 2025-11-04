import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Consumer Complaints Dashboard", layout="wide")

st.title("📊 Consumer Complaints Analysis Dashboard")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_excel("Consumer_Complaints.xlsx")
    dictionary = pd.read_csv("ConsumerComplaints_DataDictionary.csv")
    return df, dictionary

df, dictionary = load_data()

st.sidebar.header("📁 Data Overview")
if st.sidebar.checkbox("Show raw data"):
    st.dataframe(df)

if st.sidebar.checkbox("Show data dictionary"):
    st.dataframe(dictionary)

st.sidebar.header("🔍 Filters")

# --- Filter Options ---
if 'State' in df.columns:
    states = st.sidebar.multiselect("Select State(s)", sorted(df['State'].dropna().unique()))
    if states:
        df = df[df['State'].isin(states)]

if 'Product' in df.columns:
    products = st.sidebar.multiselect("Select Product(s)", sorted(df['Product'].dropna().unique()))
    if products:
        df = df[df['Product'].isin(products)]

if 'Company' in df.columns:
    companies = st.sidebar.multiselect("Select Company", sorted(df['Company'].dropna().unique()))
    if companies:
        df = df[df['Company'].isin(companies)]

# --- Summary Statistics ---
st.subheader("📈 Dataset Summary")
st.write(df.describe(include='all'))

# --- Visualizations ---
st.subheader("📊 Visualizations")

tab1, tab2, tab3, tab4 = st.tabs(["Complaints by Product", "Complaints by State", "Response Timelines", "Top Companies"])

with tab1:
    if 'Product' in df.columns:
        st.write("### Number of Complaints by Product")
        product_counts = df['Product'].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=product_counts.values, y=product_counts.index, ax=ax)
        st.pyplot(fig)

with tab2:
    if 'State' in df.columns:
        st.write("### Complaints by State")
        state_counts = df['State'].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=state_counts.values, y=state_counts.index, ax=ax)
        st.pyplot(fig)

with tab3:
    if 'Date received' in df.columns:
        st.write("### Complaints Over Time")
        df['Date received'] = pd.to_datetime(df['Date received'], errors='coerce')
        time_counts = df.groupby(df['Date received'].dt.to_period('M')).size()
        fig, ax = plt.subplots()
        time_counts.plot(ax=ax)
        plt.title("Complaints Over Time")
        st.pyplot(fig)

with tab4:
    if 'Company' in df.columns:
        st.write("### Top 10 Companies with Most Complaints")
        comp_counts = df['Company'].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=comp_counts.values, y=comp_counts.index, ax=ax)
        st.pyplot(fig)

# --- Correlation Heatmap ---
if st.checkbox("Show Correlation Heatmap (numeric columns)"):
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    if not numeric_df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No numeric columns found for correlation heatmap.")

# --- Footer ---
st.markdown("---")
st.markdown("📘 *Dashboard built using Streamlit by Bhakti Tambe*")
