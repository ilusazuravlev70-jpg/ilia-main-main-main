-- =============================================
-- БЛОК 1. Триггеры на обновление и логирование
-- =============================================

-- 1.1. Триггер аудита для изменения цен (только если цена реально изменилась)
CREATE TRIGGER IF NOT EXISTS trg_audit_price_update
AFTER UPDATE ON products
WHEN OLD.price != NEW.price
BEGIN
    INSERT INTO audit_log (table_name, operation, record_id, old_value, new_value)
    VALUES ('products', 'UPDATE', OLD.product_id, 
            printf('Цена: %.2f', OLD.price), 
            printf('Цена: %.2f', NEW.price));
END;

-- 1.2. Триггер аудита для удаления заказов
CREATE TRIGGER IF NOT EXISTS trg_audit_order_delete
AFTER DELETE ON orders
BEGIN
    INSERT INTO audit_log (table_name, operation, record_id, old_value)
    VALUES ('orders', 'DELETE', OLD.order_id, 'Заказ полностью удален');
END;

-- 1.3. Триггер автоматического обновления поля updated_at
CREATE TRIGGER IF NOT EXISTS trg_update_timestamp
AFTER UPDATE ON users
BEGIN
    UPDATE users 
    SET updated_at = datetime('now') 
    WHERE user_id = OLD.user_id;
END;


-- =============================================
-- БЛОК 2. Триггеры на вставку и бизнес-логику
-- =============================================

-- 2.1. Триггер автоматического списания остатков
CREATE TRIGGER IF NOT EXISTS trg_update_stock_after_insert
AFTER INSERT ON order_items
BEGIN
    UPDATE stock_items 
    SET quantity_available = quantity_available - NEW.quantity 
    WHERE stock_item_id = NEW.stock_item_id;
END;

-- 2.2. Триггер-защита: запрет удаления пользователя с заказами
CREATE TRIGGER IF NOT EXISTS trg_protect_user_delete
BEFORE DELETE ON users
BEGIN
    SELECT CASE 
        WHEN (SELECT COUNT(*) FROM orders WHERE user_id = OLD.user_id) > 0 
        THEN RAISE(ABORT, 'Нельзя удалить пользователя с активными заказами') 
    END;
END;

-- 2.3. Триггер проверки: запрет отрицательного количества на складе
CREATE TRIGGER IF NOT EXISTS trg_check_stock_quantity
BEFORE INSERT ON stock_items
WHEN NEW.quantity_available < 0
BEGIN
    SELECT RAISE(ABORT, 'Количество не может быть отрицательным');
END;

-- (Опционально) Триггер проверки при обновлении остатков
CREATE TRIGGER IF NOT EXISTS trg_check_stock_quantity_update
BEFORE UPDATE ON stock_items
WHEN NEW.quantity_available < 0
BEGIN
    SELECT RAISE(ABORT, 'Количество не может быть отрицательным');
END;