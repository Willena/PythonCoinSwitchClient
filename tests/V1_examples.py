from coinswitch_client.APIClient import CoinSwitchV1Client, Address

if __name__ == '__main__':
    c = CoinSwitchV1Client()

    print(c.coins())
    print(c.from_coin('btc'))
    print(c.to_coin('btc'))
    print(c.retrieve_limit_for('btc', 'eth'))
    r = c.place_offer_for('btc', 'eth', 0.3)
    print(r.is_success())
    print(r.data())
    print(r.code())
    print(r.message())
    print(r)
    r = c.place_order_for('btc', 'eth', 0.3, r.data()['offerReferenceId'], 1,
                          Address('0xcc1bf6b0625bc23895a47f4991fdb7862e34a563').json(),
                          Address('1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX').json())
    print(r)
    print(c.order_status(r.data()['orderId']))
