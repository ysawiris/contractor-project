from pymongo import MongoClient
from bson.objectid import ObjectId

product_1 = {
    'product_team_brand': 'Golden State Warriors',
    'product_name' : 'Official NBA Jersey',
    'pic_path' : '/static/warriors_jersey.jpeg',
    'product_price' : 60
}

product_2 = {
    'product_team_brand': 'Los Angeles Lakers',
    'product_name' : 'Official NBA Jersey',
    'pic_path' : '/static/lakers_jersey.jpeg',
    'product_price' : 60
}

product_3 = {
    'product_team_brand': 'L.A. Clippers',
    'product_name' : 'Official NBA Jersey',
    'pic_path' : '/static/clippers_jersey.jpeg',
    'product_price' : 60
}

product_4 = {
    'product_team_brand': 'Portland Trail Blazers',
    'product_name' : 'Official NBA Jersey',
    'pic_path' : '/static/trail_blazers_jersey.jpeg',
    'product_price' : 60
}

product_5 = {
    'product_team_brand': 'Brooklyn Nets',
    'product_name' : 'Official NBA Jersey',
    'pic_path' : '/static/nets_jersey.jpeg',
    'product_price' : 60
}

inventory_list = [
    product_1,
    product_2,
    product_3,
    product_4,
    product_5
]

class Store():
    def __init__(self, inventory):
        self.inventory = inventory
    
    def show_inventory(self):
        self.inventory.delete_many({})
        
        self.inventory.insert_many(inventory_list)
        
        for i in self.inventory.find():
            print(inventory_list)