# 🚂 Railway Deployment - Riešenie Internal Server Error

## ✅ Vykonané opravy

### 1. **requirements.txt**
- ❌ Odstránený WeasyPrint (spôsoboval build errors)
- ✅ Opravený psycopg2-binary (bez platform condition)

### 2. **app.py**
- ✅ Pridaná detekcia Railway prostredia (`RAILWAY_ENVIRONMENT`)
- ✅ Podpora pre PostgreSQL cez `DATABASE_URL`
- ✅ Automatická oprava `postgres://` → `postgresql://`

### 3. **Nové súbory**
- ✅ `nixpacks.toml` - Railway build konfigurácia
- ✅ `Procfile` - Gunicorn start command

---

## 🚀 Deployment kroky

### Krok 1: Push zmeny na GitHub

```bash
git add .
git commit -m "Fix Railway deployment - remove WeasyPrint, add Railway config"
git push origin main
```

### Krok 2: Railway nastavenia

V Railway dashboard:

#### **Environment Variables** (Settings → Variables):

```
SECRET_KEY=<vygeneruj-silny-kluc>
RAILWAY_ENVIRONMENT=production
```

**Generovanie SECRET_KEY:**
```python
import secrets
print(secrets.token_hex(32))
```

#### **Voliteľne - PostgreSQL databáza:**

1. V Railway projekte: **New → Database → PostgreSQL**
2. Railway automaticky nastaví `DATABASE_URL`
3. Aplikácia to automaticky detekuje

---

## 🔍 Kontrola deployment

### 1. Sledovanie buildov

V Railway:
- **Deployments** → Klikni na posledný deployment
- Sleduj **Build Logs** a **Deploy Logs**

### 2. Kontrola logov

```bash
# V Railway CLI (ak máš nainštalované)
railway logs
```

Alebo v Railway dashboard: **Deployments → View Logs**

### 3. Testovanie

Po úspešnom deploymete:
1. Otvor Railway URL
2. Skús sa prihlásiť/registrovať
3. Vytvor testovaciu faktúru

---

## ⚠️ Časté problémy

### Problém: "ModuleNotFoundError: No module named 'weasyprint'"

**Riešenie:** ✅ Už opravené - WeasyPrint odstránený z requirements.txt

### Problém: "Database is locked"

**Riešenie:** Použite PostgreSQL namiesto SQLite:
```bash
# V Railway projekte
New → Database → PostgreSQL
```

### Problém: "Application failed to respond"

**Riešenie:** Skontrolujte PORT:
- Railway automaticky nastaví `$PORT` environment variable
- Gunicorn v `Procfile` používa `0.0.0.0:$PORT`

### Problém: "Internal Server Error" stále pretrváva

**Riešenie:** Pozrite logy:

1. **Railway Dashboard → Deployments → View Logs**
2. Hľadajte chybové hlášky:
   ```
   ModuleNotFoundError: ...
   ImportError: ...
   sqlalchemy.exc.OperationalError: ...
   ```
3. Pošlite mi konkrétnu chybu

---

## 📊 Overenie funkčnosti

### Checklist:

- ✅ Build úspešný (zelená fajka v Railway)
- ✅ Deploy úspešný
- ✅ Aplikácia odpovedá na URL
- ✅ Prihlásenie funguje
- ✅ Demo režim funguje
- ✅ Faktúry sa vytvárajú

---

## 🆘 Ak problém pretrváva

**Pošlite mi:**

1. **Build logs** z Railway (celý output)
2. **Deploy logs** z Railway
3. **Screenshot** chybovej stránky
4. **Railway environment variables** (bez SECRET_KEY hodnoty)

**Kontakt:**
- GitHub Issues
- Email: labovskyviktor@gmail.com

---

## 🎉 Po úspešnom deploymete

### Odporúčané nastavenia:

1. **Custom doména:**
   - Railway Settings → Domains → Add Custom Domain

2. **PostgreSQL databáza:**
   - New → Database → PostgreSQL
   - Automaticky sa pripojí cez `DATABASE_URL`

3. **Monitoring:**
   - Railway má built-in metrics
   - Settings → Observability

4. **Automatic deployments:**
   - Settings → GitHub → Enable Auto Deploy

---

**Status:** ✅ Opravené a pripravené na deployment!
