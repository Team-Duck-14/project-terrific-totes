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

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📅 Sales per Month", "🧑‍💼 Sales by Staff", "🎨 Sales by Design", "📍 Sales by Location", "💷 Sales by Currency", "🧑‍🤝‍🧑 Top Customers"])

# --- Tab 1: Sales per Month ---
with tab1:
    st.subheader("Total Sales per Month")

    # Query - fix this when I have time, otherwise use below one

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
    
    # Sorting options ?
    sort_option = st.selectbox(
        "Sort by:",
        options=["Month (Ascending)", "Sales (Descending)", "Sales (Ascending)"]
    )
    if sort_option == "Month (Ascending)":
        order_by = "month ASC"
    elif sort_option == "Sales (Descending)":
        order_by = "total_sales DESC"
    else:  # Sales (Ascending)
        order_by = "total_sales ASC"

    query = f"""
        SELECT
            TO_CHAR(created_date, 'YYYY-MM') AS month,
            SUM(units_sold * unit_price) AS total_sales
        FROM fact_sales_order
        GROUP BY TO_CHAR(created_date, 'YYYY-MM')
        ORDER BY {order_by};
    """
    try:
        with get_connection() as conn:
            df = pd.read_sql(query, conn)
        st.dataframe(df.style.format({"total_sales": "{:,.2f}"}))
        st.line_chart(df.set_index("month"))
    except Exception as e:
        st.error(f"Failed to load data: {e}")

# --- Tab 2: Sales by Staff ---
with tab2:
    st.subheader("Total Sales by Staff Member")
    query = """
        SELECT CONCAT(dim_staff.first_name, ' ', dim_staff.last_name) AS full_name,
        dim_staff.department_name,
        dim_staff.location,
               SUM(fact_sales_order.units_sold * fact_sales_order.unit_price) AS total_sales
        FROM fact_sales_order
        JOIN dim_staff ON fact_sales_order.sales_staff_id = dim_staff.staff_id
        GROUP BY dim_staff.first_name, dim_staff.last_name, dim_staff.department_name, dim_staff.location
        ORDER BY total_sales DESC;
    """
    try:
        with get_connection() as conn:
            df = pd.read_sql(query, conn)
        # st.dataframe(df)
        # st.bar_chart(df.set_index("full_name")["total_sales"])
        
        # Get unique departments including "All"
        departments = ["All"] + sorted(df["department_name"].unique().tolist())
        selected_dept = st.selectbox("Choose department", departments)

        # Filter based on selection
        if selected_dept == "All":
            filtered_df = df
        else:
            filtered_df = df[df["department_name"] == selected_dept]

        st.dataframe(filtered_df.style.format({"total_sales": "{:,.2f}"}))

        # Bar chart
        st.bar_chart(filtered_df.set_index("full_name")["total_sales"])
    
    except Exception as e:
        st.error(f"Failed to load data: {e}")

# --- Tab 3: Sales by Design ---
with tab3:
    st.subheader("Total Sales by Design")
    query = """
        SELECT dim_design.design_name,
               SUM(fact_sales_order.units_sold * fact_sales_order.unit_price) AS total_sales
        FROM fact_sales_order
        JOIN dim_design ON fact_sales_order.design_id = dim_design.design_id
        GROUP BY dim_design.design_name
        ORDER BY total_sales DESC;
    """
    try:
        with get_connection() as conn:
            df = pd.read_sql(query, conn)
        st.dataframe(df.style.format({"total_sales": "{:,.2f}"}))
        st.bar_chart(df.set_index("design_name"))
    except Exception as e:
        st.error(f"Failed to load data: {e}")

# --- Tab 4: Sales by Location ---
with tab4:
    st.subheader("Total Sales by Location")
    query = """
        SELECT 
            CASE 
                WHEN dim_staff.location ILIKE 'Leds' THEN 'Leeds'
                ELSE dim_staff.location
            END AS location,
            SUM(fact_sales_order.units_sold * fact_sales_order.unit_price) AS total_sales
        FROM fact_sales_order
        JOIN dim_staff ON fact_sales_order.sales_staff_id = dim_staff.staff_id
        GROUP BY 
            CASE 
        WHEN dim_staff.location ILIKE 'Leds' THEN 'Leeds'
        ELSE dim_staff.location
            END
        ORDER BY total_sales DESC;
    """
    try:
        with get_connection() as conn:
            df = pd.read_sql(query, conn)
        st.dataframe(df.style.format({"total_sales": "{:,.2f}"}))
        st.bar_chart(df.set_index("location"))
    except Exception as e:
        st.error(f"Failed to load data: {e}")

# --- Tab 5: Sales by Currency ---
with tab5:
    st.subheader("Total Sales by Currency")
    query = """
        SELECT dim_currency.currency_code,
            SUM(fact_sales_order.units_sold * fact_sales_order.unit_price) AS total_sales
        FROM fact_sales_order
        JOIN dim_currency ON fact_sales_order.currency_id = dim_currency.currency_id
        GROUP BY dim_currency.currency_code
        ORDER BY total_sales DESC;
    """
    try:
        with get_connection() as conn:
            df = pd.read_sql(query, conn)
        st.dataframe(df.style.format({"total_sales": "{:,.2f}"}))
        st.bar_chart(df.set_index("currency_code"))
    except Exception as e:
        st.error(f"Failed to load data: {e}")

# --- Tab 6: Top counterparties (customers) ---
with tab6:
    st.subheader("Top 10 Customers by Total Sales")
    query = """
        SELECT 
            dim_counterparty.counterparty_legal_name AS top_customer,
            SUM(fact_sales_order.units_sold * fact_sales_order.unit_price) AS total_sales
        FROM fact_sales_order
        JOIN dim_counterparty 
            ON fact_sales_order.counterparty_id = dim_counterparty.counterparty_id
        GROUP BY dim_counterparty.counterparty_legal_name
        ORDER BY total_sales DESC
        LIMIT 10;
    """
    try:
        with get_connection() as conn:
            df = pd.read_sql(query, conn)
        st.dataframe(df.style.format({"total_sales": "{:,.2f}"}))
        st.bar_chart(df.set_index("top_customer"))
    except Exception as e:
        st.error(f"Failed to load data: {e}")


