from coinswitch_client.APIClient import CoinSwitchV2InstantClient
from coinswitch_client.APIClient import Address


class StatusCode:
    STATUS_NO_DEPOSIT = "no_deposit"
    STATUS_CONFIRMING = "confirming"
    STATUS_EXCHANGING = "exchanging"
    STATUS_SENDING = "sending"
    STATUS_COMPLETE = "complete"
    STATUS_FAILED = "failed"
    STATUS_REFUNDED = "refunded"
    STATUS_TIMEOUT = "timeout"


class TransactionManager():
    orders = ["22222222-6c9e-4c53-9a6d-55e089aebd04",
              "11111111-6c9e-4c53-9a6d-55e089aebd04"
              "33333333-6c9e-4c53-9a6d-55e089aebd04",
              "44444444-6c9e-4c53-9a6d-55e089aebd04",
              "66666666-6c9e-4c53-9a6d-55e089aebd04",
              "88888888-6c9e-4c53-9a6d-55e089aebd04",
              "77777777-6c9e-4c53-9a6d-55e089aebd04",
              "55555555-6c9e-4c53-9a6d-55e089aebd04"]
    api_key = ""
    ip = ""

    def __init__(self, api_key="cRbHFJTlL6aSfZ0K2q7nj6MgV5Ih4hbA2fUG0ueO", ip="1.1.1.1"):
        self.api_key = api_key
        self.ip = ip
        self.api_client = CoinSwitchV2InstantClient(api_key=api_key, ip=ip)

    def convert(self, from_coin: str, to_coin: str, quantity: float, address_to: Address, address_refund: Address):
        if quantity <= 0:
            raise ValueError(
                'The quantity of ' + from_coin + ' you would like to convert to ' + to_coin + 'should be greater than 0')

        # Check that we can exchange from_coin to to_coin
        r = self.api_client.pairs(from_coin, to_coin)
        print(r)
        if not r.is_success() or not len(r.data()) > 0:
            raise ValueError(
                'Impossible to find an available convertion from ' + from_coin + ' to ' + to_coin + '(' + r.message() + ')')

        # Beyond this point we can convert at current rate
        r = self.api_client.order(from_coin, to_coin, address_to, address_refund, quantity)
        if not r.is_success():
            raise ValueError('Something when wrong ... (' + r.message() + ')')

        print("You are expected to deposit " + str(
            r.data()['expectedDepositCoinAmount']) + from_coin + 'to exchange address ' + str(
            r.data()['exchangeAddress']))
        self.orders.append(r.data()['orderId'])
        return r.data()

    def orders_status(self) -> 'dict':
        data = {}
        for order in self.orders:
            r = self.api_client.order_status(order)
            if not r.is_success():
                continue
            data[r.data()['orderId']] = r.data()['status']
            # print(r.data()['orderId'] + " : " + r.data()['status'])

        return data

    def pending_order(self):
        pending = {}
        for orderId, status in self.orders_status().items():
            if status == StatusCode.STATUS_CONFIRMING or status == StatusCode.STATUS_EXCHANGING or status == StatusCode.STATUS_NO_DEPOSIT or status == StatusCode.STATUS_SENDING:
                pending[orderId] = status

        return pending

    def finished_orders(self):
        finished = {}
        for orderId, status in self.orders_status().items():
            if status == StatusCode.STATUS_COMPLETE or status == StatusCode.STATUS_FAILED or status == StatusCode.STATUS_TIMEOUT or status == StatusCode.STATUS_REFUNDED:
                finished[orderId] = status

        return finished
