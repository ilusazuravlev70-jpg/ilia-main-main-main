-- =============================================
-- ЗАДАНИЕ 1. Создание представлений (VIEW)
-- =============================================

-- VIEW 1: Полная информация о заказах
-- Объединяет заказы, пользователей и считает сумму позиций
CREATE VIEW IF NOT EXISTS v_orders_full AS
SELECT 
    o.order_id,
    o.order_date,
    (u.last_name || ' ' || u.first_name || COALESCE(' ' || u.middle_name, '')) AS full_name,
    SUM(oi.quantity * oi.price) AS total_amount
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date, u.user_id;

-- VIEW 2: Товары с остатками на складе
-- Объединяет товары, размеры и остатки
CREATE VIEW IF NOT EXISTS v_products_with_stock AS
SELECT 
    p.product_name,
    p.price,
    s.size_value,
    si.quantity_available
FROM products p
JOIN stock_items si ON p.product_id = si.product_id
JOIN sizes s ON si.size_id = s.size_id;

-- VIEW 3: Статистика по клиентам
-- Показывает количество заказов для каждого пользователя
CREATE VIEW IF NOT EXISTS v_user_stats AS
SELECT 
    u.user_id,
    (u.last_name || ' ' || u.first_name || COALESCE(' ' || u.middle_name, '')) AS full_name,
    u.login,
    COUNT(o.order_id) AS orders_count
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id;


-- =============================================
-- ЗАДАНИЕ 2. Создание индексов (INDEX)
-- =============================================

-- Шаг 5: Обычный индекс на категорию товаров (для фильтрации)
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);

-- Шаг 6: Индекс на дату заказа (для сортировки)
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);

-- Шаг 7: Индексы на внешние ключи (ускорение JOIN)
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_stock_product_id ON stock_items(product_id);
CREATE INDEX IF NOT EXISTS idx_stock_size_id ON stock_items(size_id);

-- Шаг 8: Составной индекс (на два поля)
-- Логично искать товары конкретного бренда в конкретной категории
CREATE INDEX IF NOT EXISTS idx_products_manufacturer_cat ON products(manufacturer, category);