import hashlib
import json
import time
from curl_cffi import requests

def md5(value: str) -> str:
    """
    Generate the MD5 hash of a given string.
    
    Args:
        value (str): The input string to hash.

    Returns:
        str: The MD5 hash of the input string.
    """
    return hashlib.md5(value.encode('utf-8')).hexdigest()

def mexc_crypto(key: str, obj: dict) -> dict:
    """
    Generate signature for API request to MEXC.

    Args:
        key (str): API key for authentication.
        obj (dict): Data to be signed.

    Returns:
        dict: A dictionary containing the generated 'time' and 'sign'.
    """
    date_now = str(int(time.time() * 1000))  
    g = md5(key + date_now)[7:] 
    s = json.dumps(obj, separators=(',', ':'))  
    sign = md5(date_now + s + g)  
    return {'time': date_now, 'sign': sign}

def place_order(key: str, obj: dict) -> dict:
    """
    Place a new order on the MEXC futures platform.

    Args:
        key (str): API key for authentication.
        obj (dict): Order details (e.g., symbol, side, price, volume).

    Returns:
        dict: Response from the API.
    """
    url = 'https://futures.mexc.com/api/v1/private/order/create'  
    signature = mexc_crypto(key, obj)
    headers = {
        'Content-Type': 'application/json',
        'x-mxc-sign': signature['sign'],
        'x-mxc-nonce': signature['time'],
        'Authorization': key
    }
    response = requests.post(url, headers=headers, json=obj, impersonate="chrome")
    return response.json()

def cancel_order(key: str, orders_id_list: list) -> dict:
    """
    Cancel specific orders on the MEXC futures platform.

    Args:
        key (str): API key for authentication.
        orders_id_list (list): List of order IDs to cancel.

    Returns:
        dict: Response from the API.
    """
    url = 'https://futures.mexc.com/api/v1/private/order/cancel'  
    signature = mexc_crypto(key, orders_id_list)
    headers = {
        'Content-Type': 'application/json',
        'x-mxc-sign': signature['sign'],
        'x-mxc-nonce': signature['time'],
        'Authorization': key
    }   
    response = requests.post(url, headers=headers, json=orders_id_list, impersonate="chrome")
    return response.json()

def cancel_all(key: str) -> dict:
    """
    Cancel all active orders on the MEXC futures platform.

    Args:
        key (str): API key for authentication.

    Returns:
        dict: Response from the API.
    """
    url = 'https://futures.mexc.com/api/v1/private/order/cancel_all'  
    signature = mexc_crypto(key, {})
    headers = {
        'Content-Type': 'application/json',
        'x-mxc-sign': signature['sign'],
        'x-mxc-nonce': signature['time'],
        'Authorization': key
    }
    response = requests.post(url, headers=headers, json={}, impersonate="chrome")
    return response.json()

def market_cancel_all(key:str):
    url="https://futures.mexc.com/api/v1/private/position/close_all"
    signature = mexc_crypto(key, {})
    headers = {
        'Content-Type': 'application/json',
        'x-mxc-sign': signature['sign'],
        'x-mxc-nonce': signature['time'],
        'Authorization': key
    }
    response = requests.post(url, headers=headers, json={}, impersonate="chrome")
    return response.json()

def edit_order(key: str, obj: dict, order_type: str = "limit_order") -> dict:
    """
    Edit an existing order on the MEXC futures platform.

    Args:
        key (str): API key for authentication.
        obj (dict): Updated order details (e.g., orderId, new price, volume).
        order_type (str): Type of order to change (default is 'limit_order').

    Returns:
        dict: Response from the API.
    """
    url = f'https://futures.mexc.com/api/v1/private/order/change_{order_type}'
    signature = mexc_crypto(key, obj)
    headers = {
        'Content-Type': 'application/json',
        'x-mxc-sign': signature['sign'],
        'x-mxc-nonce': signature['time'],
        'Authorization': key
    }
    response = requests.post(url, headers=headers, json=obj, impersonate="chrome")
    return response.json()



def get_vol_from_volume( volume ,fair_price, contract_size):
    return volume / (fair_price * contract_size)
def get_symbol_contract_size(key,symbol):
    url = 'https://futures.mexc.com/api/v1/contract/detail'  
    headers = {
        'Content-Type': 'application/json',
        'Authorization': key
    }

    response = requests.get(url, headers=headers,impersonate="chrome")
    data=response.json()["data"]
    for symbol_data in data:
        if symbol_data["symbol"]==symbol:
            return symbol_data['contractSize']



def get_balance(key):
    url = 'https://futures.mexc.com/api/v1/private/account/assets'  
    headers = {
        'Content-Type': 'application/json',

        'Authorization': key
    }
    response = requests.get(url, headers=headers,impersonate="chrome")
    return response.json()


#USAGE EXAMPLE 
key = 'WEBfd0ebc32a48868f59905a0d05d2cbc238ed9e5402f460dda8f41ae82ac776c0d'



obj={
    "symbol": "BTC_USDT",
    "side": 1,
    "openType": 1,
    "type": 1,
    "leverage": 10,
    "vol":10,
    "price": 2.5,
}




print(place_order(key,obj))


