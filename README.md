# 🕵️Pixel Tracker
*A tracking pixel to track email opens and gather IP info of the email client.*

### Overview
A pixel tracker is a small, invisible image (usually 1x1 pixel) embedded in an email, webpage, or ad that tracks user behavior. When a user interacts with the content containing the pixel, it sends data back to the server, allowing marketers and businesses to gather insights into user actions, such as whether an email was opened, a link was clicked, or a purchase was made.

The above project serves a static web page with a pixel. When a user opens the email or web page with the embedded pixel, the User-Agent string, timestamp, and IP Address are logged to the `tracker_log.txt` file. 

### 🌐Deploy in EC2
Create an EC2 instance with http traffic allowed.
SSH into the cloud instance.
<br/>
<br/>
Install Python Virtualenv
```bash
sudo apt-get update
sudo apt-get install python3-venv
```
Activate the new virtual environment in a new directory
```bash
source /venv/bin/activate
```
Create Directory
```bash
mkdir trackingPixel
cd trackingPixel
```

Clone Pixel Tracker repository
```bash
git clone https://github.com/JeffrinE/pixel-tracker.git
```
Create the virtual environment
```bash
python3 -m venv venv
```
Activate the virtual environment
```bash
source venv/bin/activate
```
Install requirements
```bash
pip install -r requirements.txt
```
Verify if it works by running 
```bash
cd app
python flaskapp.py
```
Run Gunicorn:
```bash
gunicorn -b 0.0.0.0:8000 flaskapp:app 
```
Gunicorn is running (Ctrl + C to exit gunicorn)!
```bash
sudo nano /etc/systemd/system/tracker.service
```
Then add this into the file.
```bash
[Unit]
Description= Gunicorn instance to serve tracking pixel
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/trackingPixel/app
ExecStart=/home/ubuntu/trackingPixel/venv/bin/gunicorn -b localhost:8000 flaskapp:app
Restart=always
[Install]
WantedBy=multi-user.target
```
Then enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start tracker
sudo systemctl enable tracker
```
Check if the app is running with 
```bash
curl localhost:8000
```
Run Nginx Webserver to accept and route request to Gunicorn
Finally, we set up Nginx as a reverse-proxy to accept the requests from the user and route it to gunicorn.
Install Nginx 
```bash
sudo apt-get nginx
```
Start the Nginx service and go to the Public IP address of your EC2 on the browser to see the default nginx landing page
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```
Edit the default file in the sites-available folder.
```bash
sudo nano /etc/nginx/sites-available/default
```
Replace the default content with content of `nginx_config.txt`
```bash
sudo cat nginx_config.txt > /etc/nginx/sites-available/default
```
Restart Nginx 
```bash
sudo systemctl restart nginx
```

Go to `http://ec2-publicDNS.amazonaws.com` to see the index page with text "Set to go".

### 📧ID and no ID
The project allows pixel emeddings with or without id for recognition.
```
http://ec2-publicDNS.amazonaws.com/pixel
```
The above url has no id, still can be used for tracking.
``` 
http://ec2-publicDNS.amazonaws.com/pixel/<id>
```
Id can have any Alpha-Numerical character sequence.
<br/>
<br/>
Embed the url as an image in an email or a webpage to track clicks.
```html
<img src="http://ec2-publicDNS.amazonaws.com/pixel" alt="">
or
<img src="http://ec2-publicDNS.amazonaws.com/pixel/id" alt="">
```
The IPs of clients are logged in the `track_log.txt` file in the server.

