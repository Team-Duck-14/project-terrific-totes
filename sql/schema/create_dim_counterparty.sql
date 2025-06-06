CREATE TABLE IF NOT EXISTS dim_counterparty (
    counterparty_id INT PRIMARY KEY,
    counterparty_legal_name VARCHAR(100) NOT NULL,
    counterparty_legal_address_line_1 VARCHAR(100) NOT NULL,
    counterparty_legal_address_line_2 VARCHAR(100),
    counterparty_legal_district VARCHAR(100),
    counterparty_legal_city VARCHAR(100) NOT NULL,
    counterparty_legal_postal_code VARCHAR(100) NOT NULL,
    counterparty_legal_country VARCHAR(100) NOT NULL,
    counterparty_legal_phone_number VARCHAR(100) NOT NULL
);

INSERT INTO dim_counterparty (
    counterparty_id,
    counterparty_legal_name,
    counterparty_legal_address_line_1,
    counterparty_legal_address_line_2,
    counterparty_legal_district,
    counterparty_legal_city,
    counterparty_legal_postal_code,
    counterparty_legal_country,
    counterparty_legal_phone_number
)
-- we need to use aliases to rename the columns as we need
SELECT DISTINCT
    counterparty.counterparty_id,
    counterparty.counterparty_legal_name,
    address.address_line_1 AS counterparty_legal_address_line_1,
    address.address_line_2 AS counterparty_legal_address_line_2,
    address.district AS counterparty_legal_district,
    address.city AS counterparty_legal_city,
    address.postal_code AS counterparty_legal_postal_code,
    address.country AS counterparty_legal_country,
    address.phone AS counterparty_legal_phone_number
FROM counterparty
JOIN address ON counterparty.legal_address_id = address.address_id;