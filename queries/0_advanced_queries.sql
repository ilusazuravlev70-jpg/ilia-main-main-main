-- 1. Цена со скидкой 20%
SELECT product_name, price, CALC_DISCOUNT(price, 20) AS price_with_discount
FROM products;

-- 2. ФИО клиентов без отчества (используя функцию)
SELECT FORMAT_FULL_NAME(last_name, first_name, middle_name) AS full_name
FROM users;

-- 3. Количество товара с правильным склонением
SELECT oi.quantity, PLURALIZE_ITEMS(oi.quantity) as item_word
FROM order_items oi;

-- 4. Сумма заказа клиента со скидкой 10%
SELECT 
    FORMAT_FULL_NAME(u.last_name, u.first_name, u.middle_name) AS client_name,
    SUM(oi.quantity * CALC_DISCOUNT(oi.price, 10)) AS total_with_discount
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id;

-- 5. Аналитика: уровень клиента и стаж (использует функции, зарегистрированные в Python)
SELECT 
    FORMAT_FULL_NAME(u.last_name, u.first_name, u.middle_name) AS full_name,
    SUM(oi.quantity * oi.price) AS total_spent,
    GET_CLIENT_TIER(SUM(oi.quantity * oi.price)) AS tier,
    MIN(o.order_date) AS first_order_date,
    GET_LOYALTY_DAYS(MIN(o.order_date)) AS loyalty_days
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id
ORDER BY total_spent DESC;