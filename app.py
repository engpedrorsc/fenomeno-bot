from my_functions import *
from tt_keys import *
from datetime import datetime as dt


bad_inv_value = 400000000
bad_inv_date = dt(2021, 12, 18)
bad_inv_btc_close_price = 268280.49
good_inv_amount = truncate(bad_inv_value / bad_inv_btc_close_price, 8)
current_btc_price = request_btc_price()

current_good_inv_value = good_inv_amount * current_btc_price
current_good_inv_return = current_good_inv_value / bad_inv_value - 1
good_inv_interval = int((dt.now() - bad_inv_date).days)
current_good_inv_annual_return = pow(
    1 + current_good_inv_return, 365/good_inv_interval)-1

message = build_message(good_inv_amount, current_btc_price,
                        current_good_inv_return, good_inv_interval, current_good_inv_annual_return)

send_message(consumer_key, consumer_secret, key, secret, message)
