class Item:
    def __init__(self, website):
        self.name = None
        self.date = None
        self.image = None
        self.link = None
        self.price = None
        self.website = website

    def set_name(self, name):
        self.name = name

    def set_date(self, date):
        self.date = date

    def set_image(self, image):
        self.image = image

    def set_link(self, link):
        self.link = link

    def set_price(self, price):
        self.price = price                
