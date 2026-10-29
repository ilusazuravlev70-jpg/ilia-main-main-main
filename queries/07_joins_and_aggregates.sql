-- Задание 1, Запрос 1
SELECT o.order_id, u.last_name FROM orders o INNER JOIN users u ON o.user_id = u.user_id;

-- Задание 2, Запрос 8
SELECT SUM(quantity * price) FROM order_items;

-- Задание 5, Запрос 19 (средний чек)
SELECT AVG(order_total) FROM (SELECT SUM(quantity * price) as order_total FROM order_items GROUP BY order_id) sub;