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
        api_response = requests.get("http://localhost:5000/api/v1/views_report_films", headers={"Authorization": f"Bearer {session['access_token']}"})
        
        if api_response.status_code == 200:
            x = [
                {'views': 70, 'title': "hello"},
                {'views': 20, 'title': "world"},
                {'views': 10, 'title': "foo"},
            ]

            # Filter data based on keywords
            keyword = request.args.get('title', default=None)
            if keyword:
                filtered_data = [item for item in x if keyword.lower() in item['title'].lower()]
            else:
                filtered_data = x

            # Create Bokeh plot
            # p = figure(height=350, sizing_mode="stretch_width")
            # p.circle([i for i in range(len(filtered_data))], [item['views'] for item in filtered_data], size=20, color="navy", alpha=0.5)
            # graph = figure(title = "Bokeh Vertical Bar Graph")
            # graph.xaxis.axis_label = "title"
            # graph.yaxis.axis_label = "views"
            #x = ['A', 'B', 'C', 'D', 'E'] 
            x = []

            for item in filtered_data:
                x.append(item['title'])

            #y = [10, 20, 30]
            y = []

            for item in filtered_data:
                y.append(item['views'])

            source = ColumnDataSource(data=dict(x=x, y=y))
            p = figure(x_range=x)
            p.vbar(x='x', top='y', width=0.9, source=source) 
            hover = HoverTool(tooltips=[("Value", "@y")]) 
            p.add_tools(hover) 
            
            for item in filtered_data:
                print(item)
                print(item['title'])
                print(item['views'])
                        # Generate Bokeh components
            script, div = components(p)

            # Pass data to the template
            output_file("dashboard.html")
            return render_template('dashboard.html', script=script, div=div, data=filtered_data, username=session.get('username'))
        else:
            print(api_response.status_code)
            flash('Error fetching data from the API', 'danger')
            return "well, not well"
    else:
        return redirect(url_for('login'))
    