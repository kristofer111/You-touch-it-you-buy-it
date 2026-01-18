import httpx

class OrderClient:
    def __init__(self, base_url='http://order-service:8000', timeout=5.0):
        self.__base_url = base_url
        self.__timeout = timeout

    def get_order_by_id(self, order_id: int):
        url = f'{self.__base_url}/orders/{order_id}'
        try:

            with httpx.Client(timeout=self.__timeout) as client:
                response = client.get(url, headers={'Accept': 'application/json'})
                return {'data': response.json(), 'status_code': response.status_code}

        except httpx.ConnectError as exc:
            print(f'Connection error when connecting to {url}: {exc}')
            raise

    def create_new_order(self, order: dict):
        url = f'{self.__base_url}/orders'
        try:

            with httpx.Client(timeout=self.__timeout) as client:
                response = client.post(url, json=order, headers={'Accept': 'application/json'})
                return {'data': response.json(), 'status_code': response.status_code}

        except httpx.ConnectError as exc:
            print(f'Connection error when connecting to {url}: {exc}')
            raise