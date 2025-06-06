CREATE TABLE IF NOT EXISTS dim_currency (
    currency_id INT PRIMARY KEY,
    currency_code VARCHAR(10) NOT NULL,
    currency_name VARCHAR(100) NOT NULL
);

-- we need to create currency_name as it doesn't exist in currency table
-- using common table expression
WITH currency_with_names AS ( 
    SELECT 
        currency_id,
        currency_code,
        CASE currency_code
            WHEN 'GBP' THEN 'British Pound'
            WHEN 'USD' THEN 'US Dollar'
            WHEN 'EUR' THEN 'Euro'
            ELSE 'Unknown'
        END AS currency_name
    FROM currency
)
INSERT INTO dim_currency (
    currency_id,
    currency_code,
    currency_name
)
SELECT * FROM currency_with_names;