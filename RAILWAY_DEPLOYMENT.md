# Railway Deployment Guide

## Prerequisites
1. GitHub account with your code pushed
2. Railway account (https://railway.app)

## Deployment Steps

### 1. Connect to Railway
1. Go to https://railway.app and sign up/login
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository: `deneasato/TIZ-Ecommerce`

### 2. Environment Variables
Add these environment variables in Railway dashboard:

**Required:**
- `SECRET_KEY` = Generate a new Django secret key for production
- `DEBUG` = `False`
- `DATABASE_URL` = (Will be auto-provided by Railway PostgreSQL)

**Email Settings:**
- `EMAIL_HOST_USER` = `davideneasatochibueze@gmail.com`
- `EMAIL_HOST_PASSWORD` = `ohpz baey hljd shsj`

**Paystack Settings:**
- `PAYSTACK_SECRET_KEY` = `sk_test_0a047d5e8e28eb131c7c01cc52d33b2ce1a98c88`
- `PAYSTACK_PUBLIC_KEY` = `pk_test_d8444b3f89482a480b1e1ae5ed97cd1b35acf796`
- `PAYSTACK_BASE_URL` = `https://api.paystack.co`

**Domain (will be updated after deployment):**
- `WEBSITE_DOMAIN` = `https://your-railway-app.railway.app`

### 3. Add PostgreSQL Database
1. In Railway dashboard, click "New" → "Database" → "PostgreSQL"
2. Railway will automatically set the `DATABASE_URL` environment variable

### 4. Deploy
1. Railway will automatically deploy your app
2. Monitor the build logs for any issues
3. Once deployed, your app will be available at the provided Railway URL

### 5. Post-Deployment
1. Update `WEBSITE_DOMAIN` environment variable with your Railway URL
2. Create a superuser: In Railway dashboard, go to your service and run:
   ```bash
   python manage.py createsuperuser
   ```

## Important Notes
- Never commit `.env` file to git (it's in .gitignore)
- Always use environment variables for sensitive data in production
- The app will automatically run migrations and collect static files on deployment
- Monitor Railway logs for any deployment issues

## Local Development
To run locally after deployment setup:
1. Keep your `.env` file for local development
2. Use `DEBUG=True` locally
3. SQLite will be used for local development, PostgreSQL for production
