from flask import Flask, flash, url_for, render_template, request, redirect, make_response, Response, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin

from pymongo import MongoClient
import datetime

my_ip = "192.168.2.1" #app server IP
client = MongoClient('mongodb://127.0.0.1:27017') #connect to MongoDB
db = client['pingit'] #pingitDB
payments = db['payments'] #collection for payments
card_holders = db['card_holders'] #collection for cards/holders

app = Flask(__name__)

app.secret_key = "829c63b4c6fe351bc517a048a529638660185e32a83aba5e"

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html',ip=my_ip)

#URL for logging payments to MongoDB (call from wherever)
@app.route('/payment/<card_id>/<amount>')
def payment(card_id, amount):
    details = {'card_id':card_id} #create dict to insert into MongoDB
    details.update({'amount':amount})
    socketio.emit('payment', details) #send basic details for feedback in-app
    details.update({'timestamp':datetime.datetime.now()})
    card_holder  = card_holders.find_one({'card_id':card_id})
    if card_holder:
        details.update({'name':card_holder.get('name')}) #try to find card holder in database
    else:
        details.update({'name':'Unregistered card holder'})
    try:
        payments.insert_one(details) #add to database
        return jsonify(payment = {'success':True})
    except:
        return jsonify(payment = {'success':False})

#function to find today's payments (for populating a recent payments grid)
@app.route('/today')
def payments_today():
    today = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0)
    tomorrow = today + datetime.timedelta(days = 1)
    payment_results = list(payments.find({'timestamp':{'$gte':today, '$lt':tomorrow}}, {'_id':0}).sort('timestamp', -1))
    total = sum([int(payment.get('amount')) for payment in payment_results])
    if len(payment_results) > 4:
        results = payment_results[0:5]
    else:
        results = payment_results
    return jsonify(results = results, total = total)

if __name__ == '__main__':
    socketio.run(app, host=my_ip, debug=True)
