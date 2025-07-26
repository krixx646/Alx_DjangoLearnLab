# HTTPS Deployment Configuration

This document provides instructions for configuring a web server to serve our Django application over HTTPS. These configurations are essential for ensuring that the security settings implemented in Django (such as `SECURE_SSL_REDIRECT`, `HSTS`, etc.) function correctly.

## Prerequisites

- A domain name pointing to your server
- A server running Linux (Ubuntu/Debian recommended)
- Root or sudo access to the server

## Option 1: Nginx with Let's Encrypt

### 1. Install Nginx

```bash
sudo apt update
sudo apt install nginx
```

### 2. Install Certbot for Let's Encrypt certificates

```bash
sudo apt install certbot python3-certbot-nginx
```

### 3. Configure Nginx for your Django application

Create a new Nginx configuration file:

```bash
sudo nano /etc/nginx/sites-available/libraryproject
```

Add the following configuration (replace `yourdomain.com` with your actual domain):

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;  # Django application running on port 8000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/libraryproject /etc/nginx/sites-enabled/
sudo nginx -t  # Test the configuration
sudo systemctl reload nginx
```

### 4. Obtain SSL/TLS certificates from Let's Encrypt

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts to complete the certificate installation. Certbot will automatically modify your Nginx configuration to use HTTPS.

### 5. Verify the updated Nginx configuration

The configuration should now include SSL settings:

```bash
sudo cat /etc/nginx/sites-available/libraryproject
```

It should look similar to this:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;  # Redirect HTTP to HTTPS
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    
    # Additional security headers to complement Django settings
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 6. Set up automatic certificate renewal

Let's Encrypt certificates expire after 90 days. Set up automatic renewal:

```bash
sudo certbot renew --dry-run  # Test the renewal process
```

Certbot installs a cron job or systemd timer that will renew certificates automatically before they expire.

## Option 2: Apache with Let's Encrypt

### 1. Install Apache

```bash
sudo apt update
sudo apt install apache2
```

### 2. Enable required Apache modules

```bash
sudo a2enmod proxy proxy_http ssl rewrite headers
sudo systemctl restart apache2
```

### 3. Install Certbot for Let's Encrypt certificates

```bash
sudo apt install certbot python3-certbot-apache
```

### 4. Configure Apache for your Django application

Create a new Apache configuration file:

```bash
sudo nano /etc/apache2/sites-available/libraryproject.conf
```

Add the following configuration:

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
```

Enable the site:

```bash
sudo a2ensite libraryproject.conf
sudo apache2ctl configtest  # Test the configuration
sudo systemctl reload apache2
```

### 5. Obtain SSL/TLS certificates from Let's Encrypt

```bash
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts to complete the certificate installation. Certbot will automatically modify your Apache configuration to use HTTPS.

### 6. Verify the updated Apache configuration

The configuration should now include SSL settings:

```bash
sudo cat /etc/apache2/sites-available/libraryproject-le-ssl.conf
```

It should include SSL settings and security headers:

```apache
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    
    # Set X-Forwarded-Proto header to https for Django's SECURE_PROXY_SSL_HEADER
    RequestHeader set X-Forwarded-Proto "https"
    
    # Security headers to complement Django settings
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
    
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
</IfModule>
```

## Running Django with Gunicorn

For production, it's recommended to use Gunicorn instead of Django's development server:

### 1. Install Gunicorn

```bash
pip install gunicorn
```

### 2. Create a systemd service for your Django application

```bash
sudo nano /etc/systemd/system/libraryproject.service
```

Add the following configuration:

```ini
[Unit]
Description=LibraryProject Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project/LibraryProject
ExecStart=/path/to/your/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 LibraryProject.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 3. Start and enable the service

```bash
sudo systemctl start libraryproject
sudo systemctl enable libraryproject
```

## Testing HTTPS Configuration

After setting up HTTPS, test your configuration using these tools:

1. [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
2. [Security Headers](https://securityheaders.com/)

These tools will analyze your HTTPS implementation and provide recommendations for improvements.

## Important Notes

1. **Django Settings**: Ensure that your Django settings.py has the appropriate HTTPS settings as documented in security_documentation.md.

2. **Firewall Configuration**: Make sure your firewall allows traffic on ports 80 and 443:
   ```bash
   sudo ufw allow 'Nginx Full'  # For Nginx
   # OR
   sudo ufw allow 'Apache Full'  # For Apache
   ```

3. **Production Environment**: Set the following environment variables for your production environment:
   ```bash
   export DJANGO_SETTINGS_MODULE=LibraryProject.settings
   export DJANGO_DEBUG=False
   ```

4. **Regular Updates**: Regularly update your server, web server software, and SSL certificates to maintain security.

By following these deployment instructions, your Django application will be properly configured to serve content over HTTPS, ensuring that all the security settings implemented in Django function correctly.