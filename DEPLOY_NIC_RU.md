# Deploy to NIC.RU VDS/VPS

This guide publishes the Django site on a NIC.RU VDS/VPS with Ubuntu, Nginx, Gunicorn, systemd, and HTTPS.

Replace these placeholders everywhere:

- `SERVER_IP` - your VDS/VPS public IP address
- `example.ru` - your domain
- `www.example.ru` - your www domain
- `REPO_URL` - your Git repository URL

## 1. Buy the right hosting

Use NIC.RU VDS/VPS, not ordinary shared hosting. This project is a Django app, so it needs a Python process manager behind Nginx.

Recommended first server:

- Ubuntu 24.04 LTS
- 2 GB RAM if possible
- 20-40 GB SSD
- SSH access enabled

After purchase, save the server IP, `root` password, or SSH key.

## 2. Point the domain to the server

In NIC.RU DNS settings, create A records:

```text
@    A    SERVER_IP
www  A    SERVER_IP
```

DNS can take from a few minutes to several hours to update.

## 3. Prepare the server

Connect as root:

```bash
ssh root@SERVER_IP
```

Update packages and install tools:

```bash
apt update
apt upgrade -y
apt install -y python3 python3-venv python3-pip nginx git certbot python3-certbot-nginx
```

Create a non-root user:

```bash
adduser soup
usermod -aG sudo soup
su - soup
```

## 4. Upload the project

Preferred option with Git:

```bash
git clone REPO_URL soup_project_01
cd soup_project_01
```

If you are not using Git yet, upload the project folder with SFTP or from your local machine:

```bash
scp -r /path/to/soup_project_01 soup@SERVER_IP:/home/soup/
```

## 5. Create Python environment

On the server, inside `/home/soup/soup_project_01`:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Configure environment variables

Generate a secret key:

```bash
.venv/bin/python - <<'PY'
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
PY
```

Create a server-only env file:

```bash
sudo nano /etc/soup.env
```

Paste this and replace values:

```dotenv
DJANGO_SECRET_KEY=PASTE_GENERATED_SECRET_HERE
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=example.ru,www.example.ru
DJANGO_CSRF_TRUSTED_ORIGINS=https://example.ru,https://www.example.ru
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SECURE_HSTS_SECONDS=0
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=False
DJANGO_SECURE_HSTS_PRELOAD=False
```

Protect the file:

```bash
sudo chown root:soup /etc/soup.env
sudo chmod 640 /etc/soup.env
```

## 7. Run Django checks

```bash
set -a
. /etc/soup.env
set +a

.venv/bin/python manage.py check --deploy
.venv/bin/python manage.py migrate
.venv/bin/python manage.py collectstatic --noinput
```

`check --deploy` may warn about HSTS while `DJANGO_SECURE_HSTS_SECONDS=0`. That is acceptable for the first launch. Enable HSTS later after HTTPS is confirmed stable.

## 8. Create systemd service

Exit to the `soup` user if needed, then create the service with sudo:

```bash
sudo nano /etc/systemd/system/soup.service
```

Paste:

```ini
[Unit]
Description=Soup Django site
After=network.target

[Service]
User=soup
Group=www-data
WorkingDirectory=/home/soup/soup_project_01
EnvironmentFile=/etc/soup.env
RuntimeDirectory=soup
ExecStart=/home/soup/soup_project_01/.venv/bin/gunicorn config.wsgi:application --bind unix:/run/soup/soup.sock
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable soup
sudo systemctl start soup
sudo systemctl status soup
```

If it fails:

```bash
sudo journalctl -u soup -n 100 --no-pager
```

## 9. Configure Nginx

Create the site config:

```bash
sudo nano /etc/nginx/sites-available/soup
```

Paste:

```nginx
server {
    listen 80;
    server_name example.ru www.example.ru;

    client_max_body_size 20m;

    location /static/ {
        alias /home/soup/soup_project_01/staticfiles/;
    }

    location / {
        proxy_pass http://unix:/run/soup/soup.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/soup /etc/nginx/sites-enabled/soup
sudo nginx -t
sudo systemctl reload nginx
```

Open:

```text
http://example.ru
http://www.example.ru
```

## 10. Enable HTTPS

Run:

```bash
sudo certbot --nginx -d example.ru -d www.example.ru
```

Choose redirect to HTTPS when Certbot asks.

Check renewal:

```bash
sudo certbot renew --dry-run
```

Open:

```text
https://example.ru
https://www.example.ru
```

## 11. Update the site later

When new changes are ready:

```bash
cd /home/soup/soup_project_01
git pull
. .venv/bin/activate
pip install -r requirements.txt
set -a
. /etc/soup.env
set +a
.venv/bin/python manage.py migrate
.venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart soup
sudo systemctl reload nginx
```

## Troubleshooting

`Bad Request (400)`: add the real domain to `DJANGO_ALLOWED_HOSTS` in `/etc/soup.env`, then restart:

```bash
sudo systemctl restart soup
```

No styles or images: run `collectstatic` and check the Nginx `/static/` alias:

```bash
cd /home/soup/soup_project_01
set -a
. /etc/soup.env
set +a
.venv/bin/python manage.py collectstatic --noinput
sudo nginx -t
sudo systemctl reload nginx
```

Site shows 502: check Gunicorn:

```bash
sudo systemctl status soup
sudo journalctl -u soup -n 100 --no-pager
```

HTTPS does not issue: confirm DNS points to `SERVER_IP`:

```bash
dig +short example.ru
dig +short www.example.ru
```

After HTTPS has worked for a while, you can enable HSTS by changing `/etc/soup.env`:

```dotenv
DJANGO_SECURE_HSTS_SECONDS=2592000
```

Then restart:

```bash
sudo systemctl restart soup
```
