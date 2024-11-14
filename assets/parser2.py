import json

# Пути к исходным файлам
files = ['translated_words.json', 'translated_words2.json', 'translated_words3.json', 'translated_words4.json']

# Список для хранения всех словарных пар
all_words = []

# Чтение и объединение данных из каждого файла
for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_words.extend(data)  # Добавляем данные из файла в общий список
    except FileNotFoundError:
        print(f"Файл {file} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка при чтении данных из файла {file}.")

# Сохранение объединенных данных в новый JSON файл
with open('merged_translated_words.json', 'w', encoding='utf-8') as outfile:
    json.dump(all_words, outfile, ensure_ascii=False, indent=2)

print("Все файлы объединены в merged_translated_words.json")
