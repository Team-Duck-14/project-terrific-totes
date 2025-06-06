CREATE TABLE IF NOT EXISTS dim_date (
    date_id INT PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INT NOT NULL
);

-- as we have several date names in other tables we need to 
-- collect all data from source tables and combine them
-- using Common Table Expression to UNION all the disticnct dates
WITH all_dates AS (
    SELECT agreed_delivery_date AS date FROM sales_order
    UNION
    SELECT agreed_payment_date FROM sales_order
    UNION
    SELECT agreed_delivery_date FROM purchase_order
    UNION
    SELECT agreed_payment_date FROM purchase_order
    UNION
    SELECT payment_date FROM payment
    -- should we be adding created/updated dates from all tables? if yes need to do this for all tables:
    -- UNION
    -- SELECT created_at FROM department
    -- UNION
    -- SELECT last_updated FROM department
)
INSERT INTO dim_date (
    date_id,
    year,
    month,
    day,
    day_of_week,
    day_name,
    month_name,
    quarter
)
SELECT DISTINCT
    CAST(TO_CHAR(date, 'YYYYMMDD') AS INT) AS date_id, -- to give unique id
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,
    EXTRACT(DAY FROM date) AS day,
    EXTRACT(DOW FROM date) AS day_of_week,
    TRIM(TO_CHAR(date, 'Day')) AS day_name, -- trim to remove trailing spaces
    TRIM(TO_CHAR(date, 'Month')) AS month_name,
    EXTRACT(QUARTER FROM date) AS quarter
FROM all_dates
WHERE date IS NOT NULL;