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

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def toString(self):
        return self.name+" => "+str(self.price)

os.environ['PATH'] += r"C:\Users\renda\OneDrive\Documents\CsEandeavours\SeleniumDrivers"
# driver = webdriver.Chrome()

driver = webdriver.Chrome(ChromeDriverManager().install())
domain = "https://www.takealot.com"
# url = "https://www.takealot.com/all?_sb=1&_r=1&_si=dd428b313f4ff686a4a5b5cd7dc34a50&qsearch="

#Get URL from file
url=""
try:
    f = open("urlStore.txt", "r")
    url = str(f.readline())
    f.close()
except Exception as e:
    print(str(e))

driver.get(url)
res =driver.page_source
takealot = bs4.BeautifulSoup(res,'html.parser')  

iterator = 1
allProducts = []
onePageProducts = []
aTags=[]
pageUrl = url
def scrollClick(n):
    global takealot
    global res
    global driver
    global domain
    global url
    global allProducts
    global aTags
    global iterator
    global onePageProducts
    global pageUrl
    for i in range(n):
        if (i==0):
            #Sponsored products
            aTags1 = takealot.findAll('a', attrs={'class':"product-anchor sponsored product-card-module_product-anchor_TUCBV"})

            #Normal Products
            aTags2 = takealot.findAll('a', attrs={'class':"product-anchor product-card-module_product-anchor_TUCBV"})
            aTags = aTags1+aTags2
            for aTag in aTags:
                url2 = aTag['href']
                url2 = domain+url2
                driver.get(url2)
                res =driver.page_source
                takealot2= bs4.BeautifulSoup(res,'html.parser')  
                spanTag = takealot2.find('span', attrs={'class':"currency plus currency-module_currency_29IIm"})
                h1Tag= takealot2.find('h1')
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
                product = [Product(name,price)]
                onePageProducts += product
                print("Product "+str(iterator)+ " added.")
                iterator += 1

            allProducts += onePageProducts
            #Add every product in a page to the all products array
            f = open("output.txt", "a")
            for product in onePageProducts:
                f.write(product.name+" => "+"R"+product.price+"\n")
            f.close()
            #Clean onepage products array
            onePageProducts = []

        else:
            driver.get(url)
            pageUrl = url
            res =driver.page_source
            takealot = bs4.BeautifulSoup(res,'html.parser')  

            #Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #Click
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.ghost.search-listings-module_load-more_OwyvW"))).click()
            t.sleep(5)
            url = driver.current_url
            driver.get(url)
            pageUrl = url
            res =driver.page_source
            takealot= bs4.BeautifulSoup(res,'html.parser')  

            #Normal Products
            aTags2 = takealot.findAll('a', attrs={'class':"product-anchor product-card-module_product-anchor_TUCBV"})
            aTags = aTags2
            for aTag in aTags:
                url2 = aTag['href']
                url2 = domain+url2
                driver.get(url2)
                res =driver.page_source
                takealot2= bs4.BeautifulSoup(res,'html.parser')  
                spanTag = takealot2.find('span', attrs={'class':"currency plus currency-module_currency_29IIm"})
                h1Tag= takealot2.find('h1')
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
                product = [Product(name,price)]
                onePageProducts += product
                print("Product "+str(iterator)+ " added.")
                iterator += 1

            allProducts += onePageProducts

            #Add every product in a page to the all products array
            f = open("output.txt", "a")
            for product in onePageProducts:
                f.write(product.name+" => "+"R"+product.price+"\n")
            f.close()
            #Clean onepage products array
            onePageProducts = []

#Try it, if anything goes wrong, update url with the latest page so we don't have to restart scraping
try:
    scrollClick(3)
except Exception as e:
    print("\n"+str(e)+"\n")
    print("\nUpdating url in url store...\n")
    f = open("urlStore.txt", "w")
    f.write(pageUrl)
    f.close()

print(str(len(allProducts))+" products added.")
print(allProducts[len(allProducts)-1].toString())

driver.close()