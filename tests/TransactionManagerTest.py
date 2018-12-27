from coinswitch_client.TransactionManager import TransactionManager
from coinswitch_client.APIClient import Address

if __name__ == '__main__':
    manager = TransactionManager()
    r = manager.convert('btc', 'ltc', 1, Address('0xcc1bf6b0625bc23895a47f4991fdb7862e34a563').json(),
                    Address('1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX').json())

    print(r)
    print(manager.orders_status())
    print(manager.pending_order())
    print(manager.finished_orders())
