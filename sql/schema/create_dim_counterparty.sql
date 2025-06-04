CREATE TABLE dim_counterparty (
    counterparty_id INT PRIMARY KEY NOT NULL,
    counterparty_legal_name VARCHAR(100) NOT NULL,
    counterparty_legal_address_line_1 VARCHAR(100) NOT NULL,
    counterparty_legal_address_line_2 VARCHAR(100),
    counterparty_legal_district VARCHAR(100),
    counterparty_legal_city VARCHAR(100) NOT NULL,
    counterparty_legal_postal_code VARCHAR(100) NOT NULL,
    counterparty_legal_country VARCHAR(100) NOT NULL,
    counterparty_legal_phone_number VARCHAR(100) NOT NULL
);