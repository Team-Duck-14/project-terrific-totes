CREATE TABLE IF NOT EXISTS dim_location (
    location_id INT PRIMARY KEY,
    address_line_1 VARCHAR(100) NOT NULL,
    address_line_2 VARCHAR(100),
    district VARCHAR (100),
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    phone VARCHAR(100) NOT NULL
);

INSERT INTO dim_location (
    location_id,
    address_line_1,
    address_line_2,
    district,
    city,
    postal_code,
    country,
    phone
)
SELECT DISTINCT
    address_id AS location_id,
    address_line_1,
    address_line_2,
    district,
    city,
    postal_code,
    country,
    phone
FROM address;