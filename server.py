from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
from flask_pymongo import PyMongo

app = Flask(__name__)

# Mongo Config
app.config['MONGO_URI'] = 'mongodb://localhost:27017/temp_database'
mongo = PyMongo(app) 

# SocketIO Config
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/add', methods=['POST'])
def add_data():
    if request.method == 'POST':
        print(request.data)
        data = request.get_json()
        print(data)
        mongo.db.temp_collection.insert_one(data)
        return f'Added entry: {data}'
    else:
        return 'Only POSTs accepted'

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    socketio.emit('my response', json, callback=messageReceived)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@app.route('/')
def home_page():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)

# app.run(host='0.0.0.0')
