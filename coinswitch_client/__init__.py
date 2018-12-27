from coinswitch_client.APIClient import CoinSwitchClient


def v2_instant(api_key, ip):
    return CoinSwitchClient.v2_instant(api_key=api_key, ip=ip)


def v2_fixed(api_key, ip):
    return CoinSwitchClient.v2_fixed(api_key=api_key, ip=ip)


def v1(api_key, ip):
    return CoinSwitchClient.v1(api_key=api_key, ip=ip)
