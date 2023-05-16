import requests
from plyer import notification
from PIL import Image


def get_bitcoin_price():
    url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"
    response = requests.get(url)
    data = response.json()
    price = data["USD"]
    return price


def show_notification(bitcoin_price):
    filename = 'btc_icon.png'
    img = Image.open(filename, 'r')
    img.save('btc_icon.ico')
    notification.notify(
        title = 'Reminder',
        message = f"The current price of Bitcoin is: {bitcoin_price} USD",
        app_icon = 'btc_icon.ico',
        timeout = 10
    )

bitcoin_price = get_bitcoin_price()
message = f"The current price of Bitcoin is: {bitcoin_price}"
print(message)
show_notification(message)