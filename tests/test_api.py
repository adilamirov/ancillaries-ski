import json

import pytest
from fastapi.testclient import TestClient

from ancillaries_ski.exceptions import AddBagsError
from ancillaries_ski.models import Order, BaggageSelection
from tests.helpers import load_data


@pytest.mark.parametrize(
    'test_case',
    [
        'simple_success',
    ]
)
def test_add_success(mocker, app, client, test_case):
    payload = json.loads(load_data(f'api/add/{test_case}/request.json'))
    expected_response = json.loads(load_data(f'api/add/{test_case}/response.json'))

    order = Order.parse_raw(load_data(f'api/add/{test_case}/order.json'))

    shopping_cart = json.loads(load_data(f'api/add/{test_case}/shopping_cart.json'))
    shopping_cart = [BaggageSelection.parse_obj(i) for i in shopping_cart]

    mocker.patch.object(client, 'get_order', return_value=order)
    mocker.patch.object(client, 'add_bags', return_value=shopping_cart)

    test_client = TestClient(app)

    response = test_client.put('/', json=payload)

    assert response.json() == expected_response


@pytest.mark.parametrize(
    'test_case, error_code, error_message',
    [
        ('simple_error',
         'conversation.not.found', 'Давайте начнем новый поиск и обновим результаты.'),
    ]
)
def test_add_error(mocker, app, client, test_case, error_code, error_message):
    payload = json.loads(load_data(f'api/add/{test_case}/request.json'))
    expected_response = json.loads(load_data(f'api/add/{test_case}/response.json'))

    order = Order.parse_raw(load_data(f'api/add/{test_case}/order.json'))
    exception = AddBagsError(code=error_code, message=error_message)

    mocker.patch.object(client, 'get_order', return_value=order)
    mocker.patch.object(client, 'add_bags', side_effect=exception)

    test_client = TestClient(app)

    response = test_client.put('/', json=payload)

    assert response.json() == expected_response
