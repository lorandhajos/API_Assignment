from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import output_file, show
import math
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

@app.route('/favicon.ico')
def favicon():
    return ''

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
            session['username'] = username
            session['access_token'] = req.json()['access_token']
            session['refresh_token'] = req.json()['refresh_token']
            print(req.json())
    
    if 'access_token' in session:
        return redirect(url_for('dashboard'))

    return render_template('base.html')

@app.route('/dashboard')
def dashboard():
    if 'access_token' in session:
        api_response_views = requests.get("http://localhost:5000/api/v1/views_report_films_views", headers={"Authorization": f"Bearer {session['access_token']}"})
        api_response_title = requests.get("http://localhost:5000/api/v1/views_report_films_names", headers={"Authorization": f"Bearer {session['access_token']}"})

        if api_response_views.status_code and api_response_title.status_code == 200:
            
            # Filter data based on keywords
            # keyword = request.args.get('title', default=None)
            # if keyword:
            #     filtered_data = [item for item in x if keyword.lower() in item['title'].lower()]
            # else:
            #     filtered_data = x
            filtered_data_views = api_response_views.json()
            filtered_data_title = api_response_title.json()
            # Create Bokeh plot
            movie_title = []
            for item in filtered_data_title:
                movie_title.append(item['title'])

            movie_views = []
            for item in filtered_data_views:
                movie_views.append(item['views'])

            source = ColumnDataSource(data=dict(x=movie_title, y=movie_views))
            p = figure(x_range=movie_title)
            p.vbar(x='x', top='y', width=0.9, source=source) 
            hover = HoverTool(tooltips=[("Value", "@y")]) 
            p.add_tools(hover) 
            
            # for item in filtered_data:
            #     print(item)
            #     print(item['title'])
            #     print(item['views'])
                        # Generate Bokeh components
            script, div = components(p)

            # Pass data to the template
            output_file("dashboard.html")
            return render_template('dashboard.html', script=script, div=div, data=filtered_data_views, username=session.get('username'))
        else:
            print(api_response_title.status_code)

            flash('Error fetching data from the API', 'danger')
            return "well, not well"
    else:
        return redirect(url_for('login'))
    