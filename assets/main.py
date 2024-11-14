import json
import time
from deep_translator import GoogleTranslator

words = []

# Пустой список для хранения слов и переводов
translated_words = []

# Функция перевода с обработкой ошибок
def translate_word(word):
    try:
        # Переводим слово с помощью deep-translator
        translation = GoogleTranslator(source='ru', target='en').translate(word)
        return translation
    except Exception as e:
        print(f"Ошибка при переводе слова '{word}': {e}")
        return None

# Переводим слова с паузами для стабильности
for word in words:
    translation = translate_word(word)
    if translation:
        translated_words.append({
            "word": word,
            "translation": translation
        })

# Сохраняем результат в JSON файл
with open("translated_words3.json", "w", encoding="utf-8") as f:
    json.dump(translated_words, f, ensure_ascii=False, indent=2)

print("Переводы успешно сохранены в translated_words.json")
