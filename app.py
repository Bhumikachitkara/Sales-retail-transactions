import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Retail Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* Main Background */
.stApp{
    background-color:#FFF8F5;
}

/* Title */
.main-title{
    font-size:52px;
    font-weight:800;
    color:#FF6F61;
    text-align:center;
    margin-top:20px;
    margin-bottom:30px;
    letter-spacing:1px;
}

.sub-title{
    text-align:center;
    color:#243447;
    font-size:18px;
    margin-bottom:25px;
}

/* KPI Cards */
[data-testid="stMetric"]{
    background:white;
    border-left:8px solid #FF6F61;
    padding:18px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
}

[data-testid="stMetricValue"]{
    color:#243447 !important;
    font-weight:bold;
}

[data-testid="stMetricLabel"]{
    color:#243447 !important;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#FFE5DF;
    min-width:320px !important;
    max-width:320px !important;
}

/* Sidebar Text */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div{
    color:#243447 !important;
    font-weight:600 !important;
}

/* Sidebar Headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    color:#FF6F61 !important;
    font-weight:bold !important;
}

/* Chart Containers */
.chart-card{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom:20px;
}

/* Section Titles */
.section-title{
    font-size:26px;
    font-weight:600;
    color:#243447;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

df = pd.read_csv("PNRao_SalesRetail_Sales_Transactions.csv")
df["TotalAmount"] = pd.to_numeric(
    df["TotalAmount"],
    errors="coerce"
)
st.markdown(
    "<h1 style='text-align:center;color:#FF6F61;'>📊 Retail Sales Analytics Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center;color:#243447;'>Interactive Retail Sales Analysis & Business Insights</h4>",
    unsafe_allow_html=True
)

st.sidebar.subheader("Payment Method")

cash = st.sidebar.checkbox("Cash", value=True)
credit = st.sidebar.checkbox("Credit Card", value=True)
debit = st.sidebar.checkbox("Debit Card", value=True)
mobile = st.sidebar.checkbox("Mobile Payment", value=True)

selected_methods = []

if cash:
    selected_methods.append("Cash")
if credit:
    selected_methods.append("Credit Card")
if debit:
    selected_methods.append("Debit Card")
if mobile:
    selected_methods.append("Mobile Payment")
st.sidebar.header("🎛️ Dashboard Filters")

store_filter = st.sidebar.selectbox(
    "Store ID",
    ["All"] + list(df["StoreID"].dropna().unique())
)

amount_range = st.sidebar.slider(
    "Amount Range",
    float(df["TotalAmount"].min()),
    float(df["TotalAmount"].max()),
    (
        float(df["TotalAmount"].min()),
        float(df["TotalAmount"].max())
    )
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(
        pd.to_datetime(df["Date"], dayfirst=True).min(),
        pd.to_datetime(df["Date"], dayfirst=True).max()
    )
)

df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)

if len(date_range) == 2:
    start_date, end_date = date_range

    df = df[
        (df["Date"] >= pd.Timestamp(start_date))
        &
        (df["Date"] <= pd.Timestamp(end_date))
    ]

df_filtered = df[
    (df["TotalAmount"] >= amount_range[0])
    &
    (df["TotalAmount"] <= amount_range[1])
].copy()

if store_filter != "All":
    df_filtered = df_filtered[
        df_filtered["StoreID"] == store_filter
    ]

df_filtered = df_filtered[
    df_filtered["PaymentMethod"].isin(selected_methods)
]

df_filtered.drop_duplicates(inplace=True)

if not df_filtered.empty:
    df_filtered["PaymentMethod"] = df_filtered[
        "PaymentMethod"
    ].fillna(
        df_filtered["PaymentMethod"].mode()[0]
    )

df_filtered["TotalAmount"] = pd.to_numeric(
    df_filtered["TotalAmount"],
    errors="coerce"
)

df_filtered["TotalAmount"] = df_filtered[
    "TotalAmount"
].fillna(
    df_filtered["TotalAmount"].mean()
)

df_filtered["Date"] = pd.to_datetime(
    df_filtered["Date"],
    dayfirst=True,
    errors="coerce"
)
total_sales = df_filtered["TotalAmount"].sum()
avg_sales = df_filtered["TotalAmount"].mean()
transactions = len(df_filtered)
customers = df_filtered["CustomerID"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "💰 Total Sales",
    f"₹{total_sales:,.0f}"
)

c2.metric(
    "📊 Average Sale",
    f"₹{avg_sales:,.2f}"
)

c3.metric(
    "🧾 Transactions",
    transactions
)

c4.metric(
    "👥 Customers",
    customers
)

st.markdown("---")

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:

    payment_counts = (
        df_filtered["PaymentMethod"]
        .value_counts()
        .reset_index()
    )

    payment_counts.columns = [
        "PaymentMethod",
        "Count"
    ]

    fig_pie = px.pie(
        payment_counts,
        names="PaymentMethod",
        values="Count",
        title="Payment Method Distribution",
        color_discrete_sequence=px.colors.sequential.RdPu
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

with col2:

    fig_hist = px.histogram(
        df_filtered,
        x="TotalAmount",
        nbins=20,
        title="Total Amount Distribution",
        color_discrete_sequence=["coral"]
    )

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )
st.markdown('</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:

    top_customers = (
        df_filtered.groupby("CustomerID")
        ["TotalAmount"]
        .sum()
        .nlargest(10)
        .reset_index()
    )

    fig_customer = px.bar(
        top_customers,
        x="CustomerID",
        y="TotalAmount",
        title="Top 10 Customers",
        color="TotalAmount",
        color_continuous_scale="sunset"
    )

    st.plotly_chart(
        fig_customer,
        use_container_width=True
    )

with col4:

    store_sales = (
        df_filtered.groupby("StoreID")
        ["TotalAmount"]
        .sum()
        .reset_index()
    )

    fig_store = px.bar(
        store_sales,
        x="StoreID",
        y="TotalAmount",
        title="Store Wise Sales",
        color="TotalAmount",
        color_continuous_scale="OrRd"
    )

    st.plotly_chart(
        fig_store,
        use_container_width=True
    )

df_filtered["Month"] = (
    df_filtered["Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    df_filtered.groupby("Month")
    ["TotalAmount"]
    .sum()
    .reset_index()
)

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="TotalAmount",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)
payment_sales = (
    df_filtered.groupby("PaymentMethod")
    ["TotalAmount"]
    .sum()
    .reset_index()
)

fig_payment_sales = px.bar(
    payment_sales,
    x="PaymentMethod",
    y="TotalAmount",
    color="TotalAmount",
    title="Revenue by Payment Method"
)

st.plotly_chart(
    fig_payment_sales,
    use_container_width=True
)

st.markdown("---")

st.subheader("Data Cleaning Summary")

col5, col6 = st.columns(2)

with col5:
    st.success(
        f"""
Duplicates Removed: {df.duplicated().sum()}

Missing Values Handled Successfully
"""
    )

with col6:
    st.info(
        f"""
Records After Cleaning: {len(df_filtered)}

Columns: {df_filtered.shape[1]}
"""
    )

st.markdown("---")

st.subheader("Cleaned Dataset Preview")

st.dataframe(
    df_filtered.head(20),
    use_container_width=True
)

csv = df_filtered.to_csv(index=False)

st.download_button(
    label="📥 Download Cleaned Data",
    data=csv,
    file_name="cleaned_sales_data.csv",
    mime="text/csv"
)