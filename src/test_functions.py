from app_functions import calc_discount, pluralize_items, format_full_name, get_client_tier

def test_calc_discount():
    assert calc_discount(1000, 10) == 900.0
    assert calc_discount(1000, 0) == 1000.0
    assert calc_discount(1000, 100) == 0.0
    assert calc_discount(1000, -5) == 1000.0
    assert calc_discount(1000, 150) == 0.0
    assert calc_discount(None, 10) == 0.0
    print("test_calc_discount: OK")

def test_pluralize_items():
    assert pluralize_items(1) == "1 товар"
    assert pluralize_items(2) == "2 товара"
    assert pluralize_items(5) == "5 товаров"
    assert pluralize_items(21) == "21 товар"
    assert pluralize_items(22) == "22 товара"
    assert pluralize_items(11) == "11 товаров"
    assert pluralize_items(0) == "0 товаров"
    assert pluralize_items(None) == "0 товаров"
    print("test_pluralize_items: OK")

def test_format_full_name():
    assert format_full_name("иванов", "иван", "иванович") == "Иванов И.И."
    assert format_full_name("иванов", "иван", None) == "Иванов И."
    assert format_full_name("", "иван", "иванович") == "Аноним"
    assert format_full_name("  петров  ", "  петр  ", "  ") == "Петров П."
    print("test_format_full_name: OK")

def test_client_tier():
    assert get_client_tier(1000) == "Новичок"
    assert get_client_tier(5000) == "Бронза"
    assert get_client_tier(25000) == "Серебро"
    assert get_client_tier(75000) == "Золото"
    assert get_client_tier(150000) == "Платина"
    assert get_client_tier(None) == "Без статуса"
    print("test_client_tier: OK")

if __name__ == "__main__":
    test_calc_discount()
    test_pluralize_items()
    test_format_full_name()
    test_client_tier()
    print("\nВсе тесты пройдены успешно.")