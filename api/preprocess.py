import pandas as pd
import math


def preprocess(data) -> list | pd.DataFrame:
    tables = {
        "addresses": [],
        "developers": [],
        "offers": [],
        "offers_details": [],
        "realty_details": [],
        "realty_inside": [],
        "realty_outside": []
    }

    for table_name in tables.keys():
        if hasattr(data, table_name):
            tables[table_name].append(getattr(data, table_name).dict())

    addresses_df = pd.DataFrame(tables["addresses"])
    developers_df = pd.DataFrame(tables["developers"])
    offers_df = pd.DataFrame(tables["offers"])
    offers_details_df = pd.DataFrame(tables["offers_details"])
    realty_details_df = pd.DataFrame(tables["realty_details"])
    realty_inside_df = pd.DataFrame(tables["realty_inside"])
    realty_outside_df = pd.DataFrame(tables["realty_outside"])

    addresses_df['lat'] = addresses_df['coordinates'].apply(lambda x: x['lat'] if isinstance(x, dict) else None)
    addresses_df['lng'] = addresses_df['coordinates'].apply(lambda x: x['lng'] if isinstance(x, dict) else None)
    addresses_df.drop(columns=['coordinates', 'address'], inplace=True)

    offers_df = offers_df.dropna(subset=['photos_count'])
    offers_df['publication_at'] = pd.to_datetime(pd.to_datetime(
        offers_df['publication_at'], unit='s', utc=True).dt.date)

    offers_df = offers_df.dropna(subset=['photos_count'])
    offers_df['publication_at'] = pd.to_datetime(pd.to_datetime(
        offers_df['publication_at'], unit='s', utc=True).dt.date)

    realty_details_df['finish_year'] = realty_details_df['finish_date'].apply(
        lambda x: x.get('year') if isinstance(x, dict) else None)

    realty_details_df['realty_type'] = realty_details_df['realty_type'].replace('none', None)
    realty_details_df.loc[realty_details_df['finish_year'] <= 0, 'finish_year'] = None
    realty_outside_df['material_type'] = realty_outside_df.get('material_type', None)
    realty_outside_df['material_type'] = realty_outside_df['material_type'].replace('none', None)
    realty_details_df.drop(columns=['finish_date'], inplace=True)

    main_df = addresses_df.merge(offers_df, on='cian_id', how='inner').merge(offers_details_df, on='cian_id', how='inner')

    tables_to_left_join = [developers_df, realty_details_df, realty_inside_df, realty_outside_df]
    for table in tables_to_left_join:
        main_df = main_df.merge(table, on='cian_id', how='left')

    main_df = main_df[main_df['photos_count'] >= 0].reset_index(drop=True)

    main_df['separated_wc'] = main_df['separated_wc'].fillna(0)
    main_df['loggias'] = main_df['loggias'].fillna(0)
    main_df['balconies'] = main_df['balconies'].fillna(0)
    main_df['combined_wc'] = main_df['combined_wc'].fillna(0)
    main_df['passenger_lifts'] = main_df['passenger_lifts'].fillna(0)

    main_df['total_rate'] = main_df['total_rate'].fillna(4.180479743602584)
    main_df['review_count'] = main_df['review_count'].fillna(1248.7316089939407)

    mean_proportion_ceiling_height = 0.06049278161032404
    formula = main_df['total_area'] * mean_proportion_ceiling_height
    main_df['ceiling_height'] = main_df['ceiling_height'].where(
        main_df['ceiling_height'] > 0, formula)

    mean_proportion_living_area = 0.5486437974462534
    main_df['living_area'] = main_df['living_area'].fillna(main_df['total_area'] * mean_proportion_living_area)

    mean_proportion_kitchen_area = 0.4577734591774278
    mask = (main_df['total_area'] - main_df['living_area']).replace(0, pd.NA) * mean_proportion_kitchen_area
    main_df['kitchen_area'] = main_df['kitchen_area'].fillna(mask)

    mean_proportion_rooms_count = 0.06657494706605477
    main_df['rooms_count'] = main_df['rooms_count'].fillna(main_df['living_area'] * mean_proportion_rooms_count).astype(int)
    main_df['build_year'] = main_df.apply(lambda row: row['finish_year'] if pd.isna(row['build_year']) else row['build_year'], axis=1)

    main_df = main_df.dropna(subset=['travel_time', 'views_count', 'kitchen_area', 'build_year']).copy()

    main_df['is_penthouse'] = main_df['is_penthouse'].astype(bool).fillna(False)
    main_df['garbage_chute'] = main_df['garbage_chute'].astype(bool).fillna(False)
    main_df['is_emergency'] = main_df.get('is_emergency', None)
    main_df['renovation_programm'] = main_df.get('renovation_programm', None)
    main_df['project_type'] = main_df.get('project_type', None)
    main_df['is_emergency'] = main_df['is_emergency'].astype(bool).fillna(False)
    main_df['is_apartment'] = main_df['is_apartment'].astype(bool).fillna(False)
    main_df['is_mortgage_allowed'] = main_df['is_mortgage_allowed'].astype(bool).fillna(False)
    main_df['renovation_programm'] = main_df['renovation_programm'].astype(bool).fillna(False)

    main_df['photos_count'] = main_df['photos_count'].astype(int)
    main_df['price'] = main_df['price'].astype(int)
    main_df['travel_time'] = main_df['travel_time'].astype(int)
    main_df['views_count'] = main_df['views_count'].astype(int)
    main_df['balconies'] = main_df['balconies'].astype(int)
    main_df['loggias'] = main_df['loggias'].astype(int)
    main_df['separated_wc'] = main_df['separated_wc'].astype(int)
    main_df['combined_wc'] = main_df['combined_wc'].astype(int)
    main_df['passenger_lifts'] = main_df['passenger_lifts'].astype(int)
    main_df['review_count'] = main_df['review_count'].astype(int)
    main_df['build_year'] = main_df['build_year'].astype(int)
    if main_df['material_type'] is None: main_df['material_type'] = 'ground'
    if main_df['repair_type'] is None: main_df['repair_type'] = 'cosmetic'

    main_df['publication_at'] = pd.to_datetime(main_df['publication_at'])
    main_df['year'] = main_df['publication_at'].dt.year
    main_df['month'] = main_df['publication_at'].dt.month
    main_df['day_of_week'] = main_df['publication_at'].dt.dayofweek
    main_df['day_of_month'] = main_df['publication_at'].dt.day

    main_df = main_df.drop(columns=['publication_at'])

    center_lat = 55.753600
    center_lng = 37.621184

    earth_radius_km = 6371

    def haversine(lat1, lng1, lat2, lng2):
        lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return earth_radius_km * c

    main_df['distance_from_center'] = haversine(main_df['lat'], main_df['lng'], center_lat, center_lng)

    columns_to_keep = ['county', 'district', 'metro', 'travel_type', 'travel_time', 'price',
                    'category', 'views_count', 'photos_count', 'floor_number',
                    'floors_count', 'flat_type', 'sale_type', 'review_count', 'total_rate',
                    'project_type', 'is_apartment', 'is_penthouse', 'is_mortgage_allowed',
                    'is_premium', 'is_emergency', 'renovation_programm', 'repair_type',
                    'total_area', 'living_area', 'kitchen_area', 'ceiling_height',
                    'balconies', 'loggias', 'rooms_count', 'separated_wc', 'combined_wc',
                    'build_year', 'material_type', 'garbage_chute', 'passenger_lifts',
                    'distance_from_center', 'year', 'month', 'day_of_week', 'day_of_month']

    main_df = main_df[columns_to_keep]


    missing_columns = main_df[['district', 'county', 'sale_type']].isna().any()
    if missing_columns.any():
        return missing_columns[missing_columns].index.to_list()

    X = main_df.drop(columns=['price'])
    return X
