from bs4 import BeautifulSoup as soup
import requests
import time
import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from flask import Flask, render_template

from item import Item

# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("start-maximized")
# chrome_options.add_argument("disable-infobars")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options = chrome_options)

def scrape_gumtree(items: list):

    gumtree = requests.get("https://www.gumtree.com.au/s-snow-sports/sydney/snowboard/k0c20095l3003435")

    if gumtree.status_code == 200:
        print("Able to access gumtree")

    gumtree_src = gumtree.content

    gumtree_soup = soup(gumtree_src, features = "html.parser")

    names = []
    dates = []

    p_title = "user-ad-row__title"
    p_age = "user-ad-row__age"

    for p in gumtree_soup.find_all("p", text = True):

        if(p.get("class")[0] == p_title):
            names.append(p.text)
        if(p.get("class")[0] == p_age):
            dates.append(p.text)

    prices = []

    for s in gumtree_soup.find_all("span"):

        span = s.get("class")
        if span != [] and span != None:
            if "user-ad-price__price" in span[0] and len(span) == 1:
                price = s.text.replace(",", "") # remove commas
                prices.append(price)

    links = []
    advert = False
    for a in gumtree_soup.find_all("a"):

        if(a["href"] == "/s-snow-sports/sydney/snowboard/k0c20095l3003435"):
            break

        if(advert):
            links.append("https://gumtree.com.au" + a["href"])

        if(a["href"] == "/s-snow-sports/sydney/snowboard/k0c20095l3003435?highlightAds=y"):
            advert = True

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.gumtree.com.au/s-snow-sports/sydney/snowboard/k0c20095l3003435")

    y = 1000
    for i in range(0, 5):
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += 1000
        time.sleep(0.5)

    time.sleep(1)

    images = driver.find_elements_by_tag_name("img")
    img_links = []

    for img in images:
        img_link = img.get_attribute("src")

        # pictures of items from posts have format "https://i.ebayimg.com.....l180.webp"
        if ".webp" in img_link:
            img_links.append(img_link)

    driver.quit()

    print(len(names))
    print(len(dates))
    print(len(links))
    print(len(img_links))
    print(len(prices))

    for i in range(0, len(links)):
        item = Item("Gumtree")
        item.set_name(names[i])
        item.set_date(dates[i])
        item.set_image(img_links[i])
        item.set_link(links[i])

        if prices[i] == "Negotiable":
            item.set_price(0)
        else:
            item.set_price(int(prices[i].strip("$")))

        items.append(item)

# def format_date(date: str):
    


# now we have arrays with names, links, images
# we want to output this to html

# items = []

# scrape_gumtree(items)

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index2.html", len = len(items), items = items)

# if __name__ == "__main__":
#     app.run()