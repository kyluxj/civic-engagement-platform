'''
# Civic Engagement Intelligence Platform - Deployment Guide

This guide provides comprehensive instructions for deploying the Civic Engagement Intelligence Platform to production environments.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Backend Deployment](#backend-deployment)
3. [Frontend Deployment](#frontend-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Security Considerations](#security-considerations)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)

## System Requirements

### Backend Requirements

- **Python:** 3.9 or higher
- **Database:** PostgreSQL 13+ (recommended for production) or SQLite (development only)
- **Memory:** Minimum 512MB RAM
- **Storage:** Minimum 1GB available space

### Frontend Requirements

- **Node.js:** 18.x or higher
- **npm:** 9.x or higher
- **Web Server:** Nginx, Apache, or any static file server

## Backend Deployment

### Option 1: Deploy to Heroku

1.  **Install Heroku CLI:**

    ```bash
    curl https://cli-assets.heroku.com/install.sh | sh
    ```

2.  **Login to Heroku:**

    ```bash
    heroku login
    ```

3.  **Create a new Heroku app:**

    ```bash
    cd backend
    heroku create your-app-name
    ```

4.  **Add PostgreSQL addon:**

    ```bash
    heroku addons:create heroku-postgresql:mini
    ```

5.  **Set environment variables:**

    ```bash
    heroku config:set JWT_SECRET_KEY="your-super-secret-key"
    heroku config:set OPENAI_API_KEY="your-openai-api-key"
    heroku config:set FLASK_ENV="production"
    heroku config:set CORS_ORIGINS="https://your-frontend-domain.com"
    ```

6.  **Create a `Procfile` in the backend directory:**

    ```
    web: gunicorn run:app
    ```

7.  **Deploy to Heroku:**

    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git push heroku main
    ```

8.  **Run database migrations:**

    ```bash
    heroku run python seed_data.py
    ```

### Option 2: Deploy to a VPS (Ubuntu/Debian)

1.  **Update system packages:**

    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

2.  **Install Python and dependencies:**

    ```bash
    sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx -y
    ```

3.  **Create a PostgreSQL database:**

    ```bash
    sudo -u postgres psql
    CREATE DATABASE civic_platform;
    CREATE USER civic_user WITH PASSWORD 'your-password';
    GRANT ALL PRIVILEGES ON DATABASE civic_platform TO civic_user;
    \q
    ```

4.  **Clone the repository:**

    ```bash
    cd /var/www
    git clone https://github.com/your-repo/civic-platform.git
    cd civic-platform/backend
    ```

5.  **Create virtual environment and install dependencies:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

6.  **Create `.env` file:**

    ```bash
    cat > .env << EOF
    DATABASE_URL="postgresql://civic_user:your-password@localhost/civic_platform"
    JWT_SECRET_KEY="your-super-secret-key"
    OPENAI_API_KEY="your-openai-api-key"
    FLASK_ENV="production"
    CORS_ORIGINS="https://your-frontend-domain.com"
    EOF
    ```

7.  **Initialize the database:**

    ```bash
    python seed_data.py
    ```

8.  **Create systemd service:**

    ```bash
    sudo nano /etc/systemd/system/civic-platform.service
    ```

    Add the following content:

    ```ini
    [Unit]
    Description=Civic Engagement Platform API
    After=network.target

    [Service]
    User=www-data
    WorkingDirectory=/var/www/civic-platform/backend
    Environment="PATH=/var/www/civic-platform/backend/venv/bin"
    ExecStart=/var/www/civic-platform/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 run:app

    [Install]
    WantedBy=multi-user.target
    ```

9.  **Start and enable the service:**

    ```bash
    sudo systemctl start civic-platform
    sudo systemctl enable civic-platform
    ```

10. **Configure Nginx as reverse proxy:**

    ```bash
    sudo nano /etc/nginx/sites-available/civic-platform
    ```

    Add the following configuration:

    ```nginx
    server {
        listen 80;
        server_name api.your-domain.com;

        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

11. **Enable the site and restart Nginx:**

    ```bash
    sudo ln -s /etc/nginx/sites-available/civic-platform /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

12. **Install SSL certificate (recommended):**

    ```bash
    sudo apt install certbot python3-certbot-nginx -y
    sudo certbot --nginx -d api.your-domain.com
    ```

## Frontend Deployment

### Option 1: Deploy to Netlify

1.  **Install Netlify CLI:**

    ```bash
    npm install -g netlify-cli
    ```

2.  **Build the frontend:**

    ```bash
    cd frontend
    npm install
    npm run build
    ```

3.  **Deploy to Netlify:**

    ```bash
    netlify deploy --prod --dir=dist
    ```

4.  **Configure environment variables in Netlify:**

    Go to your Netlify dashboard → Site settings → Environment variables and add:

    ```
    VITE_API_BASE_URL=https://api.your-domain.com
    ```

### Option 2: Deploy to Vercel

1.  **Install Vercel CLI:**

    ```bash
    npm install -g vercel
    ```

2.  **Deploy to Vercel:**

    ```bash
    cd frontend
    vercel --prod
    ```

3.  **Configure environment variables in Vercel:**

    ```bash
    vercel env add VITE_API_BASE_URL
    ```

    Enter the value: `https://api.your-domain.com`

### Option 3: Deploy to a VPS with Nginx

1.  **Build the frontend:**

    ```bash
    cd frontend
    npm install
    npm run build
    ```

2.  **Copy build files to web server:**

    ```bash
    sudo mkdir -p /var/www/civic-platform-frontend
    sudo cp -r dist/* /var/www/civic-platform-frontend/
    ```

3.  **Configure Nginx:**

    ```bash
    sudo nano /etc/nginx/sites-available/civic-platform-frontend
    ```

    Add the following configuration:

    ```nginx
    server {
        listen 80;
        server_name your-domain.com;
        root /var/www/civic-platform-frontend;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location /api {
            proxy_pass https://api.your-domain.com;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    ```

4.  **Enable the site:**

    ```bash
    sudo ln -s /etc/nginx/sites-available/civic-platform-frontend /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

5.  **Install SSL certificate:**

    ```bash
    sudo certbot --nginx -d your-domain.com
    ```

## Environment Configuration

### Backend Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `DATABASE_URL` | Database connection string | Yes | `postgresql://user:pass@localhost/db` |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Yes | `your-super-secret-key` |
| `OPENAI_API_KEY` | OpenAI API key for AI agents | Yes | `sk-...` |
| `FLASK_ENV` | Flask environment | Yes | `production` |
| `CORS_ORIGINS` | Allowed CORS origins | Yes | `https://your-domain.com` |

### Frontend Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `VITE_API_BASE_URL` | Backend API base URL | Yes | `https://api.your-domain.com` |

## Database Setup

### PostgreSQL Production Setup

1.  **Create database backup strategy:**

    ```bash
    # Create backup script
    cat > /usr/local/bin/backup-civic-db.sh << 'EOF'
    #!/bin/bash
    BACKUP_DIR="/var/backups/civic-platform"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    mkdir -p $BACKUP_DIR
    pg_dump civic_platform > $BACKUP_DIR/civic_platform_$TIMESTAMP.sql
    find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
    EOF

    chmod +x /usr/local/bin/backup-civic-db.sh
    ```

2.  **Schedule daily backups:**

    ```bash
    sudo crontab -e
    # Add this line:
    0 2 * * * /usr/local/bin/backup-civic-db.sh
    ```

### Database Migrations

When updating the application, run migrations:

```bash
cd backend
source venv/bin/activate
flask db upgrade
```

## Security Considerations

### Essential Security Measures

1.  **Use strong JWT secret keys:**

    Generate a secure random key:

    ```bash
    python -c "import secrets; print(secrets.token_hex(32))"
    ```

2.  **Enable HTTPS:**

    Always use SSL/TLS certificates in production. Use Let's Encrypt for free certificates.

3.  **Configure CORS properly:**

    Only allow your frontend domain in the `CORS_ORIGINS` environment variable.

4.  **Database security:**

    - Use strong database passwords
    - Restrict database access to localhost or specific IPs
    - Enable SSL for database connections

5.  **Rate limiting:**

    Consider implementing rate limiting on the API to prevent abuse.

6.  **Regular updates:**

    Keep all dependencies up to date:

    ```bash
    pip install --upgrade -r requirements.txt
    npm update
    ```

### Firewall Configuration

```bash
# Allow SSH, HTTP, and HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Monitoring and Maintenance

### Application Logs

**Backend logs:**

```bash
sudo journalctl -u civic-platform -f
```

**Nginx logs:**

```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Checks

Monitor the API health endpoint:

```bash
curl https://api.your-domain.com/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "Civic Engagement Intelligence Platform API"
}
```

### Performance Monitoring

Consider implementing monitoring tools:

- **Application Performance:** New Relic, DataDog, or Sentry
- **Server Monitoring:** Prometheus + Grafana
- **Uptime Monitoring:** UptimeRobot or Pingdom

### Backup and Recovery

1.  **Regular database backups:** Automated daily backups (configured above)
2.  **Code repository:** Keep code in version control (Git)
3.  **Configuration backups:** Store `.env` files securely
4.  **Recovery testing:** Regularly test backup restoration

## Troubleshooting

### Common Issues

**Issue: Database connection errors**

- Check database credentials in `.env`
- Verify PostgreSQL service is running: `sudo systemctl status postgresql`
- Check firewall rules

**Issue: CORS errors in frontend**

- Verify `CORS_ORIGINS` in backend `.env` matches frontend domain
- Check that frontend is using correct API URL

**Issue: 502 Bad Gateway**

- Check if backend service is running: `sudo systemctl status civic-platform`
- Review application logs: `sudo journalctl -u civic-platform -n 50`

**Issue: Frontend not loading**

- Verify Nginx configuration
- Check that build files exist in the correct directory
- Review Nginx error logs

## Support

For additional support or questions:

- Review the project documentation in the `README.md` files
- Check the issue tracker on GitHub
- Contact the development team

---

**Last Updated:** October 2025  
**Version:** 1.0.0
'''
