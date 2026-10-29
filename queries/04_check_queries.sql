SELECT * FROM roles;
SELECT u.last_name, u.first_name, r.role_name FROM users u JOIN roles r ON u.role_id = r.role_id;
SELECT * FROM products;