from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bokeh.embed import components
from bokeh.plotting import figure
import random
import threading
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

# with open("templates/login.html", "r", encoding="utf-8") as f:
#     login = f.read()
# app.config['SECRET_KEY'] = ''  # put here JWT secret key
# app.config['postgresql.sql'] = 'postgresql://postgres:example@localhost/postgres'
# db = SQLAlchemy(app)

@app.route('/favicon.ico')
def favicon():
    return ''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            hashed_password = generate_password_hash(password, method='sha1')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # additional checks for the username and password
        if(email == '' or password == ''):
            flash('Please fill out the form!', 'danger')
            return redirect(url_for('login'))
        req = requests.post("http://localhost:5000/api/v1/login", json={"email": email, "password": password})
        if req.status_code == 200:
            session['access_token'] = req.json()['access_token']
            session['refresh_token'] = req.json()['refresh_token']
            print(req.json())
    
    if 'access_token' in session:
        return redirect(url_for('dashboard'))

    return render_template('base.html')

@app.route('/dashboard')
def dashboard():
    if 'access_token' in session:
        p1 = figure(height=350, sizing_mode="stretch_width") 
        p1.circle(
            [i for i in range(10)], 
            [random.randint(1, 50) for j in range(10)], 
            size=20, 
            color="navy", 
            alpha=0.5
        )
        p2 = figure(height=350, sizing_mode="stretch_width") 
        p2.circle( 
            [i for i in range(10)], 
            [random.randint(1, 50) for j in range(10)], 
            size=20,
            color="navy",
            alpha=0.5
        )

        script1, div1 = components(p1)
        script2, div2 = components(p2)
        return render_template('dashboard.html', script=[script1, script2], div=[div1, div2])
        # return f'Welcome to the dashboard, User #{session["user_id"]}!'
    else:
        return redirect(url_for('login'))
