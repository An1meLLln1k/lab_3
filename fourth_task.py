import os
import json
from bs4 import BeautifulSoup
from collections import Counter
import statistics


# Функция для парсинга XML
def parse_xml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "xml")  # используем xml парсер

    items = []
    for clothing in soup.find_all("clothing"):
        item = {
            "id": int(clothing.find("id").text.strip()) if clothing.find("id") else None,
            "name": clothing.find("name").text.strip() if clothing.find("name") else "",
            "category": clothing.find("category").text.strip() if clothing.find("category") else "",
            "size": clothing.find("size").text.strip() if clothing.find("size") else "",
            "color": clothing.find("color").text.strip() if clothing.find("color") else "",
            "material": clothing.find("material").text.strip() if clothing.find("material") else "",
            "price": float(clothing.find("price").text.strip()) if clothing.find("price") else 0.0,
            "rating": float(clothing.find("rating").text.strip()) if clothing.find("rating") else 0.0,
            "reviews": int(clothing.find("reviews").text.strip()) if clothing.find("reviews") else 0,
            "new": clothing.find("new").text.strip() if clothing.find("new") else None,
            "exclusive": clothing.find("exclusive").text.strip() if clothing.find("exclusive") else None,
            "sporty": clothing.find("sporty").text.strip() if clothing.find("sporty") else None,
        }
        items.append(item)
    return items


# Получаем список всех XML файлов
directory_path = "./task_4"  # Путь к директории с файлами
xml_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith(".xml")]

# Парсим все XML файлы
all_items = []
for file_path in xml_files:
    all_items.extend(parse_xml(file_path))

# 1. Сортировка данных по цене
sorted_items = sorted(all_items, key=lambda x: x["price"], reverse=True)

# 2. Фильтрация данных: товары с рейтингом выше 4.0
filtered_items = [item for item in all_items if item["rating"] > 4.0]

# 3. Статистические характеристики для цены
prices = [item["price"] for item in all_items]
statistics_data = {
    "total_price": sum(prices),
    "min_price": min(prices),
    "max_price": max(prices),
    "average_price": statistics.mean(prices) if prices else 0
}

# 4. Частота категорий
categories = [item["category"] for item in all_items]
category_frequency = dict(Counter(categories))

# Подготовка данных для JSON
output_data = {
    "all_items": sorted_items,
    "filtered_items": filtered_items,
    "statistics": statistics_data,
    "category_frequency": category_frequency
}

# Проверяем сортировку данных по цене
sorted_check = all(output_data["all_items"][i]["price"] >= output_data["all_items"][i + 1]["price"]
                   for i in range(len(output_data["all_items"]) - 1))

if not sorted_check:
    print("Данные не отсортированы. Пересортировываю...")
    # Если данные не отсортированы, пересортируем по цене
    output_data["all_items"] = sorted(output_data["all_items"], key=lambda x: x["price"], reverse=True)

    # Перезаписываем отсортированные данные в новый JSON файл
    with open('clothing_items_results_sorted.json', 'w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)

    print("Данные отсортированы и сохранены в 'clothing_items_results_sorted.json'.")
else:
    print("Данные уже отсортированы.")

# Запись итоговых данных в JSON
with open("fourth_task_clothing_items_results.json", "w", encoding="utf-8") as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)


