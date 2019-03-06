from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/temp_database'
mongo = PyMongo(app) 

@app.route('/add', methods=['POST'])
def add_data():
    if request.method == 'POST':
        data = request.get_json()
        mongo.db.temp_collection.insert_one(data)
        print(data)
        return f'Added entry: {data}'
    else:
        return 'Only POSTs accepted'

@app.route('/')
def hello():
    return 'hello world!!'

app.run(host='0.0.0.0')


