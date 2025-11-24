
import pandas as pd
import streamlit as st
import plotly.express as px


df = pd.read_csv("Skill Test Data.csv")
df.columns = [c.strip() for c in df.columns]


st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Dashboard")


cities = st.sidebar.multiselect("Filter by City", options=df['city'].unique(), default=df['city'].unique())
products = st.sidebar.multiselect("Filter by Product", options=df['product_purchased'].unique(), default=df['product_purchased'].unique())
channels = st.sidebar.multiselect("Filter by Marketing Channel", options=df['marketing_channel'].unique(), default=df['marketing_channel'].unique())


df_filtered = df[(df['city'].isin(cities)) & (df['product_purchased'].isin(products)) & (df['marketing_channel'].isin(channels))]


total_orders = df_filtered['order_no'].nunique()
total_qty = df_filtered['qty_purchased'].sum()

col1, col2 = st.columns(2)
col1.metric("Total Orders", total_orders)
col2.metric("Total Quantity Purchased", total_qty)

st.markdown("---")


top_cities = df_filtered.groupby('city')['order_no'].nunique().sort_values(ascending=False).head(5).reset_index()
fig_cities = px.bar(top_cities, x='city', y='order_no', title='Top 5 Cities by Orders', color='city')
st.plotly_chart(fig_cities, use_container_width=True)


top_products = df_filtered.groupby('product_purchased')['qty_purchased'].sum().sort_values(ascending=False).head(5).reset_index()
fig_products = px.pie(top_products, names='product_purchased', values='qty_purchased', title='Top 5 Products by Quantity')
st.plotly_chart(fig_products, use_container_width=True)


channel_perf = df_filtered.groupby('marketing_channel').agg({'order_no':'nunique','qty_purchased':'sum'}).reset_index()
fig_channels = px.bar(channel_perf, x='marketing_channel', y='order_no', title='Marketing Channel Performance', color='marketing_channel')
st.plotly_chart(fig_channels, use_container_width=True)

st.markdown("---")


st.subheader("City-wise Breakdown")
st.dataframe(df_filtered.groupby('city').agg({'order_no':'nunique','qty_purchased':'sum'}).reset_index())

st.subheader("Product-wise Breakdown")
st.dataframe(df_filtered.groupby('product_purchased')
             .agg({'order_no':'nunique','qty_purchased':'sum'})
             .reset_index())
