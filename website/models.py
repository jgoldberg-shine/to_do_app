from . import db
import datetime

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)  #primary key gives each task a new id
    task = db.Column(db.String(300), unique = True) #task to have a max entry of 300 characters and task must be unique
    complete = db.Column(db.Boolean, default = False)
    date_created = db.Column(db.String(10), default=datetime.date.today().strftime('%d-%m-%Y'))
    priority = db.Column(db.String, default = False)
    category = db.Column(db.String, default = False)