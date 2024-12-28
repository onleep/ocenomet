import requests
import pandas as pd

def get_data_page(url):
    """Получает данные с объявления Циан"""
    endpoint = "http://your-api-endpoint/page_parse"
    try:
        response = requests.post(endpoint, json={"url": url})
        response.raise_for_status()
        data = response.json()
        
        if "error" in data:
            return f"Ошибка: {data['error']}"
        if not data:
            return "Ошибка: Получены пустые данные."
        
        df = pd.DataFrame([data]).replace({None: pd.NA})
        return df
    except requests.exceptions.RequestException as e:
        return f"Произошла ошибка при запросе: {e}"

# Функция для получения предсказания цены
def get_predict_price(input_data):
    """Получает предсказанную цену от модели"""
    endpoint = "http://your-api-endpoint/predict_price"
    try:
        response = requests.post(endpoint, json=input_data)
        response.raise_for_status()
        data = response.json()

        if "predicted_price" in data:
            return float(data["predicted_price"])
        elif "error" in data:
            return f"Ошибка: {data['error']}"
        return "Ошибка: Неизвестный ответ от сервера."
    except requests.exceptions.RequestException as e:
        return f"Произошла ошибка при запросе: {e}"

def calculate_difference(predicted_price, real_price):
    """Рассчитывает разницу и процентное отклонение"""
    difference = predicted_price - real_price
    difference_percent = (difference / real_price) * 100
    return difference, difference_percent

def map_feature_values(material_type, flat_type, repair_type, travel_type):
    """Маппинг значений признаков в формат, ожидаемый API."""
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

    travel_type_mapping = {
        'Пешком': 'walk',
        'На транспорте': 'transport'
    }

    return {
        "material_type": material_type_mapping.get(material_type, material_type),
        "flat_type": flat_type_mapping.get(flat_type, flat_type),
        "repair_type": repair_type_mapping.get(repair_type, repair_type),
        "travel_type": travel_type_mapping.get(travel_type, travel_type)
    }
