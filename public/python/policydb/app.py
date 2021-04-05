"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request, url_for
from flask_pymongo import PyMongo
import datetime
from mongoengine import SequenceField

app = Flask(__name__)

# app.config['MONGO_URI'] = 'mongodb+srv://admin:PSAS1100@cluster0.jrg5d.mongodb.net/myFirstDatabase'
app.config['MONGO_URI'] = 'mongodb+srv://admin:PSAS1100@cluster0.jrg5d.mongodb.net/PolicyDB'

mongo = PyMongo(app)
date = datetime.datetime.now()

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# 1: testing on _id auto increment
def mongoInsertAutoIncIdDoc(doc, user):
    while True:
        cursor = mongo.db.user.find({}, {'_id': 1}).sort([('_id', -1)]).limit(1)
        try:
            doc['_id'] = cursor.next()['_id'] + 1
        except StopIteration:
            doc['_id'] = 1

        try:
            coll.insert_one(doc)
        except pymongo.errors.DuplicateKeyError:
            continue
        break
    return (doc)

# 2: testing on _id auto increment
def getLastUserId(self):
  if len(list(self.find())) is not 0:
    last_user = list(self.find({}).sort("user_id", -1).limit(1))
    return last_user[0]["user_id"]
  else:
    return 0

#creating the GUI (html)
@app.route('/')
def index():
    return'''
        <form method="POST" action="/create" enctype="multipart/form-data">
            <p>
            ID:          <input type="text" name="_id"><br>
            Policy Name:    <input type="text" name="Pname"><br>
            Upload File: <input type="file" name="profile_image"><br>
            <input type="submit">
            </p>
        </form>
    '''

#save file (upload to the DB)
@app.route('/create', methods=['POST'])
def create():
    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        mongo.save_file(profile_image.filename, profile_image)
       # _id = SequenceField(primary=True)
       # _id = mongoInsertAutoIncIdDoc('_id', 'user')
        mongo.db.user.insert({'_id' : request.form.get('_id'), 'Pname' : request.form.get('Pname'), 'profile_image_name' : profile_image.filename, 'Year': date.year, 'Month': date.month, 'Day': date.day})
       # mongo.db.user.save
    return 'Done!'

#send file (download the file from DB)
#Exmample: "file/IceBear1.jpg"
@app.route('/file/<filename>')
def file(filename):
        return mongo.send_file(filename)

@app.route("/user/<_id>")
def user_profile(_id):
    user = mongo.db.user.find_one_or_404({"_id": _id})
    return render_template("user.html",
        user=user)

@app.route("/profile/<username>")
def profile(username):
       user = mongo.db.user.find_one_or_404({'username' : username})
       return f'''
       <h1>{username}</h1>
       <img src="{url_for('file',filename=user['profile_image_name'])}">
       '''

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)


