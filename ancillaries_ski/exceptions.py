class ClientError(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def json(self) -> dict:
        return {
            'code': self.code,
            'message': self.message,
        }


class AddBagsError(ClientError):
    pass
