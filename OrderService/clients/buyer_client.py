import httpx

class BuyerClient:
    def __init__(self, base_url='http://buyer-service:8000', timeout=5.0):
        self.__base_url = base_url
        self.__timeout = timeout

    def get_buyer_by_id(self, buyer_id):
        url = f"{self.__base_url}/buyers/{buyer_id}"
        try:
            with httpx.Client(timeout=self.__timeout) as client:
                response = client.get(url, headers={"Accept": "application/json"})
                return {'data': response.json(), 'status_code': response.status_code}
        except httpx.ConnectError as exc:
            print(f"Connection error when connecting to {url}: {exc}")
            raise
