import streamlit as st
import pandas as pd
import psycopg2

# Streamlit page config
st.set_page_config(page_title="Sales Dashboard", layout="centered")

st.title("📊 Sales Dashboard")
st.subheader("Total Sales per Month")

# Database connection
def get_connection():
    return psycopg2.connect(
        host="nc-data-eng-project-dw-prod.chpsczt8h1nu.eu-west-2.rds.amazonaws.com",
        port="5432",
        dbname="postgres",
        user="project_team_00",
        password="FjV2ZJGkirQ4Oh7"
    )

# Query
# Total sales per month 
# calculate total sales = units_sold × unit_price
# grouping by year and  month_name
# grouping by dim_date.month to sort correctly
# query = """
#     SELECT
#         dim_date.year,
#         dim_date.month_name,
#         SUM(fact_sales_order.units_sold * fact_sales_order.unit_price) AS total_sales
#     FROM fact_sales_order
#     JOIN dim_date
#         ON make_date(dim_date.year, dim_date.month, dim_date.day) = fact_sales_order.created_date
#     GROUP BY dim_date.year, dim_date.month, dim_date.month_name
#     ORDER BY dim_date.year, dim_date.month;    
# """
query = """
    SELECT
        TO_CHAR(created_date, 'YYYY-MM') AS month,
        SUM(units_sold * unit_price) AS total_sales
    FROM fact_sales_order
    GROUP BY TO_CHAR(created_date, 'YYYY-MM')
    ORDER BY month;
"""

# Get data
try:
    with get_connection() as conn:
        df = pd.read_sql(query, conn)
except Exception as e:
    st.error(f"Failed to load data: {e}")
else:
    # Show table
    st.dataframe(df)

    # Show chart
    st.line_chart(df.set_index("month"))

