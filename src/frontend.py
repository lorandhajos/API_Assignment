from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bokeh.embed import components
from bokeh.plotting import figure
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
        username = request.form['username']
        password = request.form['password']
        # additional checks for the username and password
        if(username == '' or password == ''):
            flash('Please fill out the form!', 'danger')
            return redirect(url_for('login'))
        req = requests.post("http://localhost:5000/api/v1/login", json={"username": username, "password": password})
        print(req.status_code)
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
        api_response = requests.get("http://localhost:5000/api/v1/views_report_films", headers={"Authorization": f"Bearer {session['access_token']}"})
        
        if api_response.status_code == 200:
            data = api_response.json()

            # Filter data based on keywords
            keyword = request.args.get('title', default=None)
            if keyword:
                filtered_data = [item for item in data if keyword.lower() in item['views'].lower()]
            else:
                filtered_data = data

            # Create Bokeh plot
            p = figure(height=350, sizing_mode="stretch_width")
            p.circle([i for i in range(len(filtered_data))], [item['views'] for item in filtered_data], size=20, color="navy", alpha=0.5)
            
            script, div = components(p)
            return render_template('dashboard.html', script=script, div=div, data=filtered_data)
        else:
            print(api_response.status_code)
            flash('Error fetching data from the API', 'danger')
            return "well, not well"
    else:
        return redirect(url_for('login'))
