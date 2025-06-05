CREATE TABLE dim_currency (
    currency_id INT PRIMARY KEY,
    currency_code VARCHAR(10) NOT NULL,
    currency_name VARCHAR(100) NOT NULL
);