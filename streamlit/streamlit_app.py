import pandas as pd
import json
import streamlit as st

build_year_min = 1614
build_year_max = 2028

distance_from_center_min = 0
distance_from_center_max = 40

total_area_min = 8
total_area_max = 200

rooms_count_min = 0
rooms_count_max = 7

floor_number_min = -1
floor_number_max = 85

repair_type_data = ['Евроремонт', 'Без ремонта', 'Косметический', 'Дизайнерский'] # ['euro', 'no', 'cosmetic', 'design']
flat_type_data = ['Комнатная квартира', 'Студия', 'Свободная планировка'] # ['rooms', 'studio', 'openPlan']
material_type_data = ['Панельный', 'Монолитный', 'Блочный', 'Кирпичный', 'Монолитно-кирпичный', 'Сталинский', 'Деревянный'] # ['panel', 'monolith', 'block', 'brick', 'monolithBrick', 'stalin', 'wood']
county_data = ['ЗелАО', 'ЮАО', 'СЗАО', 'ЗАО', 'ЦАО', 'САО', 'СВАО', 'ЮВАО', 'ВАО', 'ЮЗАО', 'ТАО (Троицкий)']

district_data = ['Старое Крюково', 'Даниловский', 'Куркино', 'Раменки', 'Хамовники',
 'Головинский', 'Отрадное', 'Строгино', 'Южнопортовый', 'Останкинский',
 'Щукино', 'Северное Измайлово', 'Дорогомилово', 'Северное Бутово',
 'Филевский парк', 'Кунцево', 'Алтуфьевский', 'Лосиноостровский', 'Мещанский',
 'Новогиреево', 'Нагатино-Садовники', 'Проспект Вернадского', 'Арбат',
 'Академический', 'Марьино', 'Можайский', 'Чертаново Северное', 'Дмитровский',
 'Хорошево-Мневники', 'Донской', 'Зюзино', 'Котловка', 'Москворечье-Сабурово',
 'Лианозово', 'Савеловский', 'Текстильщики', 'Перово', 'Бирюлево Западное',
 'Тверской', 'Нагорный', 'Орехово-Борисово Южное', 'Замоскворечье',
 'Измайлово', 'Рязанский', 'Южное Бутово', 'Очаково-Матвеевское',
 'Пресненский', 'Люблино', 'Басманный', 'Бутырский', 'Таганский', 'Солнцево',
 'Коньково', 'Крюково', 'Свиблово', 'Гагаринский', 'Косино-Ухтомский',
 'Чертаново Южное', 'Ростокино', 'Беговой', 'Бибирево', 'Алексеевский',
 'Сокольники', 'Преображенское', 'Митино', 'Чертаново Центральное', 'Вешняки',
 'Крылатское', 'Лефортово', 'Марфино', 'Гольяново', 'Новокосино', 'Богородское',
 'Аэропорт', 'Метрогородок', 'Марьина роща', 'Нижегородский', 'Обручевский',
 'Тропарево-Никулино', 'Некрасовка', 'Покровское-Стрешнево',
 'Бирюлево Восточное', 'Ломоносовский', 'Тимирязевский', 'Хорошевский',
 'Орехово-Борисово Северное', 'Зябликово', 'Ясенево', 'Нагатинский затон',
 'Войковский', 'Северное Медведково', 'Коптево', 'Выхино-Жулебино', 'Северный',
 'Теплый Стан', 'Северное Тушино', 'Фили-Давыдково', 'Якиманка', 'Ивановское',
 'Ховрино', 'Соколиная гора', 'Ярославский', 'Братеево', 'Савёлки',
 'Бабушкинский', 'Новая Москва', 'Западное Дегунино', 'Внуково',
 'Ново-Переделкино', 'Царицыно', 'Сокол', 'Левобережный', 'Южное Тушино',
 'Молжаниновский', 'Бескудниковский', 'Матушкино', 'Восточное Измайлово',
 'Южное Медведково', 'Кузьминки', 'Черемушки', 'Печатники', 'Красносельский',
 'Восточный', 'Восточное Дегунино', 'Силино', 'Капотня']

metro_data = ['Зеленоград — Крюково', 'Тульская', 'Сходненская', 'Мичуринский проспект',
 'Парк Культуры', 'Водный стадион', 'Владыкино', 'Строгино', 'Кожуховская',
 'Улица Академика Королёва', 'Октябрьское поле', 'Щёлковская', 'Киевская',
 'Бульвар Дмитрия Донского', 'Фили', 'Молодёжная', 'Университет',
 'Бескудниково', 'Медведково', 'Проспект Мира', 'Новогиреево', 'Нагатинская',
 'Новаторская', 'Смоленская', 'Академическая', 'Марьино', 'Давыдково', 'Южная',
 'Яхромская', 'Народное Ополчение', 'Ленинский проспект', 'Каховская',
 'Нагорная', 'Кантемировская', 'Алтуфьево', 'Петровский Парк', 'Текстильщики',
 'Перово', 'Пражская', 'Новослободская', 'Домодедовская', 'Павелецкая',
 'Первомайская', 'Бульвар Адмирала Ушакова', 'Славянский бульвар', 'Шелепиха',
 'Люблино', 'Электрозаводская', 'Дмитровская', 'Крестьянская застава',
 'Улица Скобелевская', 'Солнцево', 'Тверская', 'Беляево', 'Белорусская',
 'Кропоткинская', 'Деловой центр', 'Ботанический сад', 'Лухмановская',
 'Улица Академика Янгеля', 'Улица Сергея Эйзенштейна', 'Сетунь', 'Динамо',
 'Спортивная', 'ЗИЛ', 'Пушкинская', 'Улица 1905 года', 'ВДНХ', 'Сокольники',
 'Чертановская', 'Преображенская площадь', 'Арбатская', 'Пятницкое шоссе',
 'Зябликово', 'Проспект Вернадского', 'Маяковская', 'Крылатское',
 'Авиамоторная', 'Фонвизинская', 'Менделеевская', 'Черкизовская', 'Новокосино',
 'Белокаменная', 'Курская', 'Савёловская', 'Москва-Сити', 'Серпуховская',
 'Нижегородская', 'Воронцовская', 'Юго-Западная', 'Парк Победы',
 'Ломоносовский проспект', 'Боровицкая', 'Аэропорт', 'Некрасовка',
 'Площадь Ильича', 'Бульвар Рокоссовского', 'Спартак', 'Новые Черёмушки',
 'Покровское', 'Римская', 'Волоколамская', 'Терехово', 'Орехово',
 'Шипиловская', 'Выхино', 'Ясенево', 'Бунинская аллея', 'Багратионовская',
 'Марьина Роща', 'Коломенская', 'Полежаевская', 'Щукинская', 'Баррикадная',
 'Пролетарская', 'Селигерская', 'Коптево', 'Говорово',
 'Лермонтовский проспект', 'Цветной бульвар', 'Марк', 'Чкаловская', 'Озёрная',
 'Поклонная', 'Коньково', 'Матвеевская', 'Профсоюзная', 'Отрадное',
 'Трикотажная', 'Бауманская', 'Волгоградский проспект', 'Октябрьская',
 'Рязанский проспект', 'Физтех', 'Окружная', 'Братиславская',
 'Петровско-Разумовская', 'Речной вокзал', 'Волжская', 'Краснопресненская',
 'Раменки', 'Планерная', 'Новоясеневская', 'Достоевская', 'Бибирево',
 'Технопарк', 'Семёновская', 'Бабушкинская', 'Воробьёвы горы', 'Тушинская',
 'Войковская', 'Университет Дружбы Народов', 'Аминьевская', 'Хорошёво',
 'Тропарёво', 'Алма-Атинская', 'Ховрино', 'Улица Горчакова',
 'Шоссе Энтузиастов', 'Крёкшино', 'Беговая', 'Верхние Лихоборы',
 'Аэропорт Внуково', 'Переделкино', 'Ростокино', 'Минская', 'Царицыно',
 'Балтийская', 'Добрынинская', 'Калужская', 'Автозаводская', 'Щербинка',
 'Алексеевская', 'Окская', 'Гольяново', 'Зорге', 'Беломорская', 'Хорошёвская',
 'Новокузнецкая', 'Улица Милашенкова', 'Нахимовский проспект',
 'Боровское шоссе', 'Новопеределкино', 'Жулебино', 'Лианозово', 'Кузьминки',
 'Звенигородская', 'Китай-город', 'Кунцевская', 'Грачёвская', 'Свиблово',
 'Печатники', 'Тимирязевская', 'Площадь Гагарина', 'Новохохловская',
 'Кутузовская', 'Комсомольская', 'Варшавская', 'Дубровка', 'Марксистская',
 'Долгопрудная', 'Бутырская', 'Юго-Восточная', 'Зюзино', 'Борисово', 'Полянка',
 'Лесопарковая', 'Александровский сад', 'Митино', 'Фрунзенская', 'Депо', 'ЦСКА',
 'Филёвский парк', 'Сокол', 'Севастопольская', 'Бирюлёво', 'Таганская',
 'Рабочий посёлок', 'Шаболовская', 'Сухаревская', 'Лебедянская',
 'Нагатинский Затон', 'Генерала Тюленева', 'Стрешнево', 'Измайлово',
 'Тёплый Стан', 'Кленовый бульвар', 'Трубная', 'Моссельмаш', 'Третьяковская',
 'Перерва', 'Кавказский бульвар', 'Мякинино', 'Тургеневская', 'Серебряный Бор',
 'Студенческая', 'Дегунино', 'Аннино', 'Пионерская', 'Чистые пруды', 'Липецкая',
 'Локомотив', 'Площадь трёх вокзалов', 'Лефортово', 'Соколиная гора',
 'Красный Балтиец', 'Подрезково', 'Кузнецкий мост', 'Рижская', 'Вешняки',
 'Мнёвники', 'Каширская', 'Немчиновка', 'Красные ворота', 'Новоподрезково',
 'Красногвардейская', 'Люберцы', 'Курьяново', 'Партизанская', 'Москворечье',
 'Лихоборы', 'Бульвар Генерала Карбышева', 'Рассказовка',
 'Сретенский бульвар', 'Пенягино', 'Калитники', 'Саларьево', 'Охотный ряд',
 'Лубянка', 'Новодачная', 'Верхние котлы', 'Косино', 'Измайловская',
 'Красносельская', 'Крымская', 'Каспийская', 'Улица Дмитриевского', 'Бутово',
 'Молжаниново', 'Чеховская', 'Стахановская', 'Очаково', 'Битцевский парк',
 'Потапово', 'Вавиловская', 'Нахабино', 'Химки', 'Угрешская', 'Серп и Молот',
 'Красный Строитель', 'Чухлинка', 'Сортировочная', 'Котельники', 'Битца',
 'Театральная', 'Сколково', 'Телецентр', 'Площадь Революции',
 'Улица Старокачаловская', 'Панфиловская', 'Лобня', 'Мещерская',
 'Шереметьевская', 'Библиотека им. Ленина', 'Филатов Луг', 'Плющево',
 'Фирсановская', 'Карамышевская', 'Гражданская', 'Останкино',
 'Москва-Товарная']

# Интерфейс Streamlit
st.title("Прогноз стоимости квартиры")

# Сайдбар для выбора режима
st.sidebar.header("Выберите режим")
mode = st.sidebar.radio("Режим работы", [
    "Прогноз стоимости по ссылке cian",
    "Прогноз стоимости по параметрам"
])

if mode == "Прогноз стоимости по ссылке cian":
    st.subheader("Прогноз стоимости по ссылке")

    cian_url = st.text_input("Введите ссылку на объявление cian")

    if cian_url:
        try:
            df = page_parse(cian_url)  # ендпоинт 1

            # Отображаем загруженные данные
            st.subheader("Полученные данные")
            st.dataframe(df)

            # Прогноз
            predicted_price = predict_price(df.drop(columns=['price'])) # ендпоинт 2
            real_price = df['price']

            difference = predicted_price - real_price # 1000 - 2000 = -1000
            difference_percent = (difference / real_price) * 100 # 100 * (-1000/2000) = -50%

            st.subheader("Результаты прогнозирования")
            st.write(f"Реальная стоимость: {real_price:.2f} ₽")
            st.write(f"Предсказанная стоимость: {predicted_price[0]:.2f} ₽")
            st.write(f"Разница прогнозной стоимости от реальной: {difference[0]:.2f} ₽ ({difference_percent[0]:.2f}%)")

            if difference > 0:
                st.success(f"Выгодно покупать. Экономия {difference[0]:.2f} ₽.")
            else:
                st.error(f"Не выгодно покупать. Переплата {-difference[0]:.2f} ₽.")

        except Exception as e:
            st.error(f"Произошла ошибка: {e}")

elif mode == "Прогноз стоимости по параметрам":
    st.subheader("Прогноз стоимости по параметрам")

    total_area = st.slider("Общая площадь (м²)", min_value=total_area_min, max_value=total_area_max, value=92, step=1)
    rooms_count = st.slider("Количество комнат", min_value=rooms_count_min, max_value=rooms_count_max, value=1, step=1)
    metro = st.selectbox("Ближайшее метро", metro_data, index = metro_data.index('Аминьевская'))
    distance_from_center = st.slider("Расстояние до центра (км)", min_value=distance_from_center_min, max_value=distance_from_center_max, value=13, step=0.1)
    district = st.selectbox("Район", district_data, index = district_data.index('Раменки'))
    build_year = st.slider("Год постройки", min_value=build_year_min, max_value=build_year_max, value=2022, step=1)
    floor_number = st.slider("Этаж", min_value=floor_number_min, max_value=floor_number_max, value=7, step=1)
    material_type = st.selectbox("Тип материала", material_type_data, index=material_type_data.index('Панельный'))
    county = st.selectbox("Округ", county_data, index=county_data.index('ЗАО'))
    flat_type = st.selectbox("Тип квартиры", flat_type_data, index=flat_type_data.index('Комнатная квартира'))
    repair_type = st.selectbox("Тип ремонта", repair_type_data, index=repair_type_data.index('Косметический'))

    # Прогноз
    if st.button("Прогнозировать стоимость"):
        # Перевод признаков в английские значения
        material_type_mapping = {
            'Панельный': 'panel',
            'Монолитный': 'monolith',
            'Блочный': 'block',
            'Кирпичный': 'brick',
            'Монолитно-кирпичный': 'monolithBrick',
            'Сталинский': 'stalin',
            'Деревянный': 'wood'
        }

        flat_type_mapping = {
            'Комнатная квартира': 'rooms',
            'Студия': 'studio',
            'Свободная планировка': 'openPlan'
        }

        repair_type_mapping = {
            'Евроремонт': 'euro',
            'Без ремонта': 'no',
            'Косметический': 'cosmetic',
            'Дизайнерский': 'design'
        }

        # Собираем данные в JSON
        input_data = {
            "total_area": total_area,
            "rooms_count": rooms_count,
            "metro": metro,
            "distance_from_center": distance_from_center,
            "district": district,
            "build_year": build_year,
            "floor_number": floor_number,
            "material_type": material_type_mapping[material_type],
            "county": county,
            "flat_type": flat_type_mapping[flat_type],
            "repair_type": repair_type_mapping[repair_type]
        }

        # Создаем DataFrame из JSON
        df = pd.DataFrame([input_data])

        # Отображаем загруженные данные
        st.subheader("Выбранные данные")
        st.dataframe(df)

        # Прогноз
        try:
            input_json = json.dumps(input_data)
            predicted_price = predict_price(input_json) # ендпоинт 2

            st.subheader("Результаты прогнозирования")
            st.write(f"Предсказанная стоимость: {predicted_price[0]:.2f} ₽")
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
