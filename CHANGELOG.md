# Changelog

Všetky významné zmeny v projekte budú dokumentované v tomto súbore.

Formát je založený na [Keep a Changelog](https://keepachangelog.com/sk/1.0.0/),
a tento projekt dodržiava [Semantic Versioning](https://semver.org/lang/sk/).

## [2.1.0] - 2026-01-15

### Pridané
- ✅ **WeasyPrint** - Plnohodnotné PDF generovanie faktúr
- ✅ **Cache systém** - In-memory cache pre API volania (zníženie requestov)
- ✅ **Unit testy** - Základná testovacia infraštruktúra (`tests.py`)
- ✅ **Config.py** - Centralizovaná konfigurácia pre rôzne prostredia
- ✅ **.env.example** - Šablóna pre environment variables
- ✅ **PostgreSQL podpora** - Pripravené pre production databázu
- ✅ **CHANGELOG.md** - Dokumentácia zmien

### Zmenené
- 🔧 **requirements.txt** - Pridané verzie a nové závislosti
- 🔧 **README.md** - Aktualizovaná dokumentácia
- 🔧 **company_lookup.py** - Pridaný caching pre API volania (10 min TTL)

### Odstránené
- 🗑️ **rpo_service.py** - Duplicitný kód (nahradený `company_lookup.py`)

### Opravené
- 🐛 Optimalizované API volania s cachingom
- 🐛 Lepšia štruktúra projektu

---

## [2.0.0] - 2026-01-14

### Pridané
- 🎨 Moderný design s glassmorphism efektami
- 🌓 Dark/Light mode
- 📊 Dashboard s analytics
- 💳 PAY by square QR kódy
- 🔍 RPO/Ekosystém.Digital integrácia
- 👥 Multi-user systém
- 🎯 Demo režim
- 📅 Daňový kalendár SR
- 🔗 Verejné linky pre klientov
- 📈 Sledovanie zobrazení faktúr
- 📤 Export (CSV, Excel, XML)
- 🔄 Pravidelné faktúry (šablóny)
- 📝 Activity log (audit trail)

### Technické
- Flask 2.3+ framework
- SQLAlchemy 2.0+ ORM
- Tailwind CSS + Alpine.js
- SQLite databáza
- Gunicorn production server

---

## [1.0.0] - 2025-12-01

### Pridané
- 📝 Základná správa faktúr
- 👥 Správa klientov
- ⚙️ Nastavenia dodávateľa
- 🔐 Autentifikácia používateľov
- 📄 PDF export (základný)

---

## Legenda

- ✅ Pridané
- 🔧 Zmenené
- 🗑️ Odstránené
- 🐛 Opravené
- 🔒 Bezpečnosť
- 📝 Dokumentácia
- 🎨 Design
- ⚡ Výkon
