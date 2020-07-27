from flask import Flask, render_template

from gumtree import scrape_gumtree
from ebay import scrape_ebay
from fb import scrape_fb

items = []

while True:
    fb = input("Would you like to login to scrape Facebook Marketplace? Y/N\n")
    if fb != "Y" and fb != "N":
        print("Please enter a valid response")
    break

if fb == "Y":
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    scrape_fb(items, username, password)
else:
    print("Starting webscrape with Ebay")

while True:
    temp_items = []
    if scrape_ebay(temp_items) == None:
        continue
    else:
        for item in temp_items:
            items.append(item)
        break

scrape_gumtree(items)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", len = len(items), items = items)

@app.route("/NAME")
def index2():
    items.sort(key=lambda x: x.name)
    return render_template("index.html", len = len(items), items = items)

@app.route("/PRICE")
def index3():
    items.sort(key=lambda x: x.price)
    return render_template("index.html", len = len(items), items = items)

if __name__ == "__main__":
    app.run()
