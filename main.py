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
    def __init__(self, name, price, productUrl):
        self.name = name
        self.price = price
        self.productUrl = productUrl
    def toString(self):
        return self.name+" => R"+str(self.price)+" => "+str(self.productUrl)

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

try:
    f = open("page#.txt", "r")
    page = int(f.readline())
    f.close()
except Exception as e:
    print(str(e))

try:
    f = open("product#.txt", "r")
    iterator = int(f.readline())
    f.close()
except Exception as e:
    print(str(e))

driver.get(url)
res =driver.page_source
takealot = bs4.BeautifulSoup(res,'html.parser')  

# iterator = 1
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
    global page
    for i in range(n):
        if (url == "https://www.takealot.com/all?_sb=1&_r=1&_si=dd428b313f4ff686a4a5b5cd7dc34a50&qsearch="):
        # if (i == 0):
            print("Page "+str(page)+"...\n")
            #Sponsored products
            aTags1 = takealot.findAll('a', attrs={'class':"product-anchor sponsored product-card-module_product-anchor_TUCBV"})

            #Normal Products
            aTags2 = takealot.findAll('a', attrs={'class':"product-anchor product-card-module_product-anchor_TUCBV"})
            aTags = aTags1+aTags2
            for aTag in aTags:
                url2 = aTag['href']
                url2 = domain+url2
                productUrl = url2
                t.sleep(0.5)
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
                product = [Product(name, price, productUrl)]
                onePageProducts += product
                print("Product "+str(iterator)+ " added.")
                f = open("product#.txt", "w")
                f.write(str(iterator))
                f.close()
                iterator += 1

            allProducts += onePageProducts
            #Add every product in a page to the all products array
            f = open("output.txt", "a")
            for product in onePageProducts:
                # f.write(product.name+" => "+"R"+product.price+"\n")
                f.write(product.toString()+"\n")
                # return self.name+" => R"+str(self.price)+" => "+str(self.productUrl)
            f.close()
            #Print page size
            print("\nPage "+str(page)+" has "+str(len(onePageProducts))+" products.\n")
            f = open("page#.txt", "w")
            f.write(str(page))
            f.close()
            #Clean onepage products array
            onePageProducts = []
            #update page number
            page += 1

        else:
            print("\nPage "+str(page)+"...\n")
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
                productUrl = url2
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
                product = [Product(name, price, productUrl)]
                onePageProducts += product
                print("Product "+str(iterator)+ " added.")
                f = open("product#.txt", "w")
                f.write(str(iterator))
                f.close()
                iterator += 1

            allProducts += onePageProducts

            #Add every product in a page to the all products array
            f = open("output.txt", "a")
            for product in onePageProducts:
                # f.write(product.name+" => "+"R"+product.price+"\n")
                f.write(product.toString()+"\n")
            f.close()
            #Print page size
            print("\nPage "+str(page)+" has "+str(len(onePageProducts))+" products.\n")
            f = open("page#.txt", "w")
            f.write(str(page))
            f.close()
            #Clean onepage products array
            onePageProducts = []
            #Update URl after each page
            print("\nUpdating url in urlStore...\n")
            f = open("urlStore.txt", "w")
            f.write(pageUrl)
            f.close()
            #update page number
            page += 1

print("#############################\n")
#Try it, if anything goes wrong, update url with the latest page so we don't have to restart scraping
try:
    scrollClick(10000)
    f = open("page#.txt", "w")
    f.write(str(page))
    f.close()
except Exception as e:
    print("\nHo tanganana ###################\n")
    print("\n"+str(e)+"\n")
    print("\nUpdating url in url store...\n")
    f = open("urlStore.txt", "w")
    f.write(pageUrl)
    f.close()
    f = open("page#.txt", "w")
    f.write(str(page))
    f.close()

print(str(len(allProducts))+" products added.\n")
print(allProducts[len(allProducts)-1].toString())
print("\n#############################")

driver.close()