from typing import List

import aiohttp as aiohttp

from ancillaries_ski.exceptions import AddBagsError
from ancillaries_ski.models import Order, BaggageSelection


class Client:
    def __init__(self, host):
        self.host = host
        self.http_session = aiohttp.ClientSession()

    @property
    def orders_url(self) -> str:
        return self._build_url('orders')

    @property
    def bags_url(self) -> str:
        return self._build_url('bags')

    def _build_url(self, endpoint: str) -> str:
        return f'{self.host}/{endpoint}'

    async def close(self):
        await self.http_session.close()

    async def get_order(self, booking_number: str, passenger_id: str) -> Order:
        query_params = {
            'booking_number': booking_number,
            'passenger_id': passenger_id,
        }

        async with self.http_session.get(self.orders_url, params=query_params) as resp:
            # TODO: add error handling

            return Order.parse_obj(await resp.json())

    async def add_bags(self, baggage_selections: List[BaggageSelection]) -> List[BaggageSelection]:
        payload = {
            'baggageSelections': [b.dict() for b in baggage_selections]
        }

        async with self.http_session.put(self.bags_url, payload=payload) as resp:
            resp_json = await resp.json()

            if error := resp_json.get('error'):
                raise AddBagsError(
                    code=error['code'],
                    message=error['message']
                )

            shopping_cart = resp_json['shoppingCart']

            return [BaggageSelection.parse_obj(i) for i in shopping_cart]
