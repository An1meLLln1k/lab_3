import os
import json
from bs4 import BeautifulSoup

# Функция для парсинга HTML
def parse_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    products = []

    # Получаем все товары на странице
    product_items = soup.find_all("div", class_="product-item")

    for item in product_items:
        product_data = {}

        # Название товара, удаляем символы \, чтобы не было экранирования
        product_data["name"] = item.find("span").text.strip().replace("\\", "")

        # Цена товара
        price_tag = item.find("price")
        product_data["price"] = int(price_tag.text.strip().replace(" ₽", "").replace(" ", "")) if price_tag else 0

        # Характеристики
        characteristics = {}
        for li in item.find_all("li"):
            type_attr = li.get("type", "").strip()
            value = li.text.strip()
            if type_attr and value:  # добавляем только непустые характеристики
                characteristics[type_attr] = value

        product_data["characteristics"] = characteristics

        # Добавляем товар в список
        products.append(product_data)

    return products


# Получаем список всех HTML файлов в директории
directory_path = "./task_2"  # Путь к твоей директории с файлами
html_files = [f for f in os.listdir(directory_path) if f.endswith(".html")]

# Парсим все HTML файлы и собираем данные
all_products = []
for file_name in html_files:
    file_path = os.path.join(directory_path, file_name)
    products = parse_html(file_path)
    all_products.extend(products)

# Сортируем массив all_products по цене (по убыванию)
all_products_sorted = sorted(all_products, key=lambda x: x["price"], reverse=True)

# Подготовка данных для записи в JSON
output_data = {
    "all_products": all_products_sorted  # Используем строго отсортированный массив
}

# Запись данных в JSON
with open("second_task_products_results.json", "w", encoding="utf-8") as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)


