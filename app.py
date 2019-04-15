from flask import Flask, request, redirect, render_template, session, escape, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy import or_
app = Flask(__name__)
app.secret_key = b'\xe5\\\xd6\xea\xde\xde\x85\xbd\xdd\xb9A\x8d_\xc7Lj'
app.config["CACHE_TYPE"] = "null"
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/lc1012019'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_content = db.Column(db.String(255), nullable=False)
    complete = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, task_content, user_id):
        self.task_content = task_content
        self.user_id = user_id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(140), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'authenticated' in session:
        return redirect(url_for('todos'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username != "" and password !="":
                user = User.query.filter((User.email == username) | (User.username == username)).first()
                if user and user.password == password:
                        session['authenticated'] = True
                        session['id'] = user.id
                        return redirect(url_for('todos'))
                else:
                    flash('Invalid user or password.')
                    return redirect(url_for('login'))
            return '', 204
            
        else:
                return render_template('login.html', user_action='Sign In', alternative='Or login With', signin_action = '/login', log_reg_link="/register", email_hide='hide', needsTo='Sign Up')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email != "" and password !="":
            current_user =  User.query.filter_by(email=email).first()
            if not current_user:
                new_user = User(email=email, password=password, username='')
                db.session.add(new_user)
                db.session.commit()
                # TODO - "remember" the user
                return redirect(url_for('todos'))
            else:
                flash('An account with this user already exists. Please, sign in.')
                return redirect(url_for('register'))
        else:
            return '', 204
    else:
         return render_template('login.html', user_action='Register', alternative='Or register with', signin_action='/register', log_reg_link="/login", username_hide='hide', needsTo='Sign In')

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'authenticated' not in session:
        return redirect('/login')

@app.route('/', methods=['GET', 'POST'])
def todos():
    if 'id' in session:
        user = User.query.filter_by(id=session.get('id')).first()
        tasks = Task.query.filter((Task.user_id == session.get('id')) & (Task.complete==0) ).all()
        completed_tasks = Task.query.filter((Task.user_id == session.get('id')) & (Task.complete==1) ).all()
        return render_template('todos.html',title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks, hide='hide')
    else: 
        flash('Please, login to add tasks.', 'danger')
        return redirect(url_for('login'))

@app.route('/addTask', methods=['POST'])
def addTask():
    task_name = request.form['task']
    if task_name != '':
        new_task = Task(task_name, 0, session.get('id'))
        db.session.add(new_task)
        db.session.commit()
        taskId = new_task.id
        return jsonify({'success': 'success', 'message': 'Tasks updated', 'alertType': 'secondary'})
    else:
        return jsonify({'error': 'error', 'message': 'Please, enter a task.', 'alertType': 'info' })

@app.route('/delete-task', methods=['POST'])
def delete_task():
     task_id = int(request.form['task-id'])
     task = Task.query.get(task_id)
     task.complete = 1
     db.session.add(task)
     db.session.commit()

     return redirect('/')

@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('authenticated', None)
    return redirect(url_for('login'))

if (__name__) == '__main__':
    app.run()
