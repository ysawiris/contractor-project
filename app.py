from flask import Flask, render_template, request, redirect, url_for
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from inventory import Store
from datetime import datetime

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/FanGear')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
inventory = db['inventory']

store = Store(inventory)
store.show_inventory()

@app.route('/')
def inventory_index():
    """Show all playlists."""
    return render_template('show_inventory.html', inventory_list=inventory.find())


@app.route('/inventory/')
def show_inventory():
    items = inventory.find({'product_name': 'Official NBA Jersey'})
    return render_template("show_inventory.html", inventory=items)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))