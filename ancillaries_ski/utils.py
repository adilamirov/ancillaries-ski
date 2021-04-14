from typing import List

from ancillaries_ski.models import Order, BaggageSelection


def select_ski_ancillaries(order: Order) -> List[BaggageSelection]:
    selections: List[BaggageSelection] = []

    for air_pricing in order.ancillariesPricings:
        for route_pricing in air_pricing.baggagePricings:
            baggage_ids = [b.id for b in route_pricing.baggages if b.equipmentType == 'ski']

            for passenger_id in route_pricing.passengerIds:
                selections.append(
                    BaggageSelection(
                        passengerId=passenger_id,
                        routeId=route_pricing.routeId,
                        baggageIds=baggage_ids,
                        redemption=False
                    )
                )

    return selections
