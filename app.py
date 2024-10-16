from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['stationery_wishlist']
collection = db['items']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_item():
    item_name = request.form['item_name']
    collection.insert_one({'name': item_name})  # Save the item in MongoDB
    return redirect(url_for('wishlist'))

@app.route('/wishlist')
def wishlist():
    items = collection.find()
    return render_template('wishlist.html', items=items)

@app.route('/delete/<item_id>')
def delete_item(item_id):
    collection.delete_one({'_id': ObjectId(item_id)})  # Remove the item from MongoDB
    return redirect(url_for('wishlist'))

if __name__ == '__main__':
    app.run(debug=True)
