import json
import time
from deep_translator import GoogleTranslator

words = [
    "молекула", "кислород", "углерод", "атом", "бинарный", "экзоскелет", "осциллограф", "релятивизм", "гипотенуза",
    "многочлен", "алгебра", "гранит", "вулкан", "пепел", "извержение", "равнина", "саванна", "водоём", "тайга",
    "фауна", "флора", "азимут", "декадент", "гедонизм", "парадигма", "культура", "этика", "энергия", "интеллект",
    "академия", "гуманизм", "эмоция", "менталитет", "антидот", "вакцина", "антиген", "инфекция", "иммунитет",
    "баллистика", "катапульта", "аксиома", "теорема", "апофеоз", "архаизм", "инновация", "традиция", "семантика",
    "лингвистика", "филология", "фонетика", "морфология", "синтаксис", "речь", "декларация", "дискуссия", "диалект",
    "аргумент", "реляция", "экзистенциализм", "переменная", "константа", "логарифм", "функция", "синус", "косинус",
    "интеграл", "гипербола", "парабола", "кривизна", "каркас", "расчёт", "разработка", "проект", "концепция",
    "реализация", "эксплуатация", "процессор", "транзистор", "микросхема", "резистор", "диод", "параллель", "серия",
    "магнит", "амплитуда", "вибрация", "резонанс", "энергетика", "мотор", "карбюратор", "муфта", "вал", "шестерня",
    "статор", "ротор", "шарнир", "привод", "редуктор", "цепь", "зубец", "передача", "момент", "ускорение", "инерция",
    "тензор", "корпус", "колебание", "смещение", "трансляция", "радиосигнал", "модуляция", "генератор", "аккумулятор",
    "напряжение", "сопротивление", "индукция", "конденсатор", "кондитер", "портретист", "аниматор", "философ",
    "антрополог", "генетик", "эколог", "геолог", "краевед", "микробиолог", "педагог", "астроном", "палеонтолог",
    "гидрогеолог", "синоптик", "сейсмолог", "анестезиолог", "кардиолог", "онколог", "радиолог", "уролог",
    "эпидемиолог", "законодатель", "социолог", "юрист", "картограф", "логист", "штурман", "инженер", "слесарь",
    "металлург", "радист", "машинист", "судья", "педагог", "теоретик", "наблюдатель", "маневр", "маневренность",
    "стратегия", "путь", "участок", "трасса", "маршрут", "ориентир", "безопасность", "контроль", "планирование",
    "заказ", "логика", "анализ", "интерпретация", "прогноз", "достоверность", "проверка", "подтверждение", "гипотеза",
    "опровержение", "контраргумент", "исследование", "конфигурация", "алгоритм", "прототип", "платформа",
    "клиент", "сервер", "сторона", "сервис", "мониторинг", "поддержка", "модуль", "элемент", "подсистема",
    "инфраструктура", "провайдер", "адаптация", "модификация", "перепроектирование", "ресурс", "обновление",
    "управление", "архитектура", "параметр", "настройка", "регулировка", "конфигурация", "директива",
    "модель", "функция", "система", "драйвер", "компиляция", "оптимизация", "рефакторинг", "отладка", "снижение",
    "повышение", "продуктивность", "эффективность", "приоритет", "запрос", "вычисление", "кэширование", "клиент",
    "синхронизация", "автоматизация", "инициализация", "обратимость", "повторяемость", "конверсия", "трансформация",
    "сущность", "основа", "платформа", "аргумент", "данные", "масштабирование", "нагрузка", "порог", "стабильность",
    "устойчивость", "безопасность", "перегрузка", "режим", "переход", "эмуляция", "симуляция", "проектирование",
    "тестирование", "аналитика", "исследование", "корреляция", "фактор", "подробность", "точность", "расчёт",
    "вывод", "анализатор", "маркетинг", "дистрибуция", "бизнес", "потребитель", "ценность", "товар", "доход",
    "расход", "план", "оценка", "стратегия", "цель", "показатель", "спрос", "реклама", "акция", "бренд", "доля",
    "партнёр", "конкуренция", "продукт", "сервис", "услуга", "категория", "добавка", "распределение", "вложение",
    "инвестиция", "капитал", "ликвидность", "прибыль", "убыток", "актив", "пассив", "оборот", "дивиденд", "стоимость",
    "доходность", "дебитор", "кредитор", "смета", "заём", "обязательство", "финансирование", "бюджет", "управление",
    "риск", "прибыльность", "контракт", "поставка", "переговоры", "предложение", "договор", "согласие", "гарантия",
    "система", "компонент", "сигнализация", "датчик", "контакт", "свет", "сигнал", "камера", "датчик", "реле",
    "микрофон", "передатчик", "резерв", "объект", "периметр", "защита", "уровень", "зона", "проход", "охранник",
    "пропуск", "доступ", "контроль", "информатика", "персонаж", "сюжет", "интерактивность", "анимация", "визуализация",
    "передача", "мгновение", "секундомер", "выигрыш", "проигрыш", "точка", "рейтинг", "позиция", "переход",
    "ошибка", "уровень", "медаль", "награждение", "лидер", "трофей", "персонаж", "деталь", "захват", "уничтожение",
    "победа", "поражение", "кампания", "сетевая", "трансляция", "поток", "пересылка", "достижение", "очки",
    "сетевое", "соревнование", "команда", "противник", "игрок", "сервер", "клиент", "матч", "зачёт", "раунд",
    "арена", "карта", "поле", "территория", "база", "точка", "коммуникация", "связь", "логика", "стратегия",
    "способность", "механика", "подход", "интерфейс", "функция", "сценарий", "управление", "адаптер", "коннектор",
    "программирование", "тестирование", "отладка", "методика", "повторяемость", "консоль", "версия", "обновление",
    "патч", "драйвер", "производительность", "ускорение", "технология", "картинка", "видеокарта", "частота",
    "разрешение", "динамик", "аудио", "микрофон", "плеер", "видео", "декодер", "монитор", "яркость", "контраст",
    "оптимизация", "индикация", "подключение", "схема", "режим", "поддержка", "соединение", "цикл", "модуль",
    "проект", "парадигма", "компонент", "сценарий", "репликация", "кластер", "виртуализация", "балансировка",
    "обработка", "кэширование", "ресурс", "память", "активизация", "управление", "приоритет", "распределение",
    "нагрузка", "канал", "процесс", "режим", "журнал", "хранилище", "состояние", "агрегатор", "оповещение",
    "фильтрация", "данные", "пропуск", "восстановление", "дискретизация", "сервер", "хостинг", "пакет", "интервал",
    "профилирование", "динамика", "архитектура", "доступ", "контроль", "разделение", "безопасность", "маршрут",
    "разграничение", "транзит", "локализация", "конфиденциальность", "анализатор", "лечение", "профилактика",
    "диагностика", "симптом", "синдром", "лечение", "рекомендация", "медицина", "профилактика", "офтальмология",
    "терапия", "протезирование", "диабет", "инфекция", "диагноз", "прогноз", "рентген", "лечение", "вирус",
    "распространение", "антибиотик", "анестезия", "иммунитет", "реконструкция", "восстановление", "жизнеспособность",
    "отделение", "питание", "иммунология", "психотерапия", "специализация", "психиатрия", "аллергия", "пациент",
    "операция", "стадия", "терапия", "гинекология", "реабилитация", "клиника", "кабинет", "осмотр", "консультация",
    "результат", "пластика", "трансфузия", "цитология", "урология", "бактериология", "бактерия", "биомеханика",
    "биосфера", "биология", "ботаника", "ген", "гистология", "генетика", "зоология", "вирус", "иммунология",
    "лимфоцит", "нерв", "нейробиология", "эволюция", "элементарная", "анатомия", "палеонтология", "организм",
    "орган", "ткани", "распространение", "отдел", "разделение", "клетка", "мутация", "эволюция", "приспособляемость",
    "биохимия", "экосистема", "размножение", "эколог", "микроорганизм", "экосистема", "бактерия", "инфекция",
    "возбудитель", "состав", "микроб", "образование", "переносчик", "антиген", "генетика", "код", "наследственность",
    "изменчивость", "адаптация", "механизм", "уровень", "реакция", "сигнал", "стимул", "модуляция", "адаптер",
    "коннектор", "подключение", "настройка", "данные", "конфигурация", "логика", "интерфейс", "платформа",
    "инсталляция", "пакет", "модуль", "обновление", "сигнал", "информация", "список", "пункт", "сообщение",
    "отчёт", "результат", "формат", "задача", "цикл", "синтаксис", "система", "язык", "код", "структура",
    "шаблон", "основы", "парадигма", "текст", "запрос", "сортировка", "структура", "результат", "файл", "формат",
    "доступ", "получение", "идентификация", "обновление", "криптография", "шифрование", "подключение", "метаданные",
    "метод", "реализация", "анализ", "сегмент", "модуль", "динамика", "перемещение", "объект", "активизация",
    "продуктивность", "доступ", "введение", "динамика", "восстановление", "активизация", "сервис", "обновление",
    "перезапуск", "поддержка", "логистика", "контроль", "загрузка", "производительность", "оптимизация",
    "обновление", "управление", "событие", "сегмент", "применение", "платформа", "структура", "разделение",
    "контейнер", "агрегат", "логика", "параметр", "доступ", "распределение", "модуль", "динамика", "получение",
    "реализация", "управление", "установка", "интерпретация", "настройка", "логика", "структура", "функция",
    "метод", "получение", "предназначение", "сигнализация", "интервал", "периодичность", "модуль", "введение",
    "обновление", "программирование", "структура", "метод", "параметр", "настройка", "повторяемость", "конверсия",
    "основы", "модуль", "период", "подход", "повторение", "получение", "проект", "включение", "функция",
    "оптимизация", "производительность", "сегмент", "специализация", "цикл", "передача", "адаптер", "включение",
    "состояние", "передача", "данные", "обновление", "структура", "интерфейс", "логика", "структура", "механизм",
    "анализ", "инструмент", "сегмент", "интерфейс", "параметр", "логика", "структура", "объект", "адаптер",
    "интерфейс", "структура", "функция", "обновление", "запрос", "данные", "формат", "оптимизация", "производительность",
]



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
with open("translated_words4.json", "w", encoding="utf-8") as f:
    json.dump(translated_words, f, ensure_ascii=False, indent=2)

print("Переводы успешно сохранены в translated_words.json")