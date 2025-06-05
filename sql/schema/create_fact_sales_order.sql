CREATE TABLE fact_sales_order (
    sales_record_id SERIAL PRIMARY KEY,
    sales_order_id INT NOT NULL,
    created_date date NOT NULL,
    created_time time NOT NULL,
    last_updated_date date NOT NULL,
    last_updated_time time NOT NULL,
    sales_staff_id INT NOT NULL REFERENCES dim_staff(staff_id),
    counterparty_id INT NOT NULL REFERENCES dim_counterparty(counterparty_id),
    units_sold INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    currency_id INT NOT NULL REFERENCES dim_currency(currency_id),
    design_id INT NOT NULL REFERENCES dim_design(design_id),
    agreed_payment_date date NOT NULL,
    agreed_delivery_date date NOT NULL,
    agreed_delivery_location_id INT NOT NULL REFERENCES dim_location(location_id)
);