from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, create_model


class Baggage(BaseModel):
    id: str
    overWeight: bool
    amount: int
    unit: str
    weight: Optional[create_model('Weight', amount=(float, ...), unit=(str, ...))]
    code: str
    descriptions: List[str]
    registered: bool
    equipmentType: Optional[str]


class BaggagePricing(BaseModel):
    passengerIds: List[str]
    passengerTypes: List[Literal['ADT', 'CHD', 'INF']]
    purchaseType: str
    routeId: str
    baggages: List[Baggage]


class AncillariesPricing(BaseModel):
    airId: UUID
    baggagePricings: List[BaggagePricing]
    baggageDisabled: bool
    seatsDisabled: bool
    mealsDisabled: bool
    upgradesDisabled: bool
    loungesDisabled: bool
    fastTracksDisabled: bool
    petsDisabled: bool


class Order(BaseModel):
    ancillariesPricings: List[AncillariesPricing]


class BaggageSelection(BaseModel):
    passengerId: str
    routeId: str
    baggageIds: List[str]
    redemption: bool


class SkiAddRequest(BaseModel):
    booking_number: str
    passenger_id: str


class SkiAddResponse(BaseModel):
    shopping_cart: List[BaggageSelection]
