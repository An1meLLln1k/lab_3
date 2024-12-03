import os
import json
from bs4 import BeautifulSoup
import statistics
from collections import Counter
import re

# Список известных брендов для поиска в названии товара
known_brands = ["Nike", "ANTA", "Puma", "Adidas", "Jordan"]


# Функция для извлечения бренда из названия
def extract_brand(name):
    for brand in known_brands:
        if brand.lower() in name.lower():  # Ищем бренд в названии товара
            return brand
    return None  # Если бренд не найден, возвращаем None


# Функция для парсинга HTML
def parse_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    products = []

    # Находим все товары на странице
    product_items = soup.find_all("div", class_="pv-item scp-item")

    for item in product_items:
        product_data = {}

        # Название товара
        name_tag = item.find("a", class_="link-pv-name")
        if name_tag:
            name = name_tag.text.strip()
            product_data["name"] = name

            # Извлекаем бренд из названия товара
            product_data["brand"] = extract_brand(name)

        # Цена товара (обрабатываем строку с пробелами и "руб.")
        price_tag = item.find("div", class_="price-wrap")
        if price_tag:
            price_text = price_tag.text.strip()
            # Убираем пробелы и "руб."
            price_cleaned = price_text.replace("₽", "").replace("руб.", "").replace(" ", "").strip()
            try:
                product_data["price"] = float(price_cleaned)
            except ValueError:
                product_data["price"] = None  # В случае ошибки, если цена не может быть преобразована

        # Добавляем товар в список
        products.append(product_data)

    return products


# Путь к файлам с HTML
directory_path = "./task_5"  # Папка с HTML-файлами

# Считываем все файлы
html_files = [f for f in os.listdir(directory_path) if f.endswith(".html")]

all_products = []
for file_name in html_files:
    file_path = os.path.join(directory_path, file_name)
    products = parse_html(file_path)
    all_products.extend(products)

# 1. Сортировка по цене (если цена не None)
sorted_products = sorted(all_products, key=lambda x: x["price"] if x["price"] is not None else float('inf'))

# 2. Фильтрация: товары с определённым брендом (например, Nike)
filtered_products = [product for product in all_products if product.get("brand") == "Nike"]

# 3. Статистические характеристики для цен
prices = [product["price"] for product in all_products if product["price"] is not None]
total_price = sum(prices)
min_price = min(prices) if prices else 0
max_price = max(prices) if prices else 0
average_price = statistics.mean(prices) if prices else 0

# 4. Частота брендов
brands = [product["brand"] for product in all_products if product.get("brand")]
brand_counts = Counter(brands)

# Выводим бренды для отладки
print("Бренды товаров:")
for product in all_products[:10]:  # Выводим первые 10 товаров для отладки
    print(f"{product['name']}: {product.get('brand')}")

# Подготовка данных для записи в JSON
output_data = {
    "all_products": all_products,
    "sorted_products": sorted_products,
    "filtered_products": filtered_products,
    "statistics": {
        "total_price": total_price,
        "min_price": min_price,
        "max_price": max_price,
        "average_price": average_price
    },
    "brand_frequency": brand_counts
}

# Запись данных в JSON
output_file = "fifth_task_products_results.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)


