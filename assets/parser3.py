import json

# Загрузим содержимое файла merged_translated_words.json
with open('merged_translated_words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Преобразуем список слов в множество для удаления дубликатов
unique_data = []
seen = set()

for item in data:
    word_translation = (item['word'], item['translation'])
    if word_translation not in seen:
        unique_data.append(item)
        seen.add(word_translation)

# Запишем обновлённый список без дубликатов обратно в файл
with open('merged_translated_words_no_duplicates.json', 'w', encoding='utf-8') as f:
    json.dump(unique_data, f, ensure_ascii=False, indent=2)

print(f'Удалено {len(data) - len(unique_data)} дубликатов.')
