SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC;
SELECT u.last_name, u.first_name
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE (oi.price * oi.quantity) = (
    SELECT MAX(sub.total) FROM (
        SELECT SUM(oi2.price * oi2.quantity) as total 
        FROM orders o2 
        JOIN order_items oi2 ON o2.order_id = oi2.order_id 
        GROUP BY o2.order_id
    ) sub
);