from coinswitch_client.APIClient import CoinSwitchV2InstantClient, Address

if __name__ == '__main__':
    c = CoinSwitchV2InstantClient()

    print(c.coins())
    print(c.from_coin('btc'))
    print(c.to_coin('btc'))
    print(c.pairs('btc', 'eth'))
    r = c.rates('eth', 'btc')
    print(r)
    print('receied value = ' + str((1 * float(r.data()['rate'])) - float(r.data()['minerFee'])))
    r = c.order('btc', 'eth', Address('0xcc1bf6b0625bc23895a47f4991fdb7862e34a563').json(),
                Address('1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX').json(), quantity_from=1)
    print(r)
    print(c.order_status(r.data()['orderId']))
    print(c.orders())
