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

# Connected clients
users = []

# Add a data point into Mongo
@app.route('/add', methods=['POST'])
def add_data():
  if request.method == 'POST':
    data = request.get_json()
    print(data)
    mongo.db.temp_collection.insert_one(data)
    return f'Added entry: {data}'
  else:
    return 'Only POSTs accepted'

# Provide 100 data points to a new connection
@socketio.on('connection')
def on_connection(json, methods=['GET', 'POST']):
  users.append(request.sid)
  data_cursor = mongo.db.temp_collection.find().sort('time', -1)
  data = []
  for doc in data_cursor:
    if doc and len(data) < 150:
      doc.pop('_id')
      data.append(doc)
    else:
      break
  socketio.emit('init-data', data, room=request.sid)

@app.route('/')
def home_page():
  return render_template('index.html')

if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0', debug=True)
