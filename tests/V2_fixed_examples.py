from CoinSwitchClient import CoinSwitchV2FixedClient
from CoinSwitchClient import Address

if __name__ == '__main__':
    c = CoinSwitchV2FixedClient()

    print(c.coins())
    print(c.from_coin('btc'))
    print(c.to_coin('btc'))
    print(c.pairs('btc', 'eth'))
    r = c.place_offer('btc', 'eth', quantity_from=0.3)
    print(r.is_success())
    print(r.data())
    print(r.code())
    print(r)
    r = c.order('btc', 'eth', r.data()['offerReferenceId'],
                          Address('0xcc1bf6b0625bc23895a47f4991fdb7862e34a563').json(),
                          Address('1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX').json(), quantity_from=0.2)
    print(r)
    print(c.order_status(r.data()['orderId']))
