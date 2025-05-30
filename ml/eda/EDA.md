# Ссылки на данные и EDA

## Ссылка на Google Colab
- **Вариант 1**: [EDA на Google Colab](https://colab.research.google.com/drive/11-D42g0p_961q3Z9cnP4VY2uj7UFJqjj?usp=sharing)
- **Вариант 2**: [EDA на GitHub](https://github.com/onleep/ocenomet/tree/main/eda)

## Ссылка на датасет с данными по объявлениям о продаже недвижимости с Циан
- [**Данные на Яндекс Диск**](https://disk.yandex.ru/d/SUk9j2qwqPNPEw)

# Анализ данных недвижимости в Москве
В рамках EDA проанализированы семь таблиц (addresses, developers, offers, offers_details, realty_details, realty_inside, realty_outside), структурированных в соответствии с содержанием данных в базе данных проекта. Данные взяты с сервиса cian.

## Таблица «addresses»:
Таблица «addresses» содержит информацию о характеристиках местоположения объектов недвижимости в городе Москва.

В рамках анализа таблицы было выявлено:
- Большинство объявлений, представленных на сайте cian.ru, расположены в округе ЦАО, а по остальным округам распределение практически одинаково.
- Количество объявлений по квартирам в новостройках также преобладает в округе ЦАО, но также достаточно много в округах ЗАО, СВАО.
- Медианное время от объектов недвижимости до ближайшего метро составляет 10 минут.
- Наибольшее количество предложений по покупке недвижимости преобладает возле метро Шелепиха.

## Таблица «developers»:
Таблица «developers» содержит информацию о застройщиках.

В рамках анализа таблицы было выявлено:
- Большинство объектов было построено в периоде с 1994 по 2010 год.
- Средняя оценка застройщиков составляет 4.1.
- Отзывов по застройщикам мало оставляют.
- Группа самолет на данный момент является самым популярным застройщиком.

## Таблица «offers»:
Таблица «offers» содержит информацию о предложениях по недвижимости.

В рамках анализа таблицы было выявлено следующее:
- Предложения представлены в основном за 2022, 2023 и 2024. Наибольшее количество объявлений представлено за 2024 год.
- Самый популярный месяц по публикациям по всем годам является октябрь.
- Категория «Доля в квартире» имеет наименьшее количество предложений.
- Таблица содержит историю цен по каждому объявлению.
- Медианная цена составляет 21 млн. Таблица имеет достаточное количество выбросов, которые были убраны.

## Таблица «offers_details»:
Таблица «offers_details» содержит дополнительную информацию по публикациям.

В рамках анализа таблицы было выявлено следующее:
- В таблице представлены только данные, связанные с продажей квартир, без аренды.
- Наибольшее количество объявлений с типом квартиры «Комнатная квартира».
- Самая популярный тип продажи – Свободная продажа.

## Таблица «realty_details»:
Таблица «realty_details» содержит информацию о характеристиках недвижимости.

В рамках анализа таблицы было выявлено следующее:
- Самый популярный тип отопления – центральное.
- В основном в объявлениях указано, что ипотека разрешена.
- Наибольшее количество квартир не имеют газоснабжения.
- Много квартир еще на стадии постройки.

## Таблица «realty_inside»:
Таблица «realty_inside» содержит данные о недвижимости, включая характеристики объектов, такие как тип ремонта, общая и жилая площади, площадь кухни, высота потолков и количество балконов, лоджий и комнат.

В рамках анализа было выявлено следующее:
- Самый популярный тип ремонта среди объявлений - дизайнерский.
- В таблице нет явной корреляции между признаками.

## Таблица «realty_outside»:
Таблица «realty_outside» содержит информацию о характеристиках здания.

В рамках анализа было выявлено следующее:
- Самый популярный тип дома среди объявлений – монолитный.
- В основном парковочные места у домов подземные.
- В таблице нет явной корреляции между признаками.
## Корреляция price(таргет) c признаками
-  У колонки price есть сильная корреляция с таким признаками как living_area,  total_area, kitchen_area, rooms_count, combined_wc, что означает высокую степень взаимосвязи .
-  В основном колонка price имеет положительную зависимость с планировкой квартир.

## Вывод:
В рамках разведочного анализа данных (EDA) были проанализированы семь таблиц, отражающих различные аспекты рынка недвижимости в Москве, с акцентом на информацию о местоположении, застройщиках, предложениях и характеристиках объектов, а также были рассмотрены зависимости признаков с таргетом. Полный анализ можно посмотреть в по любой ссылке:
> [EDA на GitHub](https://github.com/onleep/ocenomet/tree/main/eda)

> [Google Colab](https://colab.research.google.com/drive/11-D42g0p_961q3Z9cnP4VY2uj7UFJqjj?usp=sharing)



