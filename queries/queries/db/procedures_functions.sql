-- Задание 3.1. Функция для суммы заказа (PostgreSQL)
CREATE OR REPLACE FUNCTION calc_total_pg(price NUMERIC, quantity INTEGER)
RETURNS NUMERIC AS $$
BEGIN
    RETURN price * quantity;
END;
$$ LANGUAGE plpgsql;

-- Задание 3.2. Процедура создания заказа (PostgreSQL)
CREATE OR REPLACE PROCEDURE create_order_pg(
    p_user_id INTEGER, 
    p_stock_item_id INTEGER, 
    p_qty INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_price NUMERIC;
BEGIN
    -- Проверка остатка
    SELECT quantity_available INTO v_price FROM stock_items WHERE stock_item_id = p_stock_item_id;
    IF v_price < p_qty THEN
        RAISE NOTICE 'Недостаточно товара на складе!';
        RETURN;
    END IF;

    -- Вставка в orders
    INSERT INTO orders (order_date, user_id) 
    VALUES (CURRENT_DATE, p_user_id);
    
    -- Получение ID заказа и цены
    -- (В реальном коде здесь была бы логика получения price)
    
    -- Вставка в order_items
    -- INSERT INTO order_items (order_id, stock_item_id, quantity, price) ...;
    
    -- Обновление остатков
    -- UPDATE stock_items SET quantity_available = quantity_available - p_qty ...;
    
    RAISE NOTICE 'Заказ успешно создан';
END;
$$;

-- Задание 3.3. Процедура с обработкой ошибок (EXCEPTION)
CREATE OR PROCEDURE safe_update_stock(p_stock_item_id INTEGER, p_qty INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE stock_items 
    SET quantity_available = quantity_available - p_qty 
    WHERE stock_item_id = p_stock_item_id;

    IF NOT FOUND THEN
        RAISE NOTICE 'Товарная позиция не найдена';
        RETURN;
    END IF;

    -- Проверка на минус
    IF (SELECT quantity_available FROM stock_items WHERE stock_item_id = p_stock_item_id) < 0 THEN
        RAISE EXCEPTION 'Ошибка: Остаток не может быть отрицательным';
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Произошла непредвиденная ошибка: %', SQLERRM;
END;
$$;