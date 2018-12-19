import random
import time

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
            if bid < 50:
                bid = ask - 2

            price = round(bid + (ask - bid) / 3 * 0 + (ask - bid) / 3 * 3 * random.random(), 6)
            print("bid:%s price:%s ask:%s" % (bid, price, ask))

            amount = 0
            if bid < price < ask:
                amount = stocks * 0.65
                if balance / price < amount:
                    amount = float('%.8f' % (balance / price * 0.65))

            if 0.000002 < amount:
                askPrice.send_keys("%.6f" % price)
                askAmount.send_keys("%.8f" % amount)
                bidPrice.send_keys("%.6f" % price)
                bidAmount.send_keys("%.8f" % amount)
                if 0.5 < random.random():
                    sellCoin.click()
                    buyCoin.click()
                else:
                    buyCoin.click()
                    sellCoin.click()

            time.sleep(random.randint(5, 11))
            # time.sleep(random.randint(2, 3))
        except Exception as e:
            print(str(e))
            break
