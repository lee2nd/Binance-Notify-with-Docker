# Reference

Binance API Token: https://algotrading101.com/learn/binance-python-api-guide/</br>
Line Token: https://notify-bot.line.me/zh_TW/</br>
Pushover sample code: https://github.com/wyattjoh/pushover</br>
Pushover website: https://pushover.net/apps/2x77e8-binance_notify</br>

# Docker Build

docker build -t binance_notify .</br>

# Docker Run

docker run -d --name 3m binance_notify python 3m.py</br>
docker run -d --name 15m binance_notify python 15m.py</br>
docker run -d --name 1h binance_notify python 1h.py</br>
docker run -d --name 4h binance_notify python 4h.py</br>
docker run -d --name 8h binance_notify python 8h.py</br>
