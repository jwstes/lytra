#!/bin/bash
sudo apt update
apt install python3-pip
pip install psutil Flask flask_cors
git clone https://github.com/jwstes/lytra.git

# Install Supervisor
sudo apt install supervisor

sudo apt install nload

# Create Supervisor configuration file
sudo nano /etc/supervisor/conf.d/flask_app.conf

# Add content to flask_app.conf
echo "[program:flask_app]" | sudo tee -a /etc/supervisor/conf.d/flask_app.conf > /dev/null
echo "command=python3 /root/lytra/server.py" | sudo tee -a /etc/supervisor/conf.d/flask_app.conf > /dev/null
echo "directory=/root/lytra/" | sudo tee -a /etc/supervisor/conf.d/flask_app.conf > /dev/null
echo "autostart=true" | sudo tee -a /etc/supervisor/conf.d/flask_app.conf > /dev/null
echo "autorestart=true" | sudo tee -a /etc/supervisor/conf.d/flask_app.conf > /dev/null
echo "stderr_logfile=/var/log/your_app.err.log" | sudo tee -a /etc/supervisor/conf.d/flask_app.conf > /dev/null
echo "stdout_logfile=/var/log/your_app.out.log" | sudo tee -a /etc/supervisor/conf.d/flask_app.conf > /dev/null

# Reload Supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Start the application
sudo supervisorctl start flask_app
