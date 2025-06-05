CREATE TABLE dim_staff (
    staff_id INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    email_address VARCHAR(100) NOT NULL
);
