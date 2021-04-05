from flask import Flask, render_template, request, redirect, url_for, session
import pymongo
from cryptography.fernet import Fernet
from pymongo import message
import scrap
from bson.objectid import ObjectId

app = Flask(__name__)

app.secret_key = 'jsdtxzgfvhjcmesgzjdcsdhzgfh'

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['price_tracker']

key = b'bYkgWH7qPbVmSFjVpyzkYiZsF5AQcGNuGpgehBKk76Y='
fernet = Fernet(key)

@app.route('/')
def loginPage():
    if 'username' in session:
        return redirect('/home')
    return render_template('login.html', message = request.args.get('message'))

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    trackers = db['trackers']
    tracks = trackers.find({ 'userId': session['userId'] })
    #print(tracks[0])
    return render_template('home.html', username = session['username'] ,tracks = tracks)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = db['users']
        query = {
            'username': request.form['username']
        }
        user = users.find_one(query)
        if user and fernet.decrypt(user['password']).decode() == request.form['password']:
            #print(user['_id'])
            session['username'] = user['username']
            session['userId'] = str(user['_id'])
            return redirect('/home')
        else: 
            return redirect(url_for('loginPage', message = 'Invalid credentials!'))
    else:
        return redirect(url_for('loginPage', message = ''))

@app.route('/logout', methods = ['POST'])
def logout():
    if request.method == 'POST':
        session.pop('username')
        session.pop('userId')
        return redirect(url_for('loginPage', message = 'Logged Out Successfully!'))

@app.route('/signup', methods = ['POST'])
def signup():
    if request.method == 'POST':
        users = db['users']
        if users.find_one({ 'username': request.form['username'] }):
            return 'Username already registered'
        else:
            user = {
                'username': request.form['username'],
                'password': fernet.encrypt(request.form['password'].encode()) 
            }
            users.insert_one(user)
            return redirect(url_for('loginPage', message = 'Account Created!'))

@app.route('/addTracker', methods = ['POST'])
def addTracker():
    if 'userId' not in session:
        return redirect(url_for('login'))
    trackers = db['trackers']
    if trackers.find_one({ 'link': request.form['link'], 'userId': session['userId'] }):
        return 'Already tracking...'
    else:
        details = scrap.getDetails(request.form['link'])
        tracker = {
            'userId': session['userId'],
            'link': request.form['link'],
            'name': details[0],
            'price': details[1],
            'email': request.form['email']
        }
        trackers.insert_one(tracker)
        return redirect(url_for('home'))

@app.route('/deleteTracker', methods = ['POST'])
def deleteTracker():
    if 'userId' not in session:
        return redirect(url_for('login'))
    trackers = db['trackers']
    trackers.find_one_and_delete({ '_id' : ObjectId(request.form['productId']) })
    return redirect(url_for('home'))

app.run(debug=True)