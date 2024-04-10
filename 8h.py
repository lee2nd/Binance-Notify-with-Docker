from binance.client import Client
from pushover import Pushover
import time
import socket

class Binance():
    
    def __init__(self):
        
        self.api_key = 'YOUR_BINANCE_API_KEY'
        self.api_secret = 'YOUR_BINANCE_API_SECRET'
        self.client = Client(self.api_key,self.api_secret)

    def check_price(self, symbol, interval, drop_percentage):
        
        klines = self.client.futures_klines(symbol=symbol, interval=interval, limit=2)
        # get the current price and previous price  
        curr_close, prev_close = float(klines[-1][4]), float(klines[0][4])
        # calculate the price change percentage
        percentage_change = round(((curr_close-prev_close)/prev_close)*100, 3)
        print(f"{symbol[:-4]} change {percentage_change}% {interval} [{prev_close}⮕{curr_close}]")
        
        if abs(percentage_change) > drop_percentage:  
            if percentage_change < 0:
                return f"{symbol[:-4]} ⬇ {percentage_change*(-1)}% {interval} [{prev_close}⮕{curr_close}]"
            else:
                return f"{symbol[:-4]} ⬆ {percentage_change}% {interval} [{prev_close}⮕{curr_close}]"
        else:
            return "0"
        
# initialize object
b_obj = Binance()
po = Pushover("YOUR_PUSHOVER_API_TOKEN")
po.user("YOUR_PUSHOVER_USER_TOKEN")

sbl_lst = ['BTCUSDT','ETHUSDT']
retry_counter = 0

while retry_counter < 5:
    try:   

        time.sleep(3)  

        notify = 0
        
        for symbol in sbl_lst:
            
            # generate the price movement messages
            message = b_obj.check_price(symbol, Client.KLINE_INTERVAL_8HOUR, 1.75)
            
            if message != "0":
                # send pushover notify message
                msg = po.msg(message)
                msg.set("title", "Binance Price Notify")
                po.send(msg)
                notify += 1
                
        if notify > 0:
            time.sleep(1200)
            
    except socket.error as error:
        
        print("Connection Failed due to socket - {}").format(error)
        print("Attempting {} of 5").format(retry_counter)
        time.sleep(3)
        retry_counter += 1                    
