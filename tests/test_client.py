import json

import pytest

from ancillaries_ski.client import Client
from ancillaries_ski.exceptions import AddBagsError
from ancillaries_ski.models import Order, BaggageSelection
from tests.helpers import load_data, MockResponse


@pytest.mark.asyncio
async def test_get_orders_success(mocker):
    response = json.loads(load_data(f'client/get_order/success_response.json'))
    expected_result = Order.parse_raw(load_data(f'client/get_order/success_expected.json'))

    client = Client(host='http://localhost')
    mocker.patch.object(client.http_session, 'get', return_value=MockResponse(response))

    order = await client.get_order('AAAAAAAA', 'ivanov')

    assert order == expected_result


@pytest.mark.asyncio
async def test_add_bags_success(mocker):
    selection = json.loads(load_data('client/add_bags/selection.json'))
    selection = [BaggageSelection.parse_obj(i) for i in selection]

    response = json.loads(load_data('client/add_bags/success_response.json'))

    expected_result = json.loads(load_data('client/add_bags/success_expected.json'))
    expected_result = [BaggageSelection.parse_obj(i) for i in expected_result]

    client = Client(host='http://localhost')
    mocker.patch.object(client.http_session, 'put', return_value=MockResponse(response))

    shopping_cart = await client.add_bags(selection)

    assert shopping_cart == expected_result


@pytest.mark.asyncio
async def test_add_bags_error(mocker):
    selection = json.loads(load_data('client/add_bags/selection.json'))
    selection = [BaggageSelection.parse_obj(i) for i in selection]

    response = json.loads(load_data('client/add_bags/error_response.json'))

    client = Client(host='http://localhost')
    mocker.patch.object(client.http_session, 'put', return_value=MockResponse(response))

    try:
        await client.add_bags(selection)
    except AddBagsError as exc:
        assert exc.code == response['error']['code']
        assert exc.message == response['error']['message']
    else:
        assert False, 'exception should be raised'
