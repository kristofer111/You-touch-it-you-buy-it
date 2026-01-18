import httpx

class MerchantClient:
    def __init__(self, base_url='http://merchant-service:8000', timeout=5.0):
        self.__base_url = base_url
        self.__timeout = timeout

    def get_merchant_by_id(self, merchant_id):
        url = f'{self.__base_url}/merchants/{merchant_id}'
        try:
            with httpx.Client(timeout=self.__timeout) as client:
                response = client.get(url, headers={'Accept': 'application/json'})
                return {'data': response.json(), 'status_code': response.status_code}
        except httpx.ConnectError as exc:
            print(f'Connection error when connecting to {url}: {exc}')
            raise
