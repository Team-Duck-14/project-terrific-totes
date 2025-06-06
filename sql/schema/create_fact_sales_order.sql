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

INSERT INTO fact_sales_order (
    sales_order_id,
    created_date,
    created_time,
    last_updated_date,
    last_updated_time,
    sales_staff_id,
    counterparty_id,
    units_sold,
    unit_price,
    currency_id,
    design_id,
    agreed_payment_date,
    agreed_delivery_date,
    agreed_delivery_location_id
)
SELECT
    sales_order.sales_order_id,
    CAST(sales_order.created_at AS DATE) AS created_date,
    CAST(sales_order.created_at AS TIME) AS created_time,
    CAST(sales_order.last_updated AS DATE) AS last_updated_date,
    CAST(sales_order.last_updated AS TIME) AS last_updated_time,    
    dim_staff.staff_id AS sales_staff_id,
    dim_counterparty.counterparty_id,
    sales_order.units_sold,
    sales_order.unit_price,
    dim_currency.currency_id,
    dim_design.design_id,
    sales_order.agreed_payment_date,
    sales_order.agreed_delivery_date,
    dim_location.location_id AS agreed_delivery_location_id
FROM
    sales_order
JOIN dim_counterparty ON sales_order.counterparty_id = dim_counterparty.counterparty_id
JOIN dim_currency ON sales_order.currency_id = dim_currency.currency_id
JOIN dim_staff ON sales_order.staff_id = dim_staff.staff_id
JOIN dim_design ON sales_order.design_id = dim_design.design_id
JOIN dim_location ON sales_order.agreed_delivery_location_id = dim_location.location_id;