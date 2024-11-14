import json

# Список файлов для обработки
files = [
    'assets/words.json',
    'merged_translated_words_no_duplicates.json'
]

# Функция для подсчета пар слов
def count_word_pairs(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Проверим, что каждый элемент в файле имеет структуру {'word': 'some_word', 'translation': 'some_translation'}
            valid_pairs = [item for item in data if isinstance(item, dict) and 'word' in item and 'translation' in item]
            print(f"Содержимое {file_name}:")
            print(valid_pairs[:5])  # Выводим первые 5 валидных пар для проверки
            return len(valid_pairs)
    except FileNotFoundError:
        print(f"Файл {file_name} не найден.")
        return 0
    except json.JSONDecodeError:
        print(f"Ошибка при чтении JSON в файле {file_name}.")
        return 0

# Подсчитываем количество валидных пар слов в каждом файле
for file in files:
    count = count_word_pairs(file)
    print(f"Количество пар слов в {file}: {count}")
