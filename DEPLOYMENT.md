# 🚀 Deployment Guide - FakturaSK

Tento návod popisuje ako nasadiť FakturaSK na rôzne platformy.

---

## 📋 Pred deploymentom

### 1. Príprava projektu

```bash
# Klonujte repository
git clone https://github.com/labovskyviktor-design/fakturacny-system.git
cd fakturacny-system

# Vytvorte .env súbor
cp .env.example .env

# Upravte .env s production hodnotami
nano .env
```

### 2. Dôležité nastavenia

V `.env` súbore nastavte:

```bash
SECRET_KEY=<vygenerujte-silny-nahodny-kluc>
FLASK_ENV=production
DATABASE_URL=<production-database-url>
SESSION_COOKIE_SECURE=True
```

**Generovanie SECRET_KEY:**

```python
import secrets
print(secrets.token_hex(32))
```

---

## 🌐 Render.com (Odporúčané)

### Automatický deployment

1. **Fork repository** na GitHub
2. Prihlásenie na [Render.com](https://render.com)
3. **New → Web Service**
4. Pripojte GitHub repository
5. Render automaticky detekuje `render.yaml`

### Manuálne nastavenie

Ak `render.yaml` nefunguje:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Environment:** Python 3.12+

### Environment Variables

V Render dashboard nastavte:

```
SECRET_KEY=<your-secret-key>
FLASK_ENV=production
RENDER=true
```

### Databáza

**Dôležité:** Render používa ephemeral storage!

**Riešenie 1:** Použite Render PostgreSQL (odporúčané)

1. Vytvorte PostgreSQL databázu v Render
2. Skopírujte Internal Database URL
3. Nastavte environment variable:
   ```
   DATABASE_URL=<postgres-url>
   ```

**Riešenie 2:** Supabase PostgreSQL (odporúčané pre produkciu)

1. Vytvorte projekt na [Supabase](https://supabase.com)
2. V Dashboard → Project Settings → Database nájdete Connection String
3. Nastavte environment variable:
   ```
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```

**Výhody Supabase:**
- ✅ Bezplatný tier s 500MB databázy
- ✅ Automatické zálohy
- ✅ Realtime subscriptions
- ✅ Built-in authentication
- ✅ Storage pre súbory

---

## 🗄️ Supabase (Odporúčané)

### Vytvorenie projektu

1. Prihlásenie na [Supabase](https://supabase.com)
2. **New Project**
3. Zadajte názov projektu a heslo databázy
4. Vyberte región (Europe - Frankfurt pre najlepší výkon v SK)

### Získanie Connection String

1. **Project Settings → Database**
2. Skopírujte **Connection String** (URI format)
3. Nahraďte `[YOUR-PASSWORD]` vaším heslom

### Environment Variables

V Render/Railway/Vercel nastavte:

```
DATABASE_URL=postgresql://postgres:your-password@db.xxxxx.supabase.co:5432/postgres
```

### Migrácia z Railway

Ak migrujete existujúcu databázu z Railway:

```bash
# Spustite migration script
python migrate_db.py
```

Alebo manuálne pomocou pg_dump:

```bash
# Export z Railway
pg_dump "postgresql://postgres:password@hopper.proxy.rlwy.net:24076/railway" > backup.sql

# Import do Supabase
psql "postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres" < backup.sql
```

---

## 🚂 Railway.app

### Deployment

1. Prihlásenie na [Railway.app](https://railway.app)
2. **New Project → Deploy from GitHub**
3. Vyberte repository
4. Railway automaticky detekuje Python projekt

### Environment Variables

```
SECRET_KEY=<your-secret-key>
FLASK_ENV=production
```

### Databáza

1. **New → Database → PostgreSQL**
2. Railway automaticky nastaví `DATABASE_URL`

---

## 🟣 Heroku

### Deployment

```bash
# Nainštalujte Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Prihlásenie
heroku login

# Vytvorte aplikáciu
heroku create fakturask-app

# Pridajte PostgreSQL
heroku addons:create heroku-postgresql:mini

# Nastavte environment variables
heroku config:set SECRET_KEY=<your-secret-key>
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Otvorte aplikáciu
heroku open
```

### Procfile

Vytvorte `Procfile` (ak neexistuje):

```
web: gunicorn app:app
```

---

## 🐍 PythonAnywhere

### Deployment

1. Prihlásenie na [PythonAnywhere](https://www.pythonanywhere.com)
2. **Web → Add a new web app**
3. Vyberte **Flask** framework
4. Python 3.12+

### Nastavenie

1. **Clone repository:**
   ```bash
   cd ~
   git clone https://github.com/labovskyviktor-design/fakturacny-system.git
   cd fakturacny-system
   ```

2. **Vytvorte virtual environment:**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.12 fakturask
   pip install -r requirements.txt
   ```

3. **WSGI konfigurácia:**
   
   V PythonAnywhere Web tab → WSGI configuration file:
   
   ```python
   import sys
   import os
   
   # Pridajte cestu k projektu
   path = '/home/yourusername/fakturacny-system'
   if path not in sys.path:
       sys.path.append(path)
   
   # Environment variables
   os.environ['SECRET_KEY'] = 'your-secret-key'
   os.environ['FLASK_ENV'] = 'production'
   
   from app import app as application
   ```

4. **Reload** web app

---

## 🐳 Docker (Pokročilé)

### Dockerfile

Vytvorte `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Závislosti pre WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Python závislosti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Aplikácia
COPY . .

# Port
EXPOSE 5000

# Spustenie
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### Docker Compose

Vytvorte `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/fakturask
      - FLASK_ENV=production
    depends_on:
      - db
    volumes:
      - ./instance:/app/instance

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=fakturask
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Spustenie

```bash
# Build
docker-compose build

# Spustenie
docker-compose up -d

# Logy
docker-compose logs -f

# Zastavenie
docker-compose down
```

---

## 🔒 Bezpečnosť

### Checklist pre production:

- ✅ Silný `SECRET_KEY` (min. 32 znakov)
- ✅ `FLASK_ENV=production`
- ✅ `DEBUG=False`
- ✅ `SESSION_COOKIE_SECURE=True` (HTTPS)
- ✅ PostgreSQL namiesto SQLite
- ✅ Pravidelné zálohy databázy
- ✅ HTTPS certifikát (Let's Encrypt)
- ✅ Firewall pravidlá
- ✅ Rate limiting
- ✅ Monitoring (Sentry, LogRocket)

---

## 📊 Monitoring

### Sentry (Error tracking)

```bash
pip install sentry-sdk[flask]
```

V `app.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

---

## 🔄 Aktualizácia

### Render/Railway/Heroku

```bash
git add .
git commit -m "Update"
git push origin main
```

Automaticky sa nasadí nová verzia.

### PythonAnywhere

```bash
cd ~/fakturacny-system
git pull
# Reload web app v dashboard
```

---

## 🆘 Troubleshooting

### Problém: WeasyPrint nefunguje

**Riešenie:** Nainštalujte systémové závislosti:

```bash
# Ubuntu/Debian
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0

# Alpine (Docker)
apk add pango gdk-pixbuf
```

### Problém: Database locked (SQLite)

**Riešenie:** Použite PostgreSQL pre production.

### Problém: 502 Bad Gateway

**Riešenie:** Skontrolujte logy:

```bash
# Render
render logs

# Heroku
heroku logs --tail

# Docker
docker-compose logs -f web
```

---

## 📞 Podpora

- **GitHub Issues:** [github.com/labovskyviktor-design/fakturacny-system/issues](https://github.com/labovskyviktor-design/fakturacny-system/issues)
- **Email:** labovskyviktor@gmail.com

---

**Úspešný deployment! 🎉**
