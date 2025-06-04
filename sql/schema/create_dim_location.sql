CREATE TABLE dim_location (
    location_id INT PRIMARY KEY,
    address_line_1 VARCHAR(100) NOT NULL,
    address_line_2 VARCHAR(100),
    district VARCHAR,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    phone VARCHAR(100) NOT NULL
);