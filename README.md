![demo-gif](demo.gif)


## Disclaimer
This software is meant to be a productive contribution to the rapidly growing AI-generated media industry. It will help artists with tasks such as animating a custom character or using the character as a model for clothing etc.

The developers of this software are aware of its possible unethical applications and are committed to take preventative measures against them. It has a built-in check which prevents the program from working on inappropriate media including but not limited to nudity, graphic content, sensitive material such as war footage etc. We will continue to develop this project in the positive direction while adhering to law and ethics. This project may be shut down or include watermarks on the output if requested by law.

Users of this software are expected to use this software responsibly while abiding by local laws. If the face of a real person is being used, users are required to get consent from the concerned person and clearly mention that it is a deepfake when posting content online. Developers of this software will not be responsible for actions of end-users.

#Setup

python3.10 -m venv env

source env/bin/activate

pip install -r requirements.txt

## Deployment on Ubuntu Server with Nginx and Gunicorn

Follow these steps to deploy the Flask application on an Ubuntu server with Nginx as a reverse proxy and Gunicorn as a WSGI server.

### 1. Set Up Your Ubuntu Server

First, ensure your server is up-to-date:

```bash
sudo apt update
sudo apt upgrade -y

2. Install Required Packages
Install Python, pip, virtual environment, Nginx, and Git:

bash
Copy code
sudo apt install python3.10 python3.10-venv python3-pip nginx git -y
3. Clone Your Flask Application
Navigate to the directory where you want to clone your project and clone it:

bash
Copy code
cd /var/www
sudo git clone https://github.com/sensahin/Deep-Live-Cam-WebUI.git
cd Deep-Live-Cam-WebUI
4. Set Up the Virtual Environment
Create and activate a virtual environment:

bash
Copy code
python3.10 -m venv env
source env/bin/activate
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
5. Test the Application Locally
Before moving to deployment, test the application locally:

bash
Copy code
python app.py
Ensure everything is working as expected at http://127.0.0.1:5000.

6. Set Up Gunicorn
Install Gunicorn in your virtual environment:

bash
Copy code
pip install gunicorn
Test Gunicorn with your Flask app:

bash
Copy code
gunicorn --bind 0.0.0.0:5000 app:app
If everything works, you'll see Gunicorn serving your Flask application. Use Ctrl+C to stop it.

7. Create a Systemd Service for Gunicorn
Create a systemd service file to manage Gunicorn as a background service:

bash
Copy code
sudo nano /etc/systemd/system/deep-live-cam-webui.service
Add the following content:

ini
Copy code
[Unit]
Description=Gunicorn instance to serve Deep-Live-Cam-WebUI
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/Deep-Live-Cam-WebUI
Environment="PATH=/var/www/Deep-Live-Cam-WebUI/env/bin"
ExecStart=/var/www/Deep-Live-Cam-WebUI/env/bin/gunicorn --workers 3 --bind unix:deep-live-cam-webui.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
Save and exit (Ctrl+X, Y, Enter).

Reload systemd to register the new service:

bash
Copy code
sudo systemctl daemon-reload
Start and enable the service:

bash
Copy code
sudo systemctl start deep-live-cam-webui
sudo systemctl enable deep-live-cam-webui
8. Configure Nginx as a Reverse Proxy
Create an Nginx configuration file for your application:

bash
Copy code
sudo nano /etc/nginx/sites-available/deep-live-cam-webui
Add the following configuration:

nginx
Copy code
server {
    listen 80;
    server_name your_domain_or_IP;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/Deep-Live-Cam-WebUI/deep-live-cam-webui.sock;
    }
}
Replace your_domain_or_IP with your server's domain name or IP address.

Save and exit (Ctrl+X, Y, Enter).

Enable the Nginx site:

bash
Copy code
sudo ln -s /etc/nginx/sites-available/deep-live-cam-webui /etc/nginx/sites-enabled
Test the Nginx configuration:

bash
Copy code
sudo nginx -t
If the test is successful, restart Nginx:

bash
Copy code
sudo systemctl restart nginx
9. Allow Firewall Access (if applicable)
If your server has a firewall enabled, allow Nginx traffic:

bash
Copy code
sudo ufw allow 'Nginx Full'
10. Access Your Application
Your Flask application should now be accessible via your domain or IP address at http://your_domain_or_IP.

Summary of Instructions:
bash
Copy code
# Update and install dependencies
sudo apt update
sudo apt upgrade -y
sudo apt install python3.10 python3.10-venv python3-pip nginx git -y

# Clone and set up your application
cd /var/www
sudo git clone https://github.com/sensahin/Deep-Live-Cam-WebUI.git
cd Deep-Live-Cam-WebUI
python3.10 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Test the app locally
python app.py

# Set up Gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 app:app

# Create a systemd service for Gunicorn
sudo nano /etc/systemd/system/deep-live-cam-webui.service
# (add the content as provided above)

# Reload systemd and start the service
sudo systemctl daemon-reload
sudo systemctl start deep-live-cam-webui
sudo systemctl enable deep-live-cam-webui

# Set up Nginx as a reverse proxy
sudo nano /etc/nginx/sites-available/deep-live-cam-webui
# (add the content as provided above)

# Enable the Nginx site and restart Nginx
sudo ln -s /etc/nginx/sites-available/deep-live-cam-webui /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Allow Nginx through the firewall (if applicable)
sudo ufw allow 'Nginx Full'
Your application should now be running 24/7 on your Ubuntu server, accessible through your domain or IP address.