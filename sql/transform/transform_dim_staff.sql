-- might be unnecessary - check
SELECT 
    staff.staff_id,
    staff.first_name,
    staff.last_name,
    department.department_name,
    department.location,
    staff.email_address
FROM
    staff
LEFT JOIN
    department
ON staff.department_id = department.department_id;