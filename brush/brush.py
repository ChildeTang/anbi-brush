import random
import time
import requests

from selenium import webdriver

driver = webdriver.Chrome()


while True:

    driver.get("https://www.anbi.com/login")
    username = driver.find_element_by_id("username")
    username.send_keys("123@163.com")
    password = driver.find_element_by_id("password")
    password.send_keys("123")
    login = driver.find_element_by_id("loginBtn")
    login.click()
    time.sleep(3)
    driver.get('https://www.anbi.com/tradingview?symbol=ETH_USDT')
    time.sleep(5)

            while True:
        try:
            print("tick --> ")

            if '' == driver.find_element_by_class_name('buy_available').text:
                break

            balance = float(driver.find_element_by_class_name('buy_available').text)
            stocks = float(driver.find_element_by_class_name('sell_available').text)

            askPrice = driver.find_element_by_id("sellPriceInput")
            askAmount = driver.find_element_by_id("sellCountInput")
            bidPrice = driver.find_element_by_id("buyPrice")
            bidAmount = driver.find_element_by_id("buySum")

            askPrice.clear()
            askAmount.clear()
            bidPrice.clear()
            bidAmount.clear()

            buyCoin = driver.find_element_by_id("buyCoin")
            sellCoin = driver.find_element_by_id("sellCoin")

            bid = float(driver.find_element_by_class_name('buy').find_elements_by_class_name('price')[0].text)
            ask = float(driver.find_element_by_class_name('sell').find_elements_by_class_name('price')[-1].text)

            huobi = requests.get('https://api.huobi.pro/market/detail/merged?symbol=ethusdt').json()
            hbid = huobi['tick']['bid'][0]
            hask = huobi['tick']['ask'][0]

            tick = True
            first = None
            little = False
            if bid < hbid < ask < hask:
                bid = hbid
            elif bid < hbid < hask < ask:
                bid = hbid
                ask = hask
            elif hbid < bid < hask < ask:
                ask = hask
            elif hask < bid < hask + 10:
                if bid + 0.0001 < ask:
                    ask = bid + 0.0001
                first = 'ask'
                little = True
            elif hbid - 10 < ask < hbid:
                if bid < ask - 0.0001:
                    bid = ask - 0.0001
                first = 'bid'
                little = True
            else:
                tick = False
                print('b: %s a: %s hb:%s ha %s' % (bid, ask, hbid, hask))

            price = round(bid + (ask - bid) / 3 * 0 + (ask - bid) / 3 * 3 * random.random(), 6)
            print("bid:%s price:%s ask:%s" % (bid, price, ask))

            amount = 0
            if bid < price < ask:
                amount = stocks * 0.45
                if balance / price < amount:
                    amount = float('%.8f' % (balance / price * 0.45))

            if little and 0.002 < amount:
                amount = 0.002

            if tick and 0.000002 < amount:
                askPrice.send_keys("%.6f" % price)
                askAmount.send_keys("%.8f" % amount)
                bidPrice.send_keys("%.6f" % price)
                bidAmount.send_keys("%.8f" % amount)
                if first is None:
                    if 0.5 < random.random():
                        sellCoin.click()
                        time.sleep(1)
                        buyCoin.click()
                    else:
                        buyCoin.click()
                        time.sleep(1)
                        sellCoin.click()
                elif first == 'bid':
                    buyCoin.click()
                    time.sleep(1)
                    sellCoin.click()
                elif first == 'ask':
                    sellCoin.click()
                    time.sleep(1)
                    buyCoin.click()

            time.sleep(random.randint(3, 5))
            # time.sleep(random.randint(2, 3))
        except Exception as e:
            print(str(e))
            break
