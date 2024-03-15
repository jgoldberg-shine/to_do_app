from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from .models import Todo
from . import db



my_view = Blueprint("my_view", __name__)
@my_view.route("/")
def home():
    todo_list = Todo.query.all()
    message = request.args.get("message", None) #Get any message or success parameter from the request URL
    success = request.args.get("success", None)
    return render_template("index.html", todo_list=todo_list, message = message, success = success)

@my_view.route("/add", methods=["POST"])    #allows post methods
def add():
    try:
        task = request.form.get("task").lower()     # Get the task from the form data
        priority = request.form.get("priority")
        category = request.form.get("category")
        new_todo = Todo(task=task, priority = priority, category=category)     # Create a new Todo object with the task
        db.session.add(new_todo)   #add into db
        db.session.commit() 
        success = "Task added successfully"    #
        return redirect(url_for("my_view.home", success = success))
    except:
        message = "Error adding your task to the ToDo list, you can not have more than one of the same task" # If an error occurs during adding the task, set an error message
        return redirect(url_for("my_view.home", message = message))

@my_view.route("/update/<todo_id>")
def update (todo_id):
    todo = Todo.query.filter_by(id=todo_id).first() # Find the todo item by its ID
    todo.complete = not todo.complete   # Toggle the completion status of the todo item
    db.session.commit() 
    return redirect(url_for("my_view.home"))

@my_view.route("/delete/<todo_id>")
def delete (todo_id):
    todo = Todo.query.filter_by(id=todo_id).first() # Find the todo item by its ID
    db.session.delete(todo) # Delete the todo item from the database
    db.session.commit()
    return redirect(url_for("my_view.home"))

@my_view.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit_todo(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        if request.method == "POST":    # If the request method is POST, update the task of the todo item
            todo.task = request.form["edit_task"]  # Corrected input field name
            db.session.commit()
            return redirect(url_for("my_view.home"))
        return render_template("edit_todo.html", todo=todo)
    except:
        message = "Error editing your task. Two identical tasks cannot exist"   # If an error occurs during editing the task, set an error message
        return redirect(url_for("my_view.home", message=message)) # Redirect to the home page with the error message


@my_view.route("/page2")
def page2():
    data = Todo.query.all()
    return render_template("page2.html", data = data)


