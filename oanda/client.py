"""Basic Oanda API client wrapper."""

from oandapyV20 import API


class OandaClient:
    """Manage authentication and requests to the Oanda REST API."""

    def __init__(self, token: str) -> None:
        """Initialise the underlying API client with the provided token."""
        self._api = API(access_token=token)

    def request(self, endpoint) -> dict:
        """Execute a prepared endpoint request and return the response."""
        self._api.request(endpoint)
        return endpoint.response


__all__ = ["OandaClient"]

