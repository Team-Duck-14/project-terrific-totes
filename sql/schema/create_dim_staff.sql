CREATE TABLE IF NOT EXISTS dim_staff (
    staff_id INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    email_address VARCHAR(100) NOT NULL
);

INSERT INTO dim_staff (
    staff_id,
    first_name,
    last_name,
    department_name,
    location,
    email_address
)
SELECT DISTINCT
    staff.staff_id,
    staff.first_name,
    staff.last_name,
    department.department_name,
    department.location,
    staff.email_address
FROM staff
JOIN department ON staff.department_id = department.department_id;

-- 1. Create and populate dimension tables
-- 2. Create and populate fact table