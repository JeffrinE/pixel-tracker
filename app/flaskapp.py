from flask import Flask, send_file, request, render_template_string
import datetime
import requests
from pathlib import Path
import ujson

app = Flask(__name__) #initialize flask app

current_directory = str(Path.cwd())
parent_directory = str(Path.cwd().parent)

@app.route('/') #default index route
def check_text_file():
    try:
        with open((parent_directory+'/track_log.txt'), 'r') as file:
            content = "Set to go"
    except FileNotFoundError:
        content = "File not found."
    except Exception as e:
        content = f"An error occurred: {e}"
    return render_template_string('<pre>{{ content }}</pre>', content=content)

@app.route('/pixel') #route for tracker with no id 
def tracking_pixel():

    filename = current_directory +"/pixel.png"
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S")

    get_ip = request.headers.get('x-forwarded-for') #get remote address

    with requests.get(f"https://ipinfo.io/{get_ip}/json") as url: #get ip data from ipinfo.io
        data = url.json()

    user_log = {"id":None , "user_agent":user_agent, "timestamp":timestamp}

    with open((parent_directory+'/track_log.txt'), 'a') as file: #write ip data to file
        user_log.update(data)
        entry = user_log.copy()
        file.write(ujson.dumps(entry) + '\n')

    return send_file(filename, mimetype="image/png")

@app.route('/pixel/<id>') #route for tracker with id 
def tracking_pixel_id(id):

    filename = current_directory +"/pixel.png"
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S")

    get_ip = request.headers.get('x-forwarded-for') #get remote address

    with requests.get(f"https://ipinfo.io/{get_ip}/json") as url: #get ip data from ipinfo.io
        data = url.json()

    user_log = {"id":id, "user_agent":user_agent, "timestamp":timestamp}

    with open((parent_directory+'/track_log.txt'), 'a') as file: #write ip data to file
        user_log.update(data)
        entry = user_log.copy()
        file.write(ujson.dumps(entry) + '\n')

    return send_file(filename, mimetype="image/png")

if __name__ == '__main__':
    app.run()
