CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(100) NOT NULL,
    month_name VARCHAR(100) NOT NULL,
    quarter INT NOT NULL
);