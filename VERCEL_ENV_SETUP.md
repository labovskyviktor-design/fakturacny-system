# Vercel Environment Variables Setup

This file contains the environment variables you need to set in Vercel Dashboard.

## How to Set Environment Variables in Vercel

1. Go to https://vercel.com/dashboard
2. Select your project (fakturacny-system)
3. Click on **Settings** tab
4. Click on **Environment Variables** in the left sidebar
5. Add each variable below

## Required Environment Variables

### DATABASE_URL
**Value:**
```
postgresql://postgres:Hudriko123+@db.posabupqsehvtwskqulh.supabase.co:5432/postgres
```
**Description:** Supabase PostgreSQL database connection string

---

### SECRET_KEY
**Value:**
```
86033e2bd0bb8e1ec7ca6c8c5ae4cc6a29388e1ec7ca6c8c5ae4cc6a2938
```
**Description:** Flask secret key for session security

---

### FLASK_ENV
**Value:**
```
production
```
**Description:** Sets Flask to production mode

## Optional Environment Variables

### SENDGRID_API_KEY
**Value:** `<your-sendgrid-api-key>`
**Description:** For sending emails (registration, password reset)

### MAIL_DEFAULT_SENDER
**Value:** `noreply@yourdomain.com`
**Description:** Default email sender address

### SENTRY_DSN
**Value:** `<your-sentry-dsn>`
**Description:** For error tracking and monitoring

## After Adding Variables

1. Vercel will automatically trigger a new deployment
2. Wait for deployment to complete (check Deployments tab)
3. Visit your site URL to verify it works
4. Test login and basic functionality

## Important Notes

⚠️ **All three required variables must be set** for the application to work properly.

🔒 **Keep SECRET_KEY secure** - Never commit it to Git or share it publicly.

💾 **DATABASE_URL is critical** - Without it, the app will try to use SQLite which doesn't work in serverless environments.
