Here’s a detailed setup guide in markdown format for deploying your web app `ddns-web-ui` on a Raspberry Pi device, ensuring it runs automatically after restarts.

---

# Raspberry Pi Deployment Guide for DDNS Web UI

## Prerequisites
- Raspberry Pi with **Raspberry Pi OS** (Debian-based).
- SSH access enabled on the Pi.
- **Nginx** installed on the Pi.
- Git installed (`sudo apt install git`).
- Python 3 and `pip` installed (`sudo apt install python3-pip`).

### Step 1: Clone the GitHub Repository
First, SSH into your Raspberry Pi and navigate to the desired directory where you want to install the app. Then clone the repository:

```bash
cd /home/pi
git clone https://github.com/kryptobaseddev/ddns-web-ui.git
cd ddns-web-ui
```

### Step 2: Create and Activate Virtual Environment
Set up a Python virtual environment to keep dependencies isolated.

```bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
Once the virtual environment is activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

### Step 4: Run Database Migrations
Ensure all database migrations are applied to set up the initial database:

```bash
flask db upgrade
```

### Step 5: Configure `.env` File
Copy the `.env.template` file to `.env` and configure it with your settings (e.g., database URL, secret keys, etc.).

```bash
cp .env.template .env
nano .env
```

### Step 6: Set Up Gunicorn
Install Gunicorn, which will serve your Flask app.

```bash
pip install gunicorn
```

Create a Gunicorn configuration file to run the app:

```bash
nano gunicorn_config.py
```

Add the following configuration:

```python
bind = "0.0.0.0:8000"
workers = 3
```

Test Gunicorn with your app:

```bash
gunicorn --config gunicorn_config.py run:app
```

You should see your app running at `http://<your-pi-ip>:8000`.

### Step 7: Configure Nginx
To serve your Flask app via Nginx, update your Nginx configuration.

Create a new Nginx config for the app:

```bash
sudo nano /etc/nginx/sites-available/ddns-web-ui
```

Add the following Nginx configuration (adjust paths and ports as necessary):

```nginx
server {
    listen 80;
    server_name <your-pi-ip>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/pi/ddns-web-ui/app/static;
    }
}
```

Enable the new Nginx configuration:

```bash
sudo ln -s /etc/nginx/sites-available/ddns-web-ui /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

### Step 8: Create a Systemd Service
To ensure the app runs on startup, create a `systemd` service for the Gunicorn process.

Create the service file:

```bash
sudo nano /etc/systemd/system/ddns-web-ui.service
```

Add the following content:

```ini
[Unit]
Description=Gunicorn instance to serve ddns-web-ui
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=/home/pi/ddns-web-ui
Environment="PATH=/home/pi/ddns-web-ui/venv/bin"
ExecStart=/home/pi/ddns-web-ui/venv/bin/gunicorn --config /home/pi/ddns-web-ui/gunicorn_config.py run:app

[Install]
WantedBy=multi-user.target
```

Reload `systemd` and enable the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ddns-web-ui
```

Start the service:

```bash
sudo systemctl start ddns-web-ui
```

Check the status to ensure it is running:

```bash
sudo systemctl status ddns-web-ui
```

### Step 9: Check Logs and Verify
Verify everything is working by checking logs and visiting your Pi's IP address.

```bash
sudo journalctl -u ddns-web-ui
```

Visit the app at `http://<your-pi-ip>` in your browser.

### Step 10: (Optional) Set Up Automatic Updates
You can set up a cron job to automatically pull updates from GitHub and restart the service.

```bash
crontab -e
```

Add the following line:

```bash
0 3 * * * cd /home/pi/ddns-web-ui && git pull && sudo systemctl restart ddns-web-ui
```

---

This setup ensures your web app runs automatically on boot and is served via Nginx on your Raspberry Pi. You can customize the service configuration as needed.