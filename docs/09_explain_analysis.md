# Отчет: День 9. Представления, индексы и анализ EXPLAIN

## 1. Созданные представления (VIEW)

Для упрощения работы с базой данных и инкапсуляции сложной логики созданы три представления:

1.  **v_orders_full**: Объединяет таблицы `orders`, `users` и `order_items`. Позволяет получить готовую строку заказа с ФИО клиента и итоговой суммой одним запросом `SELECT * FROM v_orders_full`.
2.  **v_products_with_stock**: Объединяет `products`, `stock_items` и `sizes`. Удобна для вывода каталога товаров с доступными размерами на складе.
3.  **v_user_stats**: Агрегирует данные из `users` и `orders`. Показывает статистику активности клиентов (количество заказов).

## 2. Созданные индексы (INDEX)

Для оптимизации поиска и соединений созданы следующие индексы:

| Индекс | Таблица | Поля | Назначение |
| :--- | :--- | :--- | :--- |
| `idx_products_category` | `products` | `category` | Ускорение фильтрации товаров по категориям. |
| `idx_orders_date` | `orders` | `order_date` | Ускорение сортировки заказов по времени. |
| `idx_orders_user_id` | `orders` | `user_id` | Ускорение соединения заказов с пользователями. |
| `idx_stock_product_id` | `stock_items` | `product_id` | Ускорение поиска остатков по товару. |
| `idx_stock_size_id` | `stock_items` | `size_id` | Ускорение поиска остатков по размеру. |
| `idx_products_manufacturer_cat` | `products` | `manufacturer`, `category` | **Составной индекс**. Ускоряет поиск, когда заданы и бренд, и категория. |

## 3. Анализ производительности (EXPLAIN QUERY PLAN)

### Шаг 9. Поиск по проиндексированному полю (category)
**Запрос:** `EXPLAIN QUERY PLAN SELECT * FROM products WHERE category = 'Кроссовки';`
**Результат:** `SEARCH TABLE products USING INDEX idx_products_category (category=?)`
**Вывод:** Индекс успешно используется. База данных не читает всю таблицу, а сразу находит нужные строки.

### Шаг 10. Поиск по неиндексированному полю (manufacturer)
*(Проверка до создания составного индекса)*
**Запрос:** `EXPLAIN QUERY PLAN SELECT * FROM products WHERE manufacturer = 'Nike';`
**Результат:** `SCAN TABLE products`
**Вывод:** Индекса нет, база выполняет полный перебор всех строк (Full Table Scan). Это медленно на больших объемах данных.

### Шаг 11. Анализ JOIN (соединения таблиц)
**Запрос:** `EXPLAIN QUERY PLAN SELECT * FROM orders o JOIN users u ON o.user_id = u.user_id;`
**Результат:** `SEARCH TABLE orders USING INDEX idx_orders_user_id (user_id=?)` и `SEARCH TABLE users USING INTEGER PRIMARY KEY (rowid=?)`
**Вывод:** Благодаря индексу на `orders.user_id`, соединение происходит мгновенно. База быстро находит заказы конкретного пользователя и подтягивает его данные по ID.

### Шаг 12. Общий вывод
Индексы критически важны для полей, участвующих в условиях `WHERE` и связях `JOIN`. Команда `EXPLAIN QUERY PLAN` наглядно показывает переход от медленного `SCAN` к быстрому `SEARCH`. Однако создание индекса на `manufacturer` в составе `(manufacturer, category)` не поможет, если мы ищем *только* по `category` (так как составной индекс работает слева направо). Для этого нужен отдельный индекс на `category` (создан в Шаге 5).

## 4. Проверка обновляемости представлений (Задание 14)

1.  **Простое представление:** 
    ```sql
    CREATE VIEW v_simple AS SELECT product_id, price FROM products;
    UPDATE v_simple SET price = 100 WHERE product_id = 1;
    ```
    **Результат:** Обновление прошло успешно. Так как VIEW построено на одной таблице без агрегатных функций, SQLite позволил изменить данные через него.

2.  **Сложное представление:**
    ```sql
    UPDATE v_orders_full SET total_amount = 500 WHERE order_id = 1;
    ```
    **Результат:** Ошибка: `cannot modify v_orders_full because it is a view`. 
    **Причина:** Представление содержит `JOIN` и агрегатную функцию `SUM`. СУБД не может однозначно определить, какую именно строку в таблице `order_items` нужно изменить, чтобы изменить итоговую сумму.