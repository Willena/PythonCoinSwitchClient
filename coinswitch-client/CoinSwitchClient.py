import json

import requests


class Address:
    address = ""
    flag = ""

    def __init__(self, address: str, flag=""):
        self.address = address
        self.flag = flag

    def json(self):
        return self.__dict__


class ApiResponse:
    source_data = None

    def __init__(self, text_response: str = None, json_response: json = None):

        if text_response is not None and type(text_response) is str:
            self.source_data = json.loads(text_response)
        elif json_response is not None and type(json_response) is dict:
            self.source_data = json_response

    def is_success(self):
        if self.source_data is None:
            return False

        return self.source_data['success']

    def code(self):
        return self.source_data['code'] if self.source_data is not None else ""

    def data(self):
        return self.source_data['data'] if self.source_data is not None else ""

    def __str__(self):
        return str(self.source_data)


class ApiResponseV1(ApiResponse):
    def __init__(self, text_response: str = None, json_response: json = None):
        ApiResponse.__init__(text_response=text_response, json_response=json_response)

    def message(self):
        return self.source_data['msg'] if self.source_data is not None else ""


class ApiResponseV2(ApiResponse):
    def __init__(self, text_response: str = None, json_response: json = None):
        ApiResponse.__init__(self, text_response=text_response, json_response=json_response)


class CoinSwitchClient:
    ip = ""
    api_key = ""
    api_url = ""

    def __init__(self, ip="1.1.1.1", api_key="cRbHFJTlL6aSfZ0K2q7nj6MgV5Ih4hbA2fUG0ueO"):
        self.api_key = api_key
        self.ip = ip
        self.api_url = self.get_api_url()
        self.headers = self.generate_headers()

    @classmethod
    def v2_fixed(cls, api_key="cRbHFJTlL6aSfZ0K2q7nj6MgV5Ih4hbA2fUG0ueO", ip="1.1.1.1") -> 'CoinSwitchV2Client':
        return CoinSwitchV2FixedClient(api_key=api_key, ip=ip)

    @classmethod
    def v2_instant(cls, api_key="cRbHFJTlL6aSfZ0K2q7nj6MgV5Ih4hbA2fUG0ueO", ip="1.1.1.1") -> 'CoinSwitchV2Client':
        return CoinSwitchV2InstantClient(api_key=api_key, ip=ip)

    @classmethod
    def v1(cls, api_key="cRbHFJTlL6aSfZ0K2q7nj6MgV5Ih4hbA2fUG0ueO", ip="1.1.1.1") -> 'CoinSwitchV1Client':
        return CoinSwitchV1Client(api_key=api_key, ip=ip)

    @classmethod
    def get_api_url(cls):
        return "https://api.coinswitch.co/"

    def generate_headers(self):
        return {
            'x-api-key': self.api_key,
            'x-user-ip': self.ip
        }


class CoinSwitchV1Client(CoinSwitchClient):

    def __init__(self, api_key="cRbHFJTlL6aSfZ0K2q7nj6MgV5Ih4hbA2fUG0ueO", ip="1.1.1.1"):
        CoinSwitchClient.__init__(self, api_key=api_key, ip=ip)

    @classmethod
    def get_api_url(cls):
        return CoinSwitchClient.get_api_url() + "v1/"

    def coins(self):
        return ApiResponseV1(json_response=requests.get(self.api_url + "coins", headers=self.headers).json())

    def from_coin(self, coin: str):
        return ApiResponseV1(json_response=requests.get(self.api_url + "coins/" + coin + "/deposit-coins",
                                                        headers=self.headers).json())

    def to_coin(self, coin: str):
        return ApiResponseV1(json_response=requests.get(self.api_url + "coins/" + coin + "/destination-coins",
                                                        headers=self.headers).json())

    def retrieve_limit_for(self, from_coin: str, to_coin: str):
        data = {
            'depositCoin': from_coin,
            'destinationCoin': to_coin
        }
        return ApiResponseV1(
            json_response=requests.post(self.api_url + "limit", data=json.dumps(data), headers=self.headers).json())

    def place_offer_for(self, from_coin: str, to_coin: str, quantity: float):
        data = {
            'depositCoin': from_coin,
            'destinationCoin': to_coin,
            'depositCoinAmount': quantity
        }
        return ApiResponseV1(
            json_response=requests.post(self.api_url + "offer", data=json.dumps(data), headers=self.headers).json())

    def place_order_for(self, from_coin: str, to_coin: str, quantity: float, offer_id: str, user_id: str,
                        to_adress: Address, refund_address: Address):
        data = {
            'depositCoin': from_coin,
            'destinationCoin': to_coin,
            'depositCoinAmount': quantity,
            'offerReferenceId': offer_id,
            'userReferenceId': user_id,
            'destinationAddress': to_adress,
            'refundAddress': refund_address
        }
        return ApiResponseV1(
            json_response=requests.post(self.api_url + "order", data=json.dumps(data), headers=self.headers).json())

    def order_status(self, order_id: str):
        return ApiResponseV1(
            json_response=requests.get(self.api_url + "order/" + order_id, headers=self.headers).json())


class CoinSwitchV2FixedClient(CoinSwitchClient):
    is_fixed = False

    def __init__(self, api_key="cRbHFJTlL6aSfZ0K2q7nj6MgV5Ih4hbA2fUG0ueO", ip="1.1.1.1"):
        CoinSwitchClient.__init__(self, api_key=api_key, ip=ip)
        self.api_url = self.get_api_url()

    def coins(self):
        return ApiResponseV2(json_response=requests.get(self.api_url + "coins", headers=self.headers).json())

    def pairs(self, from_coin: str = None, to_coin: str = None):
        data = {}
        if from_coin is not None:
            data['depositCoin'] = from_coin

        if to_coin is not None:
            data['destinationCoin'] = to_coin

        return ApiResponseV2(
            json_response=requests.post(self.api_url + "pairs", data=json.dumps(data), headers=self.headers).json())

    def from_coin(self, from_coin: str):
        return self.pairs(from_coin=from_coin)

    def to_coin(self, to_coin: str):
        return self.pairs(to_coin=to_coin)

    def place_offer(self, from_coin: str, to_coin: str, quantity_from: float = None, quantity_to: float = None):
        data = {
            'depositCoin': from_coin,
            'destinationCoin': to_coin
        }

        if quantity_from is not None and quantity_to is not None:
            raise ValueError(
                'You must specify one of depositCoinAmount OR destinationCoinAmount to fetch a fixed rate offer')

        if quantity_from is not None:
            data['depositCoinAmount'] = quantity_from

        if quantity_to is not None:
            data['destinationCoinAmount'] = quantity_to

        return ApiResponseV2(
            json_response=requests.post(self.get_api_url() + "offer", data=json.dumps(data),
                                        headers=self.headers).json())

    def order(self, from_coin: str, to_coin: str, offer_id: str, to_address: Address, refund_adress: Address,
              quantity_from: float = None, quantity_to: float = None, ):

        data = {
            'offerReferenceId': offer_id,
            'depositCoin': from_coin,
            'destinationCoin': to_coin,
            'destinationAddress': to_address,
            'refundAddress': refund_adress
        }

        if quantity_from is not None and quantity_to is not None:
            raise ValueError(
                'You must specify one of depositCoinAmount OR destinationCoinAmount to fetch a fixed rate offer')

        if quantity_from is not None:
            data['depositCoinAmount'] = quantity_from

        if quantity_to is not None:
            data['destinationCoinAmount'] = quantity_to

        return ApiResponseV2(json_response=requests.post(self.get_api_url() + "order", data=json.dumps(data),
                                                         headers=self.headers).json())

    def order_status(self, order_id: str):
        return ApiResponseV2(
            json_response=requests.get(self.get_api_url() + "order/" + order_id, headers=self.headers).json())

    @classmethod
    def get_api_url(cls):
        return CoinSwitchClient.get_api_url() + "v2/fixed/"


class CoinSwitchV2InstantClient(CoinSwitchClient):
    def __init__(self, api_key="cRbHFJTlL6aSfZ0K2q7nj6MgV5Ih4hbA2fUG0ueO", ip="1.1.1.1"):
        CoinSwitchClient.__init__(self, api_key=api_key, ip=ip)

    @classmethod
    def get_api_url(cls):
        return CoinSwitchClient.get_api_url() + "v2/"

    def coins(self):
        return ApiResponseV2(json_response=requests.get(self.api_url + "coins", headers=self.headers).json())

    def pairs(self, from_coin: str = None, to_coin: str = None):
        data = {}
        if from_coin is not None:
            data['depositCoin'] = from_coin

        if to_coin is not None:
            data['destinationCoin'] = to_coin

        return ApiResponseV2(
            json_response=requests.post(self.api_url + "pairs", data=json.dumps(data), headers=self.headers).json())

    def from_coin(self, from_coin: str):
        return self.pairs(from_coin=from_coin)

    def to_coin(self, to_coin: str):
        return self.pairs(to_coin=to_coin)

    def rates(self, from_coin: str, to_coin: str):
        data = {
            'depositCoin': from_coin,
            'destinationCoin': to_coin
        }
        return ApiResponseV2(json_response=requests.post(self.api_url + "rate", data=json.dumps(data), headers=self.headers).json())

    def order(self, from_coin: str, to_coin: str, to_address: Address, refund_adress: Address,
              quantity_from: float = None, quantity_to: float = None, ):

        data = {
            'depositCoin': from_coin,
            'destinationCoin': to_coin,
            'destinationAddress': to_address,
            'refundAddress': refund_adress
        }

        if quantity_from is not None and quantity_to is not None:
            raise ValueError(
                'You must specify one of depositCoinAmount OR destinationCoinAmount to fetch a fixed rate offer')

        if quantity_from is not None:
            data['depositCoinAmount'] = quantity_from

        if quantity_to is not None:
            data['destinationCoinAmount'] = quantity_to

        return ApiResponseV2(json_response=requests.post(self.api_url + "order", data=json.dumps(data),
                                                         headers=self.headers).json())

    def orders(self):
        return ApiResponseV2(json_response=requests.get(self.api_url + "orders", headers=self.headers).json())

    def order_status(self, order_id: str):
        return ApiResponseV2(
            json_response=requests.get(self.get_api_url() + "order/" + order_id, headers=self.headers).json())
