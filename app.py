from flask import Flask, render_template, request, redirect, url_for
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/FanGear')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
inventory = db.inventory



@app.route('/')
def inventory_index():
    """Show all playlists."""
    return render_template('base.html', inventory=inventory.find())