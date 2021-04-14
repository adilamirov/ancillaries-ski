from fastapi import APIRouter, Depends

from ancillaries_ski.client import Client
from ancillaries_ski.dependencies import get_client
from ancillaries_ski.models import SkiAddRequest, SkiAddResponse
from ancillaries_ski.utils import select_ski_ancillaries

router = APIRouter()


@router.put('/', response_model=SkiAddResponse)
async def add(
        ski_add_request: SkiAddRequest,
        client: Client = Depends(get_client)
) -> SkiAddResponse:
    order = await client.get_order(
        ski_add_request.booking_number,
        ski_add_request.passenger_id
    )

    baggage_selections = select_ski_ancillaries(order)

    shopping_cart = await client.add_bags(baggage_selections)

    return SkiAddResponse(shopping_cart=shopping_cart)
