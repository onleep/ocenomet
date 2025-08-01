import math
import pickle
import time

import pandas as pd
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.model_selection import learning_curve
from sklearn.preprocessing import TargetEncoder  # type: ignore

model_paths = {'linear': 'ml/model/linear.pickle', 'catboost': 'ml/model/catboost.pickle'}
models = {name: pickle.load(open(path, 'rb')) for name, path in model_paths.items()}


def distance_from_center(data) -> pd.DataFrame:
    data['lat'] = data['coordinates'].apply(lambda x: x['lat'] if isinstance(x, dict) else None)
    data['lng'] = data['coordinates'].apply(lambda x: x['lng'] if isinstance(x, dict) else None)
    center_lat = 55.753600
    center_lng = 37.621184
    earth_radius_km = 6371

    def haversine(lat1, lng1, lat2, lng2):
        lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * \
            math.cos(lat2) * math.sin(dlng / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return earth_radius_km * c
    data['distance_from_center'] = data\
        .apply(lambda row: haversine(row['lat'], row['lng'], center_lat, center_lng), axis=1)
    return data


def preparams(data) -> dict:
    tables = {
        'addresses': [],
        'developers': [],
        'offers': [],
        'offers_details': [],
        'realty_details': [],
        'realty_inside': [],
        'realty_outside': [],
    }

    for table_name in tables.keys():
        if hasattr(data, table_name):
            tables[table_name].append(getattr(data, table_name).dict())

    dfs = {table: pd.DataFrame(tables[table]) for table in tables}

    data = dfs["addresses"].merge(dfs["offers"], on='cian_id', how='inner')\
        .merge(dfs["offers_details"], on='cian_id', how='inner')

    tables_to_left_join = [dfs["developers"], dfs["realty_details"],
                           dfs["realty_inside"], dfs["realty_outside"]]
    for table in tables_to_left_join:
        data = data.merge(table, on='cian_id', how='left')

    # расчитываем дистанцию от центра
    data = distance_from_center(data)
    return data.iloc[0].to_dict()


def prepredict(data) -> pd.DataFrame:
    data = pd.DataFrame([data.dict()])
    data['lat'] = data['coordinates'].apply(lambda x: x['lat'] if isinstance(x, dict) else None)
    data['lng'] = data['coordinates'].apply(lambda x: x['lng'] if isinstance(x, dict) else None)
    data.drop(columns=['coordinates'], inplace=True)

    data['publication_at'] = pd.to_datetime(pd.to_datetime(data['publication_at'], unit='s', utc=True).dt.date)

    data['finish_year'] = data['finish_date'].apply(lambda x: x.get('year') if isinstance(x, dict) else None)

    data['realty_type'] = data['realty_type'].replace('none', None)
    data.loc[data['finish_year'] <= 0, 'finish_year'] = None
    data['material_type'] = data['material_type'].replace('none', None)
    data.drop(columns=['finish_date'], inplace=True)

    data['total_rate'] = data['total_rate'].astype(float).fillna(4.180479743602584)
    data['review_count'] = data['review_count'].astype(float).fillna(1248.7316089939407)

    mean_proportion_ceiling_height = 0.06049278161032404
    formula = data['total_area'] * mean_proportion_ceiling_height
    data['ceiling_height'] = data['ceiling_height'].where(data['ceiling_height'] > 0, formula)

    mean_proportion_living_area = 0.5486437974462534
    data['living_area'] = data['living_area'].astype(float).fillna(data['total_area'] * mean_proportion_living_area)

    mean_proportion_kitchen_area = 0.4577734591774278
    mask = (data['total_area'] - data['living_area']
            ).replace(0, pd.NA) * mean_proportion_kitchen_area
    data['kitchen_area'] = data['kitchen_area'].astype(float).fillna(mask)
    mean_proportion_rooms_count = 0.06657494706605477
    data['rooms_count'] = data['rooms_count'].fillna(data['living_area'] * mean_proportion_rooms_count).astype(int)
    data['build_year'] = data.apply(lambda row: row['finish_year'] if pd.isna(row['build_year']) else row['build_year'], axis=1)

    data['separated_wc'] = data['separated_wc'].astype(float).fillna(0)
    data['loggias'] = data['loggias'].astype(float).fillna(0)
    data['balconies'] = data['balconies'].astype(float).fillna(0)
    data['combined_wc'] = data['combined_wc'].astype(float).fillna(0)
    data['passenger_lifts'] = data['passenger_lifts'].astype(float).fillna(0)

    data['is_penthouse'] = data['is_penthouse'].astype(bool).fillna(False)
    data['garbage_chute'] = data['garbage_chute'].astype(bool).fillna(False)
    data['is_emergency'] = data['is_emergency'].astype(bool).fillna(False)
    data['is_apartment'] = data['is_apartment'].astype(bool).fillna(False)
    data['is_mortgage_allowed'] = data['is_mortgage_allowed'].astype(bool).fillna(False)
    data['renovation_programm'] = data['renovation_programm'].astype(bool).fillna(False)
    data['is_premium'] = data['is_premium'].astype(bool).fillna(False)
    data['views_count'] = data['views_count'].fillna(632)
    data['photos_count'] = data['photos_count'].fillna(18)
    data['material_type'] = data['material_type'].fillna('panel')
    data['repair_type'] = data['repair_type'].fillna('cosmetic')
    data['project_type'] = data['project_type'].fillna('Индивидуальный проект')
    data['category'] = data['category'].fillna('flatSale')
    data['sale_type'] = data['sale_type'].fillna('free')

    columns_to_int = [
        'price', 'travel_time', 'views_count', 'balconies', 'loggias', 'photos_count',
        'separated_wc', 'combined_wc', 'passenger_lifts', 'review_count', 'build_year'
    ]

    for col in columns_to_int:
        data[col] = data[col].apply(lambda x: int(x) if pd.notna(x) else None)

    data['publication_at'] = pd.to_datetime(data['publication_at'])
    data['year'] = data['publication_at'].dt.year
    data['month'] = data['publication_at'].dt.month
    data['day_of_week'] = data['publication_at'].dt.dayofweek
    data['day_of_month'] = data['publication_at'].dt.day

    data = data.drop(columns=['publication_at'])
    return data


def encoding(data) -> pd.DataFrame | ValueError:
    # onehot
    model_data = models['linear']
    onehot_columns = model_data['onehot_encoder'].feature_names_in_
    for col in onehot_columns:
        if col not in data.columns:
            return ValueError(f"Признак '{col}' отсутствует в данных")
        if data[col].isnull().any():
            return ValueError(f"Признак '{col}' пустой")
    data_encoded = pd.DataFrame(model_data['onehot_encoder'].transform(data[onehot_columns]),
                                columns=model_data['onehot_encoder'].get_feature_names_out(onehot_columns))
    data = pd.concat([data.drop(columns=onehot_columns).reset_index(drop=True), data_encoded], axis=1)

    # origin
    if data.get('repair_type') is None:
        return ValueError("Признак 'repair_type' пустой")
    orignal_columns = {'repair_type': {'no': 0, 'cosmetic': 1, 'euro': 2, 'design': 3}}
    for col, mapping in orignal_columns.items():
        data[col] = data[col].map(mapping)

    # target
    target_columns = ['district', 'project_type', 'metro']
    for col in target_columns:
        if col not in data.columns:
            return ValueError(f"Признак '{col}' отсутствует в данных")
        if data[col].isnull().any():
            return ValueError(f"Признак '{col}' пустой")
    data[target_columns] = pd.DataFrame(model_data['target_encoder'].transform(data[target_columns]),
                                        columns=target_columns)

    # scaler
    scaler_columns = model_data['scaler'].feature_names_in_
    for col in scaler_columns:
        if col not in data.columns:
            return ValueError(f"Признак '{col}' отсутствует в данных")
        if data[col].isnull().any():
            return ValueError(f"Признак '{col}' пустой")
    data = data[scaler_columns]
    data = pd.DataFrame(model_data['scaler'].transform(data), columns=data.columns)

    # model
    model_columns = model_data['model'].feature_names_in_
    for col in model_columns:
        if col not in data.columns:
            return ValueError(f"Признак '{col}' отсутствует в данных")
        if data[col].isnull().any():
            return ValueError(f"Признак '{col}' пустой")
    data = data[model_columns]
    return data

def prefit(X, y, model_type, hyperparameters) -> dict | Exception:
    try:
        if model_type == 'lr':
            model = LinearRegression(**hyperparameters)
        elif model_type == 'ls':
            model = Lasso(**hyperparameters)
        else:
            model = Ridge(**hyperparameters)
    except:
        return Exception('Неверные гиперпараметры')
    df = pd.DataFrame(X)
    if (lendf := len(df.iloc[0])) < 2:
        return Exception('Признаков меньше 2')
    if len(df) < 20:
        return Exception('Значений должно быть не меньше 20')
    if df.isnull().any().any():
        return Exception('В X есть пропущенные значения')
    y = pd.Series(y)
    if len(df) != len(y):
        return Exception('Размеры X и y не совпадают')
    cv = min(lendf, 10)
    target_encoder = TargetEncoder(target_type='continuous', cv=cv)
    cols = df.select_dtypes(exclude=['number', 'boolean']).columns
    if len(cols) > 0:
        df[cols] = target_encoder.fit_transform(df[cols], y)
    start = time.time()
    model.fit(df, y)
    fittime = time.time() - start
    train_size = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    train_sizes, train_scores, test_scores = learning_curve(model, df, y, cv=cv, scoring='r2', train_sizes=train_size) # type: ignore
    test_scores = test_scores.mean(axis=1).tolist()

    return {
        'model': model,
        'model_type': model_type,
        'target_encoder': target_encoder,
        'hyperparameters': model.get_params(),
        'train_time': fittime,
        'r2': test_scores[-2],
        'learning_curve': {
            'train_sizes': train_sizes.tolist(),
            'r2_train_scores': train_scores.mean(axis=1).tolist(),
            'r2_test_scores': test_scores,
        },
    }


def predict(data, sysmodel, loaded_model=None, request_id=None) -> float | Exception:
    # sysmodel
    if not request_id or not loaded_model:
        model = models[sysmodel]['model']
        if sysmodel == 'catboost':
            model_columns = model.feature_names_
        else:
            model_columns = model.feature_names_in_
    else:
        model = loaded_model.get(request_id)
        if not model: return Exception()
        model_columns = model.feature_names_in_

    for col in model_columns:
        if col not in data.columns:
            return Exception(f"Признак '{col}' отсутствует в данных")
        if data[col].isnull().any():
            return Exception(f"Признак '{col}' пустой")

    data = data[model_columns]

    if not request_id or not loaded_model:
        predict = model.predict(data)
        return predict[0]

    # custom model
    target_encoder = model['target_encoder']
    target_columns = data.select_dtypes(exclude=['number', 'boolean']).columns

    if len(target_columns) > 0:
        try:
            encdata = target_encoder.transform(data[target_columns])
            data[target_columns] = pd.DataFrame(encdata, columns=target_columns)
        except Exception as e:
            return e
    price = model['model'].predict(data)
    return price
