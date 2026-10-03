import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='ME')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

# Addition 1
selected_category = st.selectbox("Select a Category", df["Category"].unique())
# Addition 2
available_subcategories = df[df["Category"] == selected_category]["Sub_Category"].unique()
selected_subcategories = st.multiselect("Select Sub-Category", available_subcategories)
# Addition 3
filtered = df[(df["Category"] == selected_category) & (df["Sub_Category"].isin(selected_subcategories))].groupby(pd.Grouper(freq='ME')).sum()
st.line_chart(filtered, y="Sales")
# Addition 4
st.metric(label = "Total Sales", value = filtered["Sales"].sum())
st.metric(label = "Total Profit", value = filtered["Profit"].sum())
st.metric(label = "Overall Profit Margin (%)", value = round(filtered["Profit"].sum() / filtered["Sales"].sum() * 100, 2), 
# Addition 5
          delta = round(df["Profit"].sum() / df["Sales"].sum() * 100 - filtered["Profit"].sum() / filtered["Sales"].sum() * 100, 2))

