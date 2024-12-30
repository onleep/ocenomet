from pydantic import BaseModel
from typing import List, Dict, Literal


class Offers(BaseModel):
    cian_id: int
    price: float
    category: str | None = 'flatSale'
    views_count: int | None = 632
    photos_count: int | None = 18
    floor_number: int | None = None
    floors_count: int | None = None
    publication_at: int | None = None
    # price_changes: list | None = None


class Addresses(BaseModel):
    cian_id: int
    county: str | None = None
    district: str | None = None
    street: str | None = None
    house: str | None = None
    metro: str | None = None
    travel_type: str | None = None
    travel_time: int | None = None
    # address: list | None = None
    coordinates: dict | None = None


class RealtyInside(BaseModel):
    cian_id: int
    repair_type: str | None = 'cosmetic'
    total_area: float | None = None
    living_area: float | None = None
    kitchen_area: float | None = None
    ceiling_height: float | None = None
    balconies: int | None = 0
    loggias: int | None = 0
    rooms_count: int | None = None
    separated_wc: float | None = 0
    combined_wc: int | None = 0
    windows_view: str | None = None


class RealtyOutside(BaseModel):
    cian_id: int
    build_year: int | None = None
    entrances: int | None = None
    material_type: str | None = 'panel'
    parking_type: str | None = None
    garbage_chute: bool | None = False
    lifts_count: int | None = None
    passenger_lifts: int | None = 0
    cargo_lifts: int | None = None


class RealtyDetails(BaseModel):
    cian_id: int
    realty_type: str | None = None
    project_type: str | None = 'Индивидуальный проект'
    heat_type: str | None = None
    gas_type: str | None = None
    is_apartment: bool | None = False
    is_penthouse: bool | None = False
    is_mortgage_allowed: bool | None = False
    is_premium: bool | None = False
    is_emergency: bool | None = False
    renovation_programm: bool | None = False
    finish_date: dict | None = None


class OffersDetails(BaseModel):
    cian_id: int
    agent_name: str | None = None
    deal_type: str | None = None
    flat_type: str | None = None
    sale_type: str | None = 'free'
    # is_duplicate: bool | None = None
    description: str | None = None


class Developers(BaseModel):
    cian_id: int
    name: str | None = None
    review_count: int | None = None
    total_rate: float | None = None
    buildings_count: int | None = None
    foundation_year: int | None = None
    is_reliable: bool | None = None


class Params(BaseModel):
    offers: Offers
    addresses: Addresses
    realty_inside: RealtyInside
    realty_outside: RealtyOutside
    realty_details: RealtyDetails
    offers_details: OffersDetails
    developers: Developers
    
class Predict(Offers, Addresses, RealtyInside, RealtyOutside, RealtyDetails, OffersDetails, Developers):
    distance_from_center: float | None = None
    cian_id: int | None = None
    price: float | None = None

class PredictReq(BaseModel):
    id: str | None = None
    data: Predict

class PredictResponse(BaseModel):
    price: float

class ModelConfig(BaseModel):
    id: str
    ml_model_type: Literal['lr', 'ls', 'rg']
    hyperparameters: Dict[str, str | int | float | bool] = {}


class FitRequest(BaseModel):
    X: List[dict]
    y: List[dict]
    config: ModelConfig


class ModelList(BaseModel):
    models: List[dict]


class PredictionResponse(BaseModel):
    predictions: List[int | float | bool]


class LoadRequest(BaseModel):
    id: str


class MessageResponse(BaseModel):
    message: str
