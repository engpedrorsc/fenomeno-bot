import requests
from datetime import datetime as dt
from math import trunc
import tweepy


def request_btc_price():
    response = requests.get('https://cointradermonitor.com/api/pbb/v1/ticker')
    data = response.json()
    # print(f'last: {data["last"]}, volume24h: {data["volume24h"]}')
    return data['last']


def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return trunc(number)

    factor = 10.0 ** decimals
    return trunc(number * factor) / factor


def eng_to_br(text, thousand='_', decimal='.'):
    return text.replace(decimal, ',').replace(thousand, '.')


def build_message(btc_amount, btc_current_price, inv_return, days_interval, annual_inv_return):
    fiat_amount = btc_amount * btc_current_price

    btc_amount = eng_to_br(f'{btc_amount:_.0f}')
    fiat_amount = eng_to_br(f'{fiat_amount:_.2f}')
    inv_return = eng_to_br(f'{inv_return:_.1%}')
    days_interval = eng_to_br(f'{days_interval:_}')
    if abs(annual_inv_return) < 1:
        annual_inv_return = eng_to_br(f'{annual_inv_return:_.1%}')
    else:
        annual_inv_return = eng_to_br(f'{annual_inv_return:_.0%}')

    text = f'Se o Fenômeno tivesse comprado bitcoin com o dinheiro da compra do Cruzeiro, hoje ele teria aproximadamente ₿{btc_amount} que valem R${fiat_amount}.\n\
Isso representa um retorno de {inv_return} em {days_interval} dias, o que equivale a {annual_inv_return} ao ano.'

    return text


def send_message(consumer_key, consumer_secret, key, secret, message):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    api = tweepy.API(auth)
    api.update_status(message)
    print(f'Tweet enviado [{dt.now()}]:\n{message}')
    return
