from flask import Flask, render_template, request, redirect, url_for, flash, session
from bokeh.embed import components
from bokeh.plotting import figure, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Paired
from bokeh.transform import cumsum
from math import pi
import pandas as pd
from bokeh.io import output_file
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

@app.route('/favicon.ico')
def favicon():
    return ''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # additional checks for the username and password
        if(username == '' or password == ''):
            flash('Please fill out the form!', 'danger')
            return redirect(url_for(''))
        req = requests.post("http://localhost:5000/api/v1/login", json={"username": username, "password": password}, headers={"Accept": "application/json"})
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
        api_response_views = requests.get("http://localhost:5000/api/v1/report/views_report_films_views", headers={"Authorization": f"Bearer {session['access_token']}", "Accept": "application/json"})
        api_response_title = requests.get("http://localhost:5000/api/v1/report/views_report_films_names", headers={"Authorization": f"Bearer {session['access_token']}", "Accept": "application/json"})
        api_responce_series_title = requests.get("http://localhost:5000/api/v1/report/views_report_series_title", headers={"Authorization": f"Bearer {session['access_token']}", "Accept": "application/json"})
        api_responce_series_views = requests.get("http://localhost:5000/api/v1/report/views_report_series_views", headers={"Authorization": f"Bearer {session['access_token']}", "Accept": "application/json"})
        api_responce_country = requests.get("http://localhost:5000/api/v1/report/country", headers={"Authorization": f"Bearer {session['access_token']}", "Accept": "application/json"}).json()
        if api_response_views.status_code and api_response_title.status_code and api_responce_series_title.status_code and api_responce_series_views.status_code:
            # Filter data based on keywords
            # keyword = request.args.get('title', default=None)
            # if keyword:
            #     filtered_data = [item for item in x if keyword.lower() in item['title'].lower()]
            # else:
            #     filtered_data = x
            filtered_data_views = api_response_views.json()
            filtered_data_title = api_response_title.json()

            filtered_data_series_title = api_responce_series_title.json()
            filtered_data_series_views = api_responce_series_views.json()

            # filtered_data_country = api_responce_country.json()
            # filtered_data_country_number = api_responce_country_number.json()

            # Create Bokeh plot
            movie_title = []
            for item in filtered_data_title:
                movie_title.append(item['title'])

            movie_views = []
            for item in filtered_data_views:
                movie_views.append(item['views'])
            
            series_title = []
            for item in filtered_data_series_title:
                series_title.append(item['title'])
            
            series_views = []
            for item in filtered_data_series_views:
                series_views.append(item['views'])
            
            # Graph for movies
            source_movies = ColumnDataSource(data=dict(x=movie_title, y=movie_views))
            p = figure(x_range=movie_title)
            p.vbar(x='x', top='y', width=0.9, source=source_movies) 
            hover = HoverTool(tooltips=[("Views", "@y")]) 
            p.add_tools(hover)
            
            # Graph for series
            source_series = ColumnDataSource(data=dict(x=series_title, y=series_views))
            p2 = figure(x_range=series_title)
            p2.vbar(x='x', top='y', width=0.9, source=source_series)
            hover = HoverTool(tooltips=[("People", "@y")])
            p2.add_tools(hover)
            
             #Pie chart for countries
            data = pd.Series(api_responce_country).reset_index(name='value').rename(columns={'index':'country'})
            print(data)
            data['angle'] = data['value']/data['value'].sum() * 2*pi
            data['color'] = Paired[len(api_responce_country)]

            pieChart = figure(height=350, title="Pie Chart", toolbar_location=None,
                    tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

            pieChart.wedge(x=0, y=1, radius=0.4,
                    start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                    line_color="white", fill_color='color', legend_field='country', source=data)

            pieChart.axis.axis_label=None
            pieChart.axis.visible=False
            pieChart.grid.grid_line_color = None

            # Generate Bokeh components
            script, div = components(p)
            script2, div2 = components(p2)
            script3, div3 = components(pieChart)

            # Pass data to the template
            output_file("dashboard.html")
            return render_template('dashboard.html', script=script, div=div, script2=script2, div2=div2,script3=script3, div3=div3, username=session.get('username'))
        else:
            print(api_response_title.status_code)
            print(api_response_views.status_code)
            print(api_responce_series_title.status_code)
            print(api_responce_series_views.status_code)
            print(api_responce_country.status_code)
            print(api_responce_country_number.status_code)
            flash('Error fetching data from the API', 'danger')
            return "well, not well"
    else:
        return redirect(url_for(''))
    
@app.route('/table')
def table():
    if 'access_token' in session:
        # Get the user's choice from the radio buttons
        user_choice = request.args.get('FilmViews', 'FilmNames', 'SeriesViews')
        API_ENDPOINTS = {'FilmViews': 'http://localhost:5000/api/v1/report/views_report_films_views',
                         'FilmNames': 'http://localhost:5000/api/v1/report/views_report_films_names',
                        'SeriesViews': 'http://localhost:5000/api/v1/report/views_report_series_views',
        }
        # Check if the user's choice is a valid option
        if user_choice in API_ENDPOINTS:
            api_endpoint = API_ENDPOINTS[user_choice]
            # Make the API request
            api_response = requests.get(api_endpoint, headers={"Authorization": f"Bearer {session['access_token']}", "Accept": "application/json"})
            print(api_response.status_code)
            if api_response.status_code == 200:
                x = api_response.json()
                headers = []
                tableData = []
                return render_template('table.html', x=x, headers=headers, tableData=tableData, username=session.get('username'))
            else:
                print(api_response.status_code)
                flash('Error fetching data from the API', 'danger')
                return "well, not well"
        else:
            flash('Invalid choice', 'danger')
            return redirect(url_for('table'))
    else:
        return redirect(url_for('login'))
    