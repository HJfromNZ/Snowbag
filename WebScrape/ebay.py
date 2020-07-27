from bs4 import BeautifulSoup as soup
import requests
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from item import Item

def scrape_ebay(items: list):

    ebay = requests.get("https://www.ebay.com.au/sch/i.html?_from=R40&_nkw=snowboard&_sacat=0&LH_TitleDesc=0&_sop=10")

    time.sleep(2)
    
    if ebay.status_code == 200:
        print("Able to access ebay")

    ebay_src = ebay.content

    ebay_soup = soup(ebay_src, features = "html.parser")

    # want an array of names, images, and links which correspond to items which are within 2 days

    dates = []
    prices = []
    advert = False

    for s in ebay_soup.find_all("span"):

        span = s.get("class")

        if span != None and span != []:

            # dates

            if "s-item__dynamic" in span[0]:
                advert = True
            if span[0] == "BOLD" and advert:
                dates.append(s.text.split(" ")[0]) # we remove time since date is precise enough
                advert = False

            # prices

            if span[0] == "s-item__price":
                price = s.text.split(" ")[1].split(".")[0] # remove currency "AU"
                price = price.replace(",", "") # remove commas
                prices.append(price)

            if len(span) >= 2 and "s-item__buyItNowOption" in span[1]:
                prices.pop(len(prices) - 1)

    names = []
    img_links = []
    for img in ebay_soup.find_all("img", alt = True):
        name = img.get("alt")
        img_link = img.get("src")
        if "s-l225" in img_link or "secureir" in img_link:
            img_links.append(img.get("src"))
            names.append(name)

    links = []
    advert = False

    for a in ebay_soup.find_all("a"):

        link = a.get("href")

        if link == None:
            continue

        if (link == "https://www.ebay.com.au/sch/i.html?_from=R40&_nkw=snowboard&_sacat=0&LH_TitleDesc=0&_sop=10&_pgn=1"):
            break

        if "ebay.com.au/itm/" in link:
            advert = True
        else:
            advert = False

        if advert and link not in links:
            links.append(link)

    # first link is an automated advertisement i.e. not snowboard 
    links.pop(0)

    print(len(names))
    print(len(dates))
    print(len(links))
    print(len(img_links))
    print(len(prices))

    if len(names) != 50 or len(dates) != 50 or len(links) != 50 or len(img_links) != 50 or len(prices) != 50:
        return None

    for i in range(0, len(links)):
        item = Item("Ebay")
        item.set_name(names[i])
        item.set_date(dates[i])
        item.set_image(img_links[i])
        item.set_link(links[i])
        item.set_price(int(prices[i].strip("$")))

        items.append(item)

    return True

