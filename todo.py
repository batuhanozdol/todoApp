# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 13:55:23 2019

@author: Batuhan
"""

from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

#Desktop/TodoApp/> sqlite3 todo.db     .tables    .exit   db oluşturma

app = Flask(__name__)
app.config["SQLACLHEMY_DATABASE_URI"] = "sqlite:////Users/CEM/Desktop/TodoApp/todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos=todos)

@app.route("/complete/<string:id>")
def completetodo(id):
    todo = Todo.query.filter_by(id=id).first()
    print(todo)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deletetodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit() #database de değişiklik yaptığımızdan commit ederiz
    return redirect(url_for("index"))


@app.route("/add",methods=["POST"])
def add():
    title = request.form.get("title")
    newTodo = Todo(title=title,complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))    
    
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    