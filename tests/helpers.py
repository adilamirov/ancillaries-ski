def load_data(fixture_name) -> str:
    with open(f'tests/data/{fixture_name}', 'r') as f:
        return f.read()


class MockResponse:

    def __init__(self, data: dict, status: int = 200):
        self._data = data
        self._status = status

    async def __aenter__(self) -> 'MockResponse':
        return self

    async def __aexit__(self, *args):
        pass

    def status(self) -> int:
        return self._status

    async def json(self) -> dict:
        return self._data
