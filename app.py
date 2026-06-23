import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Sales Data Cleaning Dashboard")

df = pd.read_csv('PNRao_SalesRetail_Sales_Transactions.csv')
st.sidebar.header("Filters")

payment_filter = st.sidebar.multiselect(
    "Select Payment Method",
    options=df["PaymentMethod"].dropna().unique(),
    default=df["PaymentMethod"].dropna().unique()
)

store_filter = st.sidebar.multiselect(
    "Select Store ID",
    options=df["StoreID"].dropna().unique(),
    default=df["StoreID"].dropna().unique()
)

col1, col2, col3 = st.columns(3)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())
st.header("Original Dataset")
st.dataframe(df.head())

st.header("Dataset Shape")
st.write("Rows:", df.shape[0])
st.write("Columns:", df.shape[1])

st.header("Missing Values")
st.write(df.isnull().sum())

st.header("Duplicate Records")
st.write(df.duplicated().sum())

df_filtered = df[
    (df["PaymentMethod"].isin(payment_filter)) &
    (df["StoreID"].isin(store_filter))
].copy()

df_filtered.drop_duplicates(inplace=True)

df_filtered['PaymentMethod'] = df_filtered['PaymentMethod'].fillna(
    df_filtered['PaymentMethod'].mode()[0]
)

df_filtered['TotalAmount'] = pd.to_numeric(
    df_filtered['TotalAmount'],
    errors='coerce'
)

df_filtered['TotalAmount'] = df_filtered['TotalAmount'].fillna(
    df_filtered['TotalAmount'].mean()
)

st.header("Cleaned Dataset")
st.dataframe(df_filtered.head())

st.header("Missing Values After Cleaning")
st.write(df_filtered.isnull().sum())

st.header("Payment Method Distribution")

fig, ax = plt.subplots()
sns.countplot(data=df_filtered, x='PaymentMethod', ax=ax)
plt.xticks(rotation=45)

st.pyplot(fig)

st.header("Total Amount Distribution")

fig2, ax2 = plt.subplots()
sns.histplot(df_filtered['TotalAmount'], bins=20, ax=ax2)

st.pyplot(fig2)

st.header("Top 10 Customers")

top_customers = df_filtered.groupby(
    'CustomerID'
)['TotalAmount'].sum().nlargest(10).reset_index()

fig3, ax3 = plt.subplots(figsize=(10,5))

sns.barplot(
    data=top_customers,
    x='CustomerID',
    y='TotalAmount',
    ax=ax3
)

plt.xticks(rotation=45)

st.pyplot(fig3)

st.header("Store Wise Sales")

store_sales = df_filtered.groupby(
    'StoreID'
)['TotalAmount'].sum().reset_index()

fig4, ax4 = plt.subplots(figsize=(8,5))

sns.barplot(
    data=store_sales,
    x='StoreID',
    y='TotalAmount',
    ax=ax4
)

st.pyplot(fig4)

st.header("Sales Distribution")

fig5, ax5 = plt.subplots(figsize=(8,5))

sns.boxplot(
    y=df_filtered['TotalAmount'],
    ax=ax5
)

st.pyplot(fig5)

df_filtered['Date'] = pd.to_datetime(
    df_filtered['Date'],
    dayfirst=True,
    errors='coerce'
)