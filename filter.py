import os
from unittest import result
from bs4 import BeautifulSoup
import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, time
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time as t
###########################################################################################

prices=[]
urls=[]
names=[]
iterator = 0
# try:
#     f = open("computersAndTablets.txt", "r")
#     ff = open("prices.txt", "a")
#     for line in f:
#         if(len(line.split(" => ")) > 0):
#             price = line.split(" => ")[1][1:]
#             url = line.split(" => ")[2]
#             name= line.split(" => ")[0]
#         if(price != "Price unavailable" and price.isnumeric()):
#             # print(price)
#             price = price.replace(",", "")
#             print(price)
#             prices.append(int(price))
#             urls.append(str(url))
#             names.append(str(name))
#             ff.write(str(price))
#             # print("Iterator: "+str(iterator))
#             iterator += 1
#     f.close()
#     ff.close()
#     # print("\n####################\n")
#     # print("First: \n")
#     # print(prices[0])
#     # print("\nLast: \n")
#     # print(prices[len(prices)-1])
#     # print("\n####################")
# except Exception as e:
#     print(str(e))
# pricelt100 = []
# for i in range(len(prices)):
#     if(prices[i]<=100):
#         pricelt100.append(prices[i])
#         try:
#             fff = open("pricelt100.txt", "a")
#             fff.write(str(names[i])+" => R"+str(prices[i])+" => "+str(urls[i]))
#             fff.close()
#         except Exception as e:
#             print(e)
# print("\n####################\n")
# print("Data collected")

# print("Less than 100:\n")
# print(len(pricelt100))



#############################################################################################

class Product:
    def __init__(self, name, price, productUrl):
        self.name = name
        self.price = price
        self.productUrl = productUrl
    def toString(self):
        return self.name+" => R"+str(self.price)+" => "+str(self.productUrl)
    def setPrice(self, price):
        self.price = price

os.environ['PATH'] += r"C:\Users\renda\OneDrive\Documents\CsEandeavours\SeleniumDrivers"
# driver = webdriver.Chrome()

driver = webdriver.Chrome(ChromeDriverManager().install())

results = []
n = 1 
def scrollClick():
    global driver
    global results
    global n
    try:
        f = open("pricelt100.txt", "r")
        fff = open("pricelt100_2.txt", "a")
        for line in f:
            apparentPrice = line.split(" => ")[1][1:]
            url = line.split(" => ")[2]

            driver.get(url)
            res =driver.page_source
            takealot = bs4.BeautifulSoup(res,'html.parser')  

            spanTag = takealot.find('span', attrs={'class':"currency plus currency-module_currency_29IIm"})
            h1Tag= takealot.find('h1')
            try:
                name = h1Tag.string
            except:
                name = "Name unavailable"
            try:
                price = spanTag.string[2:]
            except:
                price = "Price unavailable"
            if(name is None):
                name = "Name unavailable"
            if(price is None):
                price = "Price unavailable"
            # product = [name+"\n"+price]
            product = Product(name, price, url)
            productl = [product]
            # if(apparentPrice == price):
            results += productl
            print("Product "+str(n)+" added.")
            n += 1
            if(n%100 == 0):
                fff.write(product.toString())
            # else:
                
            #     product.setPrice(price)
        f.close()
        fff.close()
        # ff = open("Pricelt100_2.txt", "a")
        # for product in results:
        #     ff.write(product.toString())
        #     print("Product "+str(n)+" added.")
        # ff.close()
    except Exception as e:
        print(str(e))

print("#############################\n")
try:
    scrollClick()
except Exception as e:
    print("\nHo tanganana ###################\n")
    print("\n"+str(e)+"\n")
print("\n#############################")

driver.close()