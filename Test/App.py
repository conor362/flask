
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users3.db'
app.config['SECRET_KEY'] = "SECRET"

'''
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:36%Reilly!@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
'''

#creating database for app
db = SQLAlchemy(app)
 
#Creating model table for the database that can then be created, updated and deleted
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(100))
    door_id = db.Column(db.String(100))
    start_id = db.Column(db.String(100))
    end_id = db.Column(db.String(100))
    access = db.Column(db.String(100))

    def __init__(self, user_id, door_id, start_id, end_id, access):
 
        
        self.user_id = user_id
        self.door_id = door_id
        self.start_id = start_id
        self.end_id = end_id
        self.access = access
 
 
 
#This is the index route where we are going to get the user/eployee data
@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", employees = all_data)
 

#this route is for inserting data to the database via html POST forms
@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
        
        user_id = request.form['user_id']
        door_id = request.form['door_id']
        start_id = request.form['start_id']
        end_id = request.form['end_id']
        access = request.form['access'] 
 
        my_data = Data(user_id, door_id, start_id, end_id, access)
        db.session.add(my_data)
        db.session.commit()
 
        flash("User Inserted Successfully")
 
        return redirect(url_for('Index'))
 
 
#This is for updating route where it will be possible to GET and UPDATE user data
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
 
        
        my_data.user_id = request.form['user_id']
        my_data.door_id = request.form['door_id']
        my_data.start_id = request.form['start_id']
        my_data.end_id = request.form['end_id']
        my_data.access = request.form['access'] 
 
        db.session.commit()
 
        return redirect(url_for('Index'))
 
 
#This route is for deleting any Users from Database
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
 
    return redirect(url_for('Index'))

 
if __name__ == "__main__":
    app.run(debug=True)