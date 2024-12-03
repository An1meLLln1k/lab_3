import os
import json
from bs4 import BeautifulSoup
from collections import Counter
import statistics


# Функция для парсинга HTML
def parse_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    tournament_data = {}
    tournament_data["type"] = soup.find("span").text.strip().replace("Тип:", "").strip()
    tournament_data["title"] = soup.find("h1", class_="title").text.strip().replace("Турнир:", "").strip()
    tournament_data["city"] = soup.find("p", class_="address-p").text.split("Начало:")[0].replace("Город:", "").strip()
    tournament_data["start_date"] = soup.find("p", class_="address-p").text.split("Начало:")[1].strip()

    # Извлекаем информацию о турнире
    info = soup.find_all("span")
    tournament_data["rounds"] = int(info[1].text.replace("Количество туров:", "").strip())
    tournament_data["time_control"] = info[2].text.replace("Контроль времени:", "").strip()
    tournament_data["min_rating"] = int(info[3].text.replace("Минимальный рейтинг для участия:", "").strip())

    # Рейтинг и просмотры
    tournament_data["rating"] = float(soup.find_all("span")[-2].text.replace("Рейтинг:", "").strip())
    tournament_data["views"] = int(soup.find_all("span")[-1].text.replace("Просмотры:", "").strip())

    # Изображение турнира
    tournament_data["image"] = soup.find("img")["src"]

    return tournament_data


# Получаем список всех HTML файлов в директории
directory_path = "./task_1"  # Путь к твоей директории с файлами
html_files = [f for f in os.listdir(directory_path) if f.endswith(".html")]

# Парсим все HTML файлы и собираем данные
all_tournaments = []
for file_name in html_files:
    file_path = os.path.join(directory_path, file_name)
    tournament = parse_html(file_path)
    all_tournaments.append(tournament)

# Выполняем операции

# 1. Сортировка данных по рейтингу
sorted_tournaments = sorted(all_tournaments, key=lambda x: x["rating"], reverse=True)

# 2. Фильтрация данных: турниры с рейтингом больше 2.0
filtered_tournaments = [t for t in all_tournaments if t["rating"] > 2.0]

# 3. Статистические характеристики для числового поля (например, рейтинг)
ratings = [t["rating"] for t in all_tournaments]
total_rating = sum(ratings)
min_rating = min(ratings)
max_rating = max(ratings)
average_rating = statistics.mean(ratings)

# 4. Частота меток для текстового поля (например, "Тип")
types = [t["type"] for t in all_tournaments]
type_counts = Counter(types)

# Запись данных в JSON
output_data = {
    "all_tournaments": all_tournaments,
    "sorted_tournaments": sorted_tournaments,
    "filtered_tournaments": filtered_tournaments,
    "statistics": {
        "total_rating": total_rating,
        "min_rating": min_rating,
        "max_rating": max_rating,
        "average_rating": average_rating
    },
    "type_frequency": type_counts
}

with open("first_task_tournaments_results.json", "w", encoding="utf-8") as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)

