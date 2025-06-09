import pandas as pd

def transform_dim_staff(staff_df, department_df):

    """
    Transforms staff and department data into the dim_staff star schema table.

    Args:
        staff_df (pd.DataFrame): DataFrame containing staff data
        department_df (pd.DataFrame): DataFrame containing department data

    Returns:
        pd.DataFrame: Transformed dim_staff DataFrame
    """

    # Merge staff with department on department_id
    merged_df = pd.merge(
        staff_df,
        department_df,
        how="inner",
        on="department_id"
    )
    # Select required columns
    dim_staff_df = merged_df[[
        "staff_id",
        "first_name",
        "last_name",
        "department_name",
        "location",
        "email_address"
    ]]
    # Drop duplicate rows just in case
    return dim_staff_df.drop_duplicates()

def transform_dim_counterparty(counterparty_df, address_df):
    """
    Transforms counterparty and address data into the dim_counterparty star schema table.

    Args:
        counterparty_df (pd.DataFrame): DataFrame containing counterparty data
        address_df (pd.DataFrame): DataFrame containing address data

    Returns:
        pd.DataFrame: Transformed dim_counterparty DataFrame
    """
    # Merge counterparty with address on address_id
    merged_df = pd.merge(
        counterparty_df, 
        address_df,
        how="inner",
        left_on="legal_address_id",
        right_on="address_id"
    )
    # Select required columns
    dim_counterparty_df = merged_df[[
        "counterparty_id",
        "counterparty_legal_name",
        "address_line_1",
        "address_line_2",
        "district",
        "city",
        "postal_code",
        "country",
        "phone"
    ]].rename(columns={
        "address_line_1": "counterparty_legal_address_line_1",
        "address_line_2": "counterparty_legal_address_line_2",
        "district": "counterparty_legal_district",
        "city": "counterparty_legal_city",
        "postal_code": "counterparty_legal_postal_code",
        "country": "counterparty_legal_country",
        "phone": "counterparty_legal_phone_number"
    })
    return dim_counterparty_df.drop_duplicates()

def transform_dim_currency(currency_df):
    """
    Transforms currency data into the dim_currency star schema table,
    mapping currency_code to human-readable currency_name.

    Args:
        currency_df (pd.DataFrame): DataFrame containing currency data

    Returns:
        pd.DataFrame: Transformed dim_currency DataFrame
    """

    # Map currency codes to names
    currency_name_map = {
        "GBP": "British Pound",
        "USD": "US Dollar",
        "EUR": "Euro"
    }

    currency_df["currency_name"] = currency_df["currency_code"].map(
        currency_name_map
    ).fillna("Unknown")

    # Select and return the final schema
    dim_currency_df = currency_df[[
        "currency_id",
        "currency_code",
        "currency_name"
    ]]

    return dim_currency_df.drop_duplicates()

def transform_dim_date(sales_order_df, purchase_order_df, payment_df):
    """
    Transforms dates from multiple source tables into a date dimension table.

    Args:
        sales_order_df (pd.DataFrame): DataFrame with sales orders
        purchase_order_df (pd.DataFrame): DataFrame with purchase orders
        payment_df (pd.DataFrame): DataFrame with payments

    Returns:
        pd.DataFrame: Transformed dim_date DataFrame
    """
    # Collect relevant date columns
    date_cols = [
        sales_order_df["agreed_delivery_date"],
        sales_order_df["agreed_payment_date"],
        purchase_order_df["agreed_delivery_date"],
        purchase_order_df["agreed_payment_date"],
        payment_df["payment_date"],
    ]

    # Combine into a single Series
    all_dates = pd.concat(date_cols, ignore_index=True).dropna().drop_duplicates()

    # Convert to datetime just in case
    all_dates = pd.to_datetime(all_dates)

    # Build the dim_date DataFrame
    dim_date_df = pd.DataFrame({
            "date": all_dates
        })

    dim_date_df["date_id"] = dim_date_df["date"].dt.strftime("%Y%m%d").astype(int)
    dim_date_df["year"] = dim_date_df["date"].dt.year
    dim_date_df["month"] = dim_date_df["date"].dt.month
    dim_date_df["day"] = dim_date_df["date"].dt.day
    dim_date_df["day_of_week"] = dim_date_df["date"].dt.weekday  # Monday=0
    dim_date_df["day_name"] = dim_date_df["date"].dt.day_name()
    dim_date_df["month_name"] = dim_date_df["date"].dt.month_name()
    dim_date_df["quarter"] = dim_date_df["date"].dt.quarter

    return dim_date_df[[
        "date_id",
        "year",
        "month",
        "day",
        "day_of_week",
        "day_name",
        "month_name",
        "quarter"
    ]].drop_duplicates()

def transform_dim_design(design_df):
    """
    Transforms the design table into dim_design star schema format.

    Args:
        design_df (pd.DataFrame): DataFrame containing design data

    Returns:
        pd.DataFrame: Transformed dim_design DataFrame
    """
    dim_design_df = design_df[[
        "design_id",
        "design_name",
        "file_location",
        "file_name"
    ]].drop_duplicates()

    return dim_design_df

def transform_dim_location(location_df):

    location_df = location_df.rename(columns={"address_id": "location_id"})

    dim_location_df = location_df[[
        "location_id",
        "address_line_1",
        "address_line_2",
        "district",
        "city",
        "postal_code",
        "country",
        "phone"
    ]].drop_duplicates()

    return dim_location_df

def transform_fact_sales_order(sales_order_df):
    # Extract date and time from datetime fields
    sales_order_df["created_date"] = pd.to_datetime(sales_order_df["created_at"]).dt.date
    sales_order_df["created_time"] = pd.to_datetime(sales_order_df["created_at"]).dt.time
    sales_order_df["last_updated_date"] = pd.to_datetime(sales_order_df["last_updated"]).dt.date
    sales_order_df["last_updated_time"] = pd.to_datetime(sales_order_df["last_updated"]).dt.time

    # Rename staff_id to match fact table naming convention
    sales_order_df = sales_order_df.rename(columns={
        "staff_id": "sales_staff_id",
        "agreed_delivery_location_id": "agreed_delivery_location_id"
    })

    # Select required columns
    fact_sales_order_df = sales_order_df[[
        "sales_order_id",
        "created_date",
        "created_time",
        "last_updated_date",
        "last_updated_time",
        "sales_staff_id",
        "counterparty_id",
        "units_sold",
        "unit_price",
        "currency_id",
        "design_id",
        "agreed_payment_date",
        "agreed_delivery_date",
        "agreed_delivery_location_id"
    ]].drop_duplicates()

    return fact_sales_order_df
