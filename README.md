# A Simple python library for coinswitch

This is a simple library that uses coinswitch APIs. 
It is just a collection of utils to manipulate, interpret and simplify calls to their APIs 

## How to use

First install the package with pip

```
pip install coinswitch-client
```

Then be sure to have your API key. If not it defaults to a sandbox api key
There are two major blocks inside this package:
1. `TransactionManager` : it is a set of function that call the v2 instant API
2. `CoinSwitchV1Client` : function that reflect the v1 coinswitch api
3. `CoinSwitchV2FixedClient` : function that reflect the v2 fixed coinswitch api
4. `CoinSwitchV2InstantClient` : function that reflect the v2 instant coinswitch api
5. `ApiResponse` : an object that represent the reponse from coinswitch apis

You can find examples inside the `test` directory of this repo. 

#### Usage of ApiResponse

You never have to crete this object, but it will be return by each api calls.
Here is the global structure of an ApiResponse

```json
{
  "success": true,
  "code": "",
  "data": "",
  "error": ""
}
```

The ApiResponse object provide simple method to access basic information

```python

api_response.is_success() # returns a boolean
api_response.code() # return the code string in the "code" field
api_response.message() # returns the content of error or msg depending on the remote response
api_response.data() # return a dict object that represent the data

```

Please see https://developer.coinswitch.co/ for any information of the returned fields in the data message

#### Usage for TransactionManager

```python

# import required modules and classes
from coinswitch_client.TransactionManager import TransactionManager
from coinswitch_client.APIClient import Address

# create an instance of the transaction manager
manager = TransactionManager(api_key="MY_API_KEY")

# Ask to convert 1 BTC to ETH with 
manager.convert('btc', 'eth', 1.0, Address('ETH_ADDRESS').json(),
                    Address('REFUND_ADDRESS').json())
                    
#this function returns the response from the coinswitch api as a ApiResponse
```

#### Usage for CoinSwitchV1Client

It follows the https://developer.coinswitch.co/ apis
Here is a simple usage though

```python
from coinswitch_client.APIClient import CoinSwitchV1Client

client = CoinSwitchV1Client(api_key="MYKEY")
api_response = client.coins()
if api_response.is_success():
    print(api_response.data())

```

#### Usage for CoinSwitchV2InstantClient

It follows the https://developer.coinswitch.co/ apis
Here is a simple usage though

```python
from coinswitch_client.APIClient import CoinSwitchV2InstantClient

client = CoinSwitchV2InstantClient(api_key="MYKEY")
api_response = client.coins()
if api_response.is_success():
    print(api_response.data())
    
api_response = client.rates('btc', 'eth')
if api_response.is_success():
    print(api_response.data())

```
#### Usage for CoinSwitchV2FixedClient

It follows the https://developer.coinswitch.co/ apis
Here is a simple usage though

```python
from coinswitch_client.APIClient import CoinSwitchV2FixedClient

client = CoinSwitchV2FixedClient(api_key="MYKEY")
api_response = client.coins()
if api_response.is_success():
    print(api_response.data())
    
api_response = client.place_offer('btc', 'eth',quantity_from=1.0)
if api_response.is_success():
    print(api_response.data())

```