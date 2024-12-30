from pydantic import BaseModel


class Offers(BaseModel):
    cian_id: int
    price: float
    category: str | None = None
    views_count: int | None = None
    photos_count: int | None = None
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

class PredictResponse(BaseModel):
    price: float
