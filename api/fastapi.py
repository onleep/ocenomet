from fastapi import FastAPI, HTTPException
from .preprocess import preprocess
from app.main import apartPage
from pydantic import BaseModel
import pandas as pd
import uvicorn
import pickle
import re


class Offers(BaseModel):
    cian_id: int
    price: float
    category: str | None = None
    views_count: int | None = None
    photos_count: int | None = None
    floor_number: int | None = None
    floors_count: int | None = None
    publication_at: int | None = None
    price_changes: list | None = None


class Addresses(BaseModel):
    cian_id: int
    county: str | None = None
    district: str | None = None
    street: str | None = None
    house: str | None = None
    metro: str | None = None
    travel_type: str | None = None
    travel_time: int | None = None
    address: list | None = None
    coordinates: dict | None = None


class RealtyInside(BaseModel):
    cian_id: int
    repair_type: str | None = None
    total_area: float | None = None
    living_area: float | None = None
    kitchen_area: float | None = None
    ceiling_height: float | None = None
    balconies: int | None = None
    loggias: int | None = None
    rooms_count: int | None = None
    separated_wc: float | None = None
    combined_wc: int | None = None
    windows_view: str | None = None


class RealtyOutside(BaseModel):
    cian_id: int
    build_year: int | None = None
    entrances: int | None = None
    material_type: str | None = None
    parking_type: str | None = None
    garbage_chute: bool | None = None
    lifts_count: int | None = None
    passenger_lifts: int | None = None
    cargo_lifts: int | None = None


class RealtyDetails(BaseModel):
    cian_id: int
    realty_type: str | None = None
    project_type: str | None = None
    heat_type: str | None = None
    gas_type: str | None = None
    is_apartment: bool | None = None
    is_penthouse: bool | None = None
    is_mortgage_allowed: bool | None = None
    is_premium: bool | None = None
    is_emergency: bool | None = None
    renovation_programm: bool | None = None
    finish_date: dict | None = None


class OffersDetails(BaseModel):
    cian_id: int
    agent_name: str | None = None
    deal_type: str | None = None
    flat_type: str | None = None
    sale_type: str | None = None
    is_duplicate: bool | None = None
    description: str | None = None


class Developers(BaseModel):
    cian_id: int
    name: str | None = None
    review_count: int | None = None
    total_rate: float | None = None
    buildings_count: int | None = None
    foundation_year: int | None = None
    is_reliable: bool | None = None


class Data(BaseModel):
    offers: Offers
    addresses: Addresses
    realty_inside: RealtyInside
    realty_outside: RealtyOutside
    realty_details: RealtyDetails
    offers_details: OffersDetails
    developers: Developers

app = FastAPI()

with open('model.pickle', 'rb') as file:
    model_data = pickle.load(file)

model = model_data['model']
onehot_encoder = model_data['onehot_encoder']
target_encoder = model_data['target_encoder']
scaler = model_data['scaler']


@app.get('/getparams')
async def getparams(url: str):
    match = re.search(r'flat/(\d{4,})', url)
    if not match or not (id := match.group(1)):
        raise HTTPException(status_code=400, detail=f'Неверный формат объявления')
    data = apartPage([id], dbinsert=0)
    data = Data(**data)
    response = preprocess(data)
    if isinstance(response, list):
        raise HTTPException(status_code=400, detail=f'Ошибка')
    return response.iloc[0].to_json(force_ascii=False)


@app.post('/getparams')
async def process_json(request: Data):
    X_train = preprocess(request)
    if isinstance(X_train, list):
        raise HTTPException(status_code=400, detail=f'В объявлении не указаны: {X}')
    return X_train.iloc[0].to_json(force_ascii=False)
    onehot_columns = ['county', 'flat_type', 'sale_type',
                      'category', 'material_type', 'travel_type']
    X_train_encoded = pd.DataFrame(onehot_encoder.transform(
        X_train[onehot_columns]), columns=onehot_encoder.get_feature_names_out(onehot_columns))
    X_train = pd.concat([X_train.drop(columns=onehot_columns).reset_index(
        drop=True), X_train_encoded], axis=1)

    ordinal_columns = {'repair_type': {'no': 0, 'cosmetic': 1, 'euro': 2, 'design': 3}}
    for col, mapping in ordinal_columns.items():
        X_train[col] = X_train[col].map(mapping)

    target_columns = ['district', 'project_type', 'metro']
    X_train[target_columns] = pd.DataFrame(target_encoder.transform(X_train[target_columns]), columns=target_columns)
    return X_train.to_json()
    # Scaler
    # X_train = pd.DataFrame(scaler.transform(X_train), columns=X_train.columns)

    pred = model.predict(X_train)
    return {"message": 'IZI', "X_data": pred}


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
