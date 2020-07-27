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

def scrape_fb(items: list, username, password):

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = chrome_options)
    driver.get("https://www.facebook.com")

    user = username
    pw = password

    user_x = '//*[@id="email"]'
    pw_x = '//*[@id="pass"]'
    login_x = '//*[@id="u_0_b"]' 

    user_element = driver.find_element_by_xpath(user_x)
    pw_element = driver.find_element_by_xpath(pw_x)
    login_element = driver.find_element_by_xpath(login_x)

    user_element.send_keys(user)
    time.sleep(0.2)
    pw_element.send_keys(pw)
    time.sleep(0.2)
    login_element.click()

    time.sleep(5)

    driver.get("https://www.facebook.com/marketplace/sydney/search/?sortBy=creation_time_descend&query=snowboard&exact=false")

    y = 1000
    for i in range(0, 5):
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += 1000
        time.sleep(1)

    time.sleep(2)

    temp_links = driver.find_elements_by_tag_name("a")
    links = []

    for l in temp_links:
        link = l.get_attribute("href")
        if "item" in link:
            links.append(link)
        if len(links) >= 20:
            break

    names = []
    prices = []
    img_links = []
    dates = []

    for link in links:
        driver.get(link)
        time.sleep(3)

        info = driver.find_elements_by_tag_name("span")

        i = 0
        while i < len(info):
            if len(info[i].text) > 0 and info[i].text[0] == "$":

                price = info[i].text.replace(",", "") # remove commas
                prices.append(price)

                names.append(info[i-1].text)
                if "Listed" in info[i+2].text:
                    dates.append(info[i+2].text.strip("Listed ").split(" in")[0])
                else:
                    j = 3
                    while "Listed" not in info[i+j].text:
                        j += 1
                    
                    dates.append(info[i+j].text.strip("Listed ").split(" in")[0])

                break

            i += 1

        images = driver.find_elements_by_tag_name("img")
        img_links.append(images[0].get_attribute("src"))

        time.sleep(2)

    for i in range(0, len(links)):

        item = Item("Facebook")
        item.set_name(names[i])
        item.set_date(dates[i])
        item.set_image(img_links[i])
        if(len(links) != 0):
            item.set_link(links[i])
        item.set_price(int(prices[i].strip("$")))

        items.append(item)

    driver.quit()
