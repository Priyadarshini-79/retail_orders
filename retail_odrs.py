#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to MySQL Database
db_connection = mysql.connector.connect(
    host="127.0.0.1",        
    user="root",        
    password="Mahe@1970", 
    database="retail_orders"
)

# Function to execute SQL query and return a DataFrame
def get_data(query):
    return pd.read_sql(query, db_connection)

# Queries
top_products_query = """
SELECT product_id, SUM(list_price * quantity) AS total_revenue
FROM orders
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT 10;
"""
top_cities_query = """
SELECT city, SUM(profit) AS total_profit
FROM orders
GROUP BY city
ORDER BY total_profit DESC
LIMIT 5;
"""
discount_by_category_query = """
SELECT category, SUM(discount_percent) AS total_discount
FROM orders
GROUP BY category;
"""
avg_sale_price_query = """
SELECT category, AVG(list_price) AS average_sale_price
FROM orders
GROUP BY category;
"""
highest_avg_sale_region_query = """
SELECT region, AVG(list_price) AS average_sale_price
FROM orders
GROUP BY region
ORDER BY average_sale_price DESC
LIMIT 1;
"""
total_profit_by_category_query = """
SELECT category, SUM(profit) AS total_profit
FROM orders
GROUP BY category;
"""
top_segments_query = """
SELECT segment, SUM(quantity) AS total_quantity
FROM orders
GROUP BY segment
ORDER BY total_quantity DESC
LIMIT 3;
"""
avg_discount_region_query = """
SELECT region, AVG(discount_percent) AS average_discount_percentage
FROM orders
GROUP BY region;
"""
top_profit_category_query = """
SELECT category, SUM(profit) AS total_profit
FROM orders
GROUP BY category
ORDER BY total_profit DESC
LIMIT 1;
"""
total_revenue_per_year_query = """
SELECT YEAR(order_date) AS year, SUM(list_price * quantity) AS total_revenue
FROM orders
GROUP BY YEAR(order_date);
"""

# Fetch Data
df1 = get_data(top_products_query)
df2 = get_data(top_cities_query)
df3 = get_data(discount_by_category_query)
df4 = get_data(avg_sale_price_query)
df5 = get_data(highest_avg_sale_region_query)
df6 = get_data(total_profit_by_category_query)
df7 = get_data(top_segments_query)
df8 = get_data(avg_discount_region_query)
df9 = get_data(top_profit_category_query)
df10 = get_data(total_revenue_per_year_query)

# Streamlit App
st.title("Retail Order Data Analysis")

# Display each query result with its respective visualization
st.subheader("Top 10 Highest Revenue Generating Products")
st.dataframe(df1)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='product_id', y='total_revenue', data=df1, ax=ax, palette="Blues_r")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
ax.set_xlabel("Product ID")
ax.set_ylabel("Total Revenue")
ax.set_title("Top 10 Highest Revenue Generating Products")
st.pyplot(fig)

st.subheader("Top 5 Cities with Highest Profit Margins")
st.dataframe(df2)
fig, ax = plt.subplots()
sns.barplot(x='city', y='total_profit', data=df2, ax=ax)
ax.set_xlabel("City")
ax.set_ylabel("Total Profit")
ax.set_title("Top 5 Cities with Highest Profit Margins")
st.pyplot(fig)

st.subheader("Total Discount Given for Each Category")
st.dataframe(df3)
fig, ax = plt.subplots()
ax.pie(df3["total_discount"], labels=df3["category"], autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
ax.axis("equal")
st.pyplot(fig)

st.subheader("Average Sale Price per Product Category")
st.dataframe(df4)
fig, ax = plt.subplots()
sns.barplot(x='category', y='average_sale_price', data=df4, ax=ax)
ax.set_xlabel("Category")
ax.set_ylabel("Average Sale Price")
ax.set_title("Average Sale Price per Product Category")
st.pyplot(fig)

st.subheader("Region with Highest Average Sale Price")
st.dataframe(df5)
fig, ax = plt.subplots()
sns.barplot(x='region', y='average_sale_price', data=df5, ax=ax)
ax.set_xlabel("Region")
ax.set_ylabel("Average Sale Price")
ax.set_title("Region with Highest Average Sale Price")
st.pyplot(fig)

st.subheader("Total Profit per Category")
st.dataframe(df6)
fig, ax = plt.subplots()
ax.pie(df6["total_profit"], labels=df6["category"], autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
ax.axis("equal")
st.pyplot(fig)

st.subheader("Top 3 Segments with Highest Quantity of Orders")
st.dataframe(df7)
fig, ax = plt.subplots()
sns.barplot(x='segment', y='total_quantity', data=df7, ax=ax)
ax.set_xlabel("Segment")
ax.set_ylabel("Total Quantity")
ax.set_title("Top 3 Segments with Highest Quantity of Orders")
st.pyplot(fig)

st.subheader("Average Discount Percentage per Region")
st.dataframe(df8)
fig, ax = plt.subplots()
sns.boxplot(x='region', y='average_discount_percentage', data=df8, ax=ax)
ax.set_xlabel("Region")
ax.set_ylabel("Average Discount Percentage")
ax.set_title("Distribution of Discount Percentage per Region")
st.pyplot(fig)

st.subheader("Product Category with Highest Total Profit")
st.dataframe(df9)
fig, ax = plt.subplots()
ax.pie(df9["total_profit"], labels=df9["category"], autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
ax.axis("equal")
st.pyplot(fig)

st.subheader("Total Revenue Generated per Year")
st.dataframe(df10)
fig, ax = plt.subplots()
sns.lineplot(x='year', y='total_revenue', data=df10, marker='o', ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Total Revenue")
ax.set_title("Total Revenue Generated per Year")
st.pyplot(fig)

# Close database connection
db_connection.close()

