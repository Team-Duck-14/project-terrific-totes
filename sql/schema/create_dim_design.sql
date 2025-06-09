CREATE TABLE IF NOT EXISTS dim_design (
    design_id INT PRIMARY KEY,
    design_name VARCHAR(100) NOT NULL,
    file_location VARCHAR(100) NOT NULL,
    file_name VARCHAR(100) NOT NULL
);

INSERT INTO dim_design (
    design_id,
    design_name,
    file_location,
    file_name
)
SELECT DISTINCT
    design_id,
    design_name,
    file_location,
    file_name
FROM design;