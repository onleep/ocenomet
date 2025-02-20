# Отчёт по проекту

## 1. Введение

### Сервис предсказания стоимости недвижимости в Москве

Цель проекта — разработать систему предсказания стоимости недвижимости в Москве с использованием методов машинного обучения. Основные задачи:

- Достичь высокой точности прогнозирования стоимости объектов недвижимости.
- Реализовать интеграцию с Telegram-ботом для удобного взаимодействия с пользователями.

Пользователь может получить прогноз, указав ключевые характеристики объекта: площадь, количество комнат, местоположение и другие параметры.

---

## 2. Команда проекта

- **Куратор:** Александр Чуприн — tg: @Chew13
- **Участник 1:** Антон Кузьмин — tg: @onleepa, GitHub: [onleep](https://github.com/onleep)
- **Участник 2:** Семён Черемисин — tg: @samhook, GitHub: [krabat7](https://github.com/krabat7)
- **Участник 3:** Алексей Урсулян — tg: @GreatPopka, GitHub: [GreatPopka](https://github.com/GreatPopka)
- **Участник 4:** Георгий Лавренов — tg: @goga1899, GitHub: [glavrenov124](https://github.com/glavrenov124)

---

## 3. Описание набора данных

В репозитории содержится несколько файлов, описывающих структуру данных по недвижимости:

- **dataset.md**: Описание структуры данных и информация о наборе данных, включающем ключевые параметры объектов недвижимости, такие как площадь, количество комнат, местоположение и прочие атрибуты.
- **EDA.md**: Выводы и описание работы над этапами разведочного анализа данных (EDA). Этот файл содержит описание подходов к обработке и предварительному анализу данных, включая выявление закономерностей и очистку данных.
- **ocenomet_eda.ipynb**: Основной файл с EDA. Ноутбук включает графики, таблицы и ключевые статистические метрики, которые помогают понять структуру и распределение данных.
- **correlation_matrix.html**: Корреляционная матрица всего датасета, показывающая взаимосвязи между основными характеристиками объектов недвижимости. Этот файл удобен для визуализации и анализа сильных и слабых корреляций между параметрами.
- **model.ipynb**: Ноутбук для построения и обучения модели машинного обучения. Включает этапы подготовки данных, настройку гиперпараметров и оценку качества модели.
- **model.md**: Документация модели, описание её и параметров. Здесь содержится информация о подходе к выбору модели, использовании алгоритмов и их применении к данным.
- **model.pickle**: Сериализованная модель в формате pickle для дальнейшего использования. Позволяет быстро загружать обученную модель в любом проекте, где она может быть полезной.
- **devcontainer.json**: Файл конфигурации DevContainer для настройки окружения разработки, что облегчает работу с проектом в контейнерах.
- **fastapi.py**: Скрипт, реализующий API на базе FastAPI, для взаимодействия с пользователем и предоставления функционала предсказания стоимости недвижимости.
- **models.py**: Модуль, содержащий модели данных и структуры, используемые в проекте.
- **preprocess.py**: Файл, содержащий функции предобработки данных, такие как заполнение пропусков, нормализация и преобразование категориальных признаков.
- **database.py**: Модуль для работы с базой данных, включая подключение, выполнение запросов и управление таблицами.
- **main.py**: Основной файл приложения, запускающий Streamlit-приложение для взаимодействия с пользователем.
- **tools.py**: Утилитарные функции для обработки данных и логики приложения.
- **validate_page.py**: Модуль, отвечающий за валидацию данных на страницах приложения.
- **update.sh**: Скрипт для автоматического обновления проекта, включая получение последних изменений из репозитория и перезапуск сервисов.

---

## 4. Структура базы данных

- **addresses:** Информация об адресах объектов недвижимости.
- **developers:** Данные о застройщиках.
- **offers:** Информация о предложениях по недвижимости.
- **offers_details:** Детализированная информация об объявлениях продажи недвижимости.
- **realty_details:** Детализированная информация о недвижимости.
- **realty_inside:** Внутренние характеристики объектов недвижимости.
- **realty_outside:** Внешние характеристики объектов недвижимости.

---


## 5. Виртуальный сервер (ВПС)

В рамках проекта был развернут ВПС, который выполняет следующие задачи:

1. **Установка и настройка инфраструктуры**:
   - На сервере была развернута база данных.
   - Установлены все зависимости, необходимые для работы проекта.

2. **Деплой проекта**:
   - Загружена копия проекта из репозитория GitHub.
   - Настроено окружение для запуска приложений.

3. **Запуск парсера**:
   - Парсер запускается на сервере для автоматического сбора данных с ЦИАН.
   - Собранные данные сохраняются в базе данных для последующего анализа.

4. **Запуск API**:
   - Запущен API на базе Streamlit, обеспечивающий доступ к функционалу предсказания стоимости.
   - Сервер доступен по публичному IP-адресу.

5. **Обеспечение доступности**:
   - ВПС работает круглосуточно, обеспечивая стабильную работу всех компонентов проекта.

**Преимущества использования ВПС:**
- Автономная работа всех модулей проекта.
- Доступность для пользователей в любое время.
- Возможность масштабирования и добавления новых функций.

## 6. Работа парсера

Парсер в проекте предназначен для автоматического сбора данных с платформы ЦИАН. Он выполняет следующие функции:

1. Отправка запросов на страницы ЦИАН:
   - Парсер использует ссылки на объявления, чтобы отправлять HTTP-запросы к API или веб-страницам ЦИАН.

2. Скачивание и распаковка данных:
   - После получения ответа от сервера ЦИАН парсер извлекает JSON-данные из ответа.
   - JSON-данные распаковываются и преобразуются в читаемый формат, подходящий для анализа и обработки.

3. Добавление данных в базу:
   - Распакованные данные структурируются и добавляются в базу данных.
   - Парсер обрабатывает ключевые параметры объекта недвижимости, такие как:
     - Площадь
     - Количество комнат
     - Цена
     - Расположение
     - Дополнительные параметры (этаж, год постройки, состояние ремонта и т.д.).

4. Работа с прокси-серверами:
   - Парсер использует 10–15 прокси-серверов для распределения нагрузки и обхода ограничений платформы ЦИАН.
   - Каждый прокси отправляет запросы с интервалом в 10 секунд, чтобы снизить вероятность блокировок.

5. Обработка ошибок и банов:
   - Если прокси получает бан или капчу, он временно исключается из работы:
     - При первом случае отдыхают 2 минуты.
     - Если после возвращения ошибка повторяется, прокси отдыхает уже 5 минут.
   - Эта система позволяет минимизировать риски длительной блокировки всех прокси-серверов.

6. Гибкость и устойчивость:
   - Парсер автоматически адаптируется к изменениям структуры страниц и API, обновляя правила обработки данных.
   - Обеспечивается стабильная работа даже при изменениях на стороне ЦИАН благодаря многопоточности и использованию ротации прокси.

---

### Пример алгоритма работы парсера

1. Отправить запрос на страницу объявления через один из доступных прокси.
2. Проверить статус ответа:
   - Если запрос успешен (код 200), извлечь JSON-данные.
   - Если ошибка (например, капча), отключить текущий прокси на 2 минуты.
3. Распаковать JSON-данные, выделить необходимые параметры.
4. Добавить данные в базу.
5. Повторить процесс для следующей ссылки.

---

### Преимущества подхода

- Устойчивость к блокировкам: Использование ротации прокси снижает вероятность массового бана.
- Автоматизация: Все процессы происходят без вмешательства человека, что позволяет собирать большие объемы данных.
- Обновляемость данных: Регулярные запросы обеспечивают актуальную информацию о рынке недвижимости.

## 7. Функционал API и пример использования

### 7.1. Получение параметров объекта недвижимости

Для получения параметров объекта из объявления на ЦИАН отправляется запрос:
```
GET /getparams?url=<ссылка-на-объект>
```

где `url` — ссылка на страницу объекта на платформе ЦИАН.

**Пример кода (Python):**

```python
import httpx

url = 'https://www.cian.ru/sale/flat/294517249/'
getparams = httpx.get('http://<server-address>/api/getparams', params={'url': url}, timeout=120)

print(getparams.status_code)
print(getparams.json())
```

**Пример результата запроса:**

```
200
{
    "cian_id": 294517249,
    "deal_type": "sale",
    "flat_type": "rooms",
    "description": "Продаётся видовая квартира (выходит на 3 стороны) в минуте хотьбы от м.Юго-Западная, в современном монолитно-кирпичном доме...",
    "total_area": 67.0,
    "living_area": 35.0,
    "kitchen_area": 12.0,
    "floor_number": 23,
    "floors_count": 27,
    "price": 33000000.0,
    "metro": "Юго-Западная",
    "travel_time": 4,
    "coordinates": {
        "lat": 55.663349,
        "lng": 37.478729
    }
}
```

### 7.2. Получение предсказания стоимости

После получения параметров недвижимости можно запросить предсказание стоимости, отправив их методом POST на эндпоинт:
```
POST /predict
```
Тело запроса должно содержать JSON с параметрами объекта (например, теми, что вернулись на первом шаге).

**Пример кода (Python):**

```python
price = httpx.post('http://<server-address>/api/predict', json={'data': getparams.json()})
print(price.status_code)
print(price.text)
```

**Пример результата:**

```
200
{
    "price": 27253739.08660581
}
```

Значение `price` — предсказанная стоимость объекта в рублях.

---

## 8. Streamlit-приложение для предсказания стоимости недвижимости


## 8.1 Основное назначение
Streamlit-приложение доступно по [ссылке](https://ocenomet.streamlit.app/).
Streamlit-приложение разработано для удобного взаимодействия с моделью предсказания стоимости недвижимости. Оно предоставляет следующие функции:

- Прогноз стоимости недвижимости по ссылке на объявление ЦИАН.
- Прогноз стоимости на основе пользовательских данных.
- Загрузка и обучение на пользовательских датасетах в формате CSV.

---

## 8.2 Основной интерфейс
![image](https://github.com/user-attachments/assets/12b3b6f2-c817-4d70-8e5f-a28eeda83581)

### Настройки датасета
- **Загрузка файла**: Пользователь может загрузить свой датасет в формате CSV (размер файла до 200MB).
- **Выбор используемого датасета**: Если пользователь не загружает свои данные, используется стандартный датасет по умолчанию.

### Режимы работы
- **Прогноз стоимости по ссылке**: Пользователь вводит ссылку на объявление ЦИАН, и приложение возвращает предсказанную стоимость объекта.
- **Прогноз стоимости по своим параметрам**: Пользователь вручную вводит параметры объекта, такие как площадь, количество комнат, этаж и т.д., и получает прогноз стоимости.

---
## 8.3 Прогноз стоимости по ссылке

### Описание режима

Этот режим позволяет пользователю ввести ссылку на объявление недвижимости на платформе ЦИАН, чтобы получить предсказанную стоимость квартиры. Приложение автоматически парсит данные из объявления, анализирует их и сравнивает с рыночной статистикой.

### Этапы работы

1. **Ввод ссылки**:
   - Пользователь вводит ссылку на объявление ЦИАН в соответствующее поле.
   - Пример: `https://www.cian.ru/sale/flat/311852463/`.

2. **Парсинг данных**:
   - Приложение извлекает основные параметры объекта из объявления:
     - Общая площадь
     - Жилая площадь
     - Площадь кухни
     - Этаж
     - Количество комнат
     - Цена

3. **Анализ данных**:
   - Полученные параметры сравниваются с медианными и средними значениями по рынку.
   - Приложение строит графики для визуализации:
     - Распределение стоимости квартир.
     - Взаимосвязь общей площади и стоимости.
     - Распределение цен по количеству комнат.
     - Средняя стоимость по округам.

4. **Результаты предсказания**:
   - Приложение отображает:
     - Предсказанную стоимость объекта.
     - Реальную стоимость объекта из объявления.
     - Отклонение предсказанной стоимости от реальной (в процентах и рублях).
   - Карта местоположения квартиры с указанием её положения.

### Пример интерфейса
**Ввод ссылки и таблица с параметрами:**
![image](https://github.com/user-attachments/assets/1aae5bc8-a026-4752-b68e-6a94210777e8)

**Анализ данных с графиками:**
![image](https://github.com/user-attachments/assets/a8a67910-b598-499e-b736-9dccc3d4c9a8)
**Анализ данных с графиками 2:**
![image](https://github.com/user-attachments/assets/ce7c83d9-6217-4c22-ba3a-22121dc3a5bd)

**Результаты предсказания и карта:**
![image](https://github.com/user-attachments/assets/ea0377ff-3327-4dc6-984a-99f03d9d519c)

# 8.4 Режим прогнозирования по своим параметрам

Этот режим позволяет пользователю вручную задать параметры недвижимости для расчёта стоимости объекта. Полезен, когда данные о квартире недоступны в открытых источниках, или для моделирования стоимости объекта с разными характеристиками.

---

## Этапы работы

### 1. Ввод параметров

Пользователь вводит данные в следующих категориях:

#### Основные параметры квартиры
- **Общая площадь (м²)**: Указывается значение от 1 до 200.
- **Количество комнат**: Выбор из диапазона 0–7.
- **Тип квартиры**: Например, "Комнатная квартира", "Студия".
- **Тип ремонта**: Выбор из категорий, таких как "Косметический" или "Без ремонта".

#### Местоположение
- **Район**: Выбор из списка районов Москвы.
- **Ближайшее метро**: Указывается станция метро.
- **Расстояние до центра (км)**: Диапазон от 0 до 40.

#### Параметры дома
- **Год постройки**: Диапазон от 1614 до 2028 года.
- **Этаж**: Значение от -1 до 85.
- **Тип материала**: Например, "Панельный", "Кирпичный".
- **Округ**: Например, "ЦАО", "ЗАО".
- **Количество этажей**: Например 10

#### Транспортная доступность
- **Способ передвижения**: Пешеходный или на транспорте.
- **Время до метро (мин)**: Указывается диапазон от 1 до 52.

Пример интерфейса для ввода параметров:
#### Параметры квартиры:
![image](https://github.com/user-attachments/assets/842837cd-7ed0-47b6-a49e-f2158bdc8fb4)

#### Параметры дома:
![image](https://github.com/user-attachments/assets/990c4f6a-1408-4a9c-990e-099cbf2e420e)

---

### 2. Анализ и прогнозирование

После ввода всех данных, приложение строит следующие графики для анализа:
- **Распределение стоимости квартир**: Гистограмма с выделением прогнозируемой стоимости.
- **Взаимосвязь общей площади и стоимости**: График, показывающий зависимость стоимости от площади.
- **Распределение цен по количеству комнат**: Boxplot с выделением стоимости для заданного количества комнат.
- **Средняя стоимость по округам**: Столбчатая диаграмма, показывающая медианные стоимости в разных округах Москвы.

---

### 3. Результаты прогнозирования

- **Предсказанная стоимость**: Итоговая стоимость объекта в рублях.
- **Реальная стоимость**: Не отображается в этом режиме, так как данные вводятся вручную.

Пример результатов:
![image](https://github.com/user-attachments/assets/6bf279d4-781d-4a15-a924-d231ecdf1fd8)


---

## Преимущества режима

- Возможность моделировать стоимость объектов с разными характеристиками.
- Подходит для оценки объектов, не размещённых на публичных платформах.
- Простота использования благодаря удобному интерфейсу и визуализации.

--- 
## 8.5 Режим работы через загрузка данных в формате CSV

Приложение позволяет загружать данные в формате CSV для обучения модели. Однако есть важные ограничения:

1. **Гибкость в обучении**:
   - На этапе обучения (`fit`) модель принимает любые данные, независимо от их связности с недвижимостью.
   - Это означает, что пользователь может обучить модель на любом наборе данных.

2. **Ограничения для предсказания (`predict`)**:
   - Прогноз возможен только на данных, соответствующих известному формату (структуре), используемому в API.
   - Данные для предсказания должны включать столбцы и строки, соответствующие ключевым параметрам недвижимости.

3. **Особенности обработки данных**:
   - На этапе обучения (`fit`) приложение не проводит валидацию данных. Это означает, что качество и структура данных полностью зависят от пользователя.
   - В случае использования некорректного датасета для предсказания (`predict`), модель выдаст ошибку.

---

## 1. Структура данных для предсказания

# Полный набор данных для обучения (fit)

Для обучения модели (fit) данные должны быть предоставлены в формате CSV. В таблице должны быть следующие столбцы, соответствующие параметрам объекта недвижимости.

## Столбцы CSV для обучения

1. **cian_id**: Уникальный идентификатор объекта на платформе ЦИАН.
2. **deal_type**: Тип сделки (например, "sale" — продажа).
3. **flat_type**: Тип объекта недвижимости (например, "rooms").
4. **description**: Текстовое описание объекта (необязательное поле).
5. **total_area**: Общая площадь объекта (в м²).
6. **living_area**: Жилая площадь объекта (в м²).
7. **kitchen_area**: Площадь кухни (в м²).
8. **floor_number**: Этаж, на котором находится объект.
9. **floors_count**: Общее количество этажей в доме.
10. **price**: Цена объекта (в рублях).
11. **metro**: Название ближайшей станции метро.
12. **travel_time**: Время до метро (в минутах).
13. **lat**: Широта объекта (координаты).
14. **lng**: Долгота объекта (координаты).

---

## Пример структуры CSV

| cian_id   | deal_type | flat_type | description           | total_area | living_area | kitchen_area | floor_number | floors_count | price      | metro         | travel_time | lat       | lng       |
|-----------|-----------|-----------|-----------------------|------------|-------------|--------------|--------------|--------------|------------|---------------|-------------|-----------|-----------|
| 294517249 | sale      | rooms     | Продаётся квартира... | 67.0       | 35.0        | 12.0         | 23           | 27           | 33000000.0 | Юго-Западная | 4           | 55.663349 | 37.478729 |
| 294517250 | sale      | studio    | Уютная квартира...    | 35.0       | 20.0        | 10.0         | 10           | 20           | 15000000.0 | Тропарёво     | 5           | 55.651930 | 37.487921 |

---

# 2. Режим работы с моделями

Этот раздел позволяет пользователю создавать, настраивать, обучать и управлять моделями. Интерфейс поддерживает основные операции, такие как настройка гиперпараметров, загрузка данных, сохранение и удаление моделей.

---

## 2.1 Основные возможности режима

### 1. Создание и обучение модели
Пользователь может создать новую модель, указав следующие параметры:
- **ID модели**: Уникальный идентификатор, например, `001`.
- **Тип модели**: Выбор из предложенного списка, например, `lr` (линейная регрессия).
- **Гиперпараметры**: Ввод параметров в формате JSON (например, `{"alpha": 0.1}`).
- **Данные для обучения**:
  - Входные данные (`X`) в формате JSON.
  - Выходные данные (`y`) в формате JSON.

Пример интерфейса для создания модели:
![image](https://github.com/user-attachments/assets/feb7d423-d9de-475a-8fd9-116be52455d9)


После успешного обучения пользователь видит:
- Метрики модели, например, `R2 Score`.
- График обучения с разделением на тренировочную и тестовую выборки.

Пример результатов обучения:
![image](https://github.com/user-attachments/assets/074686b9-1a79-4f06-9913-341555f0d384)

---

### 2. Управление моделями
#### Просмотр данных моделей
Кнопка "Показать данные моделей" отображает доступные модели, их настройки и результаты обучения.

#### Загрузка модели
Позволяет загрузить ранее сохранённую модель по её ID.

#### Выгрузка модели
Кнопка "Выгрузить модель" позволяет скачать модель для дальнейшего использования.

#### Удаление модели
Пользователь может удалить конкретную модель, указав её ID. Также доступна опция удаления всех моделей сразу.

Пример интерфейса управления моделями:
![image](https://github.com/user-attachments/assets/37a16f26-ff07-4128-b786-e836b569b86c)


---

### Преимущества
- Интуитивно понятный интерфейс для создания и управления моделями.
- Возможность кастомизации гиперпараметров.
- Поддержка различных типов моделей.
- Визуализация метрик и графиков обучения для оценки производительности.

---

# 9. Выводы

1. **Сбор и хранение данных**
   - Развернута БД для хранения ключевых характеристик объектов недвижимости.
   - Настроен устойчивый парсер с ротацией прокси, собирающий данные с ЦИАН.

2. **Модель машинного обучения**
   - Проведён EDA для выявления зависимостей и очистки выбросов.
   - Обучена модель, показывающая высокую точность предсказания стоимости недвижимости.
   - Предусмотрена возможность обучения на пользовательских датасетах.

3. **API и веб-интерфейс**
   - Реализован REST API (FastAPI) для прогноза по ссылке и по кастомным параметрам.
   - Создано Streamlit-приложение с наглядными визуализациями, поддержкой ручного ввода и загрузки CSV.

4. **Инфраструктура на ВПС**
   - Все компоненты (база, парсер, API, приложение) работают круглосуточно на виртуальном сервере.
   - Автоматизирован процесс обновления через скрипт `update.sh`.

5. **Практическая ценность**
   - Сервис удобен как для риелторов и застройщиков, так и для частных лиц.
   - Легко масштабируется, допускает добавление новых функций и интеграций.
