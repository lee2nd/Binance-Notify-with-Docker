from binance.client import Client
import time
import socket
import requests


class Binance:
    def __init__(self, api_key, api_secret):
        """
        Initializes the Binance object.

        Args:
            api_key (str): The API key for the Binance API.
            api_secret (str): The API secret for the Binance API.
        """
        # Set the API key and secret
        self.api_key = api_key
        self.api_secret = api_secret

        # Create a Binance client object
        self.client = Client(self.api_key, self.api_secret)

    def check_price(self, symbol, interval, drop_percentage):
        """
        Checks the price change of a symbol.

        Args:
            symbol (str): The symbol to check.
            interval (str): The time interval to check.
            drop_percentage (int): The percentage change to trigger a notification.

        Returns:
            str: A message if the price change is greater than the drop percentage, otherwise "0".
        """
        # Get the last two klines
        klines = self.client.futures_klines(symbol=symbol, interval=interval, limit=2)
        
        # Calculate the current and previous close prices
        curr_close, prev_close = map(float, (klines[-1][4], klines[0][4]))
        
        # Calculate the percentage change
        percentage_change = round(((curr_close - prev_close) / prev_close) * 100, 3)
        
        # Build the message
        message = f"{symbol[:-4]} change {percentage_change}% {interval} [{prev_close}⮕{curr_close}]"
        print(message)
        
        # Check if the percentage change is greater than the drop percentage
        if abs(percentage_change) > drop_percentage:
            # Determine the direction of the change
            symbol_direction = "⬇" if percentage_change < 0 else "⬆"
            return f"{symbol[:-4]} {symbol_direction} {abs(percentage_change)}% {interval} [{prev_close}⮕{curr_close}]"
        else:
            # Return "0" if the percentage change is not greater than the drop percentage
            return "0"


def lineNotifyMessage(token, msg):
    """
    Sends a message using Line Notify API.

    Args:
        token (str): The Line Notify API token.
        msg (str): The message to be sent.

    Returns:
        int: The status code of the response.
    """

    # Set the headers for the request
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Set the payload for the request
    payload = {"message": msg}

    # Send a POST request to the Line Notify API with the headers and payload
    r = requests.post(
        "https://notify-api.line.me/api/notify", headers=headers, params=payload
    )

    # Return the status code of the response
    return r.status_code


# initialize object
b_obj = Binance(api_key='MYgUFxFMjeVglbzUsips2x38QR11XNJQ5NuYVbov3QBITOcyYmnBGA3MtuHTegWY',
                api_secret='tOfsgUFcmjb1odifv2F1z4gYjl8Fvbzr5xjbQmiMbNSZnADjRcpCuToHp1H0R2x7')
token = "G68BgzaWHmFGUJUm4VAnyHS1w3oRFu2n1fgBiCqkTHE"

sbl_lst = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
retry_counter = 0

while retry_counter < 5:
    try:

        time.sleep(3)

        notify = 0

        for symbol in sbl_lst:

            # generate the price movement messages
            message = b_obj.check_price(symbol, Client.KLINE_INTERVAL_1HOUR, 1)

            if message != "0":
                # send pushover notify message
                lineNotifyMessage(token, message)
                notify += 1

        if notify > 0:
            time.sleep(180)

    except socket.error as error:

        print("Connection Failed due to socket - {}").format(error)
        print("Attempting {} of 5").format(retry_counter)
        time.sleep(3)
        retry_counter += 1