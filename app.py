from flask import Flask, request, redirect, render_template 
from flask_sqlalchemy import SQLAlchemy
import pymysql
app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/lc1012019'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_content = db.Column(db.String(255), nullable=False)
    complete = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, task_content):
        self.task_content = task_content

tasks = []

@app.route('/', methods=['GET', 'POST'])
def todos():
    if request.method == 'POST':
        task_name = request.form['task']
        if task_name != '':
            new_task = Task(task_name)
            db.session.add(new_task)
            db.session.commit()



    tasks = Task.query.all()
    return render_template('todos.html', tasks = tasks)

if (__name__) == '__main__':
    app.run()
