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
inventory = db.inventory
comments = db.comments 

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

@app.route('/inventory/<inventory_id>')
def show_item(inventory_id):
    item = inventory.find_one({'_id': ObjectId(inventory_id)})
    item_comments = comments.find({'inventory_id': ObjectId(inventory_id)})
    return render_template("item_show.html", inventory = item, comments = item_comments)

@app.route('/inventory/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'inventory_id': ObjectId(request.form.get('inventory_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('show_item', inventory_id=request.form.get('inventory_id')))

@app.route('/inventory/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('show_item', inventory_id=comment.get('inventory_id')))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))