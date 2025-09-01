from oandapyV20 import API


def get_client(token: str) -> API:
    """Return an authenticated Oanda API client."""
    return API(access_token=token)
