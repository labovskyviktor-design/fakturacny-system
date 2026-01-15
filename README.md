<div align="center">

# 💸 FakturaSK

### Profesionalny fakturacny system pre slovenske firmy

[![Live Demo](https://img.shields.io/badge/Live%20Demo-fakturask.onrender.com-blue?style=for-the-badge)](https://fakturacny-system.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-CC0--1.0-lightgrey?style=for-the-badge)](LICENSE)

[Spustit Demo](#-demo) • [Funkcie](#-funkcie) • [Instalacia](#-instalacia) • [Dokumentacia](#-pouzitie)

</div>

---

## 🎯 O projekte

FakturaSK je moderny fakturacny system navrhnuty specialne pre slovenske firmy a zivnostnikov.
Ponuka kompletnu spravu faktur, klientov a financnych prehladov s podporou slovenskych standardov
vratane PAY by square QR kodov a RPO integracie.

### 🌟 Hlavne vyhody

- ✅ **PAY by square QR kody** - Kompatibilne so vsetkymi slovenskymi bankami
- ✅ **RPO integracia** - Automaticke vyhladavanie firiem podla ICO
- ✅ **Multi-user system** - Kazdy uzivatel ma vlastne data
- ✅ **Demo rezim** - Vyskusajte bez registracie
- ✅ **Dark mode** - Setrite oci pri nocnej praci
- ✅ **Responzivny dizajn** - Funguje na mobile aj desktope

---

## 📸 Demo

**Vyskusajte si system bez registracie!**

👉 [**Spustit Demo**](https://fakturacny-system.onrender.com/demo)

> ⚠️ V demo rezime sa data neukladaju a budu vymazane po odhlaseni.

---

## ✨ Funkcie

<table>
<tr>
<td width="50%">

### 💼 Spravy faktur
- Vytvaranie, uprava a mazanie faktur
- Automaticke generovanie cisiel
- Polozky s nakupnymi a predajnymi cenami
- Vypocet DPH a celkovej sumy
- Sledovanie stavov (vystavene, uhradene, po splatnosti)
- Export do CSV a PDF

### 👥 Sprava klientov
- Kompletna evidencia klientov
- Automaticke vyhladavanie v RPO
- Historia fakturacie

</td>
<td width="50%">

### 📊 Dashboard & Analytika
- Prehlad prijmov a ziskov
- Mesacne grafy vyvoja
- Top odberatelia
- Klikatelne statistiky

### 🎨 Dizajn
- Tailwind CSS
- Dark / Light mode
- Responzivny layout
- Moderne animacie

### 🔐 Bezpecnost
- Multi-user autentifikacia
- Hashovane hesla (Werkzeug)
- GDPR kompatibilne

</td>
</tr>
</table>

---

## 🚀 Instalacia

### Poziadavky
- Python 3.8+
- pip

### Rychly start

```bash
# 1. Klonujte repository
git clone https://github.com/labovskyviktor-design/fakturacny-system.git
cd fakturacny-system

# 2. Vytvorte virtualne prostredie
python -m venv venv

# 3. Aktivujte prostredie
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Nainstalujte zavislosti
pip install -r requirements.txt

# 5. Spustite aplikaciu
python app.py
```

👉 Otvorte prehliadac na `http://localhost:5000`

---

## 📦 Zavislosti

| Balicek | Pouzitie |
|---------|----------|
| Flask | Web framework |
| Flask-SQLAlchemy | ORM pre databazu |
| Flask-Login | Autentifikacia |
| requests | HTTP klient pre API |
| qrcode | Generovanie QR kodov |
| Pillow | Praca s obrazkami |
| Werkzeug | Bezpecnost hesiel |

---

## 📁 Struktura projektu

```
fakturacny_system/
├── app.py                 # Hlavna Flask aplikacia
├── models.py              # Databazove modely
├── templates/             # HTML sablony
│   ├── auth/              # Login, Register
│   ├── base.html          # Zakladny layout
│   ├── dashboard.html     # Hlavny prehlad
│   ├── invoices.html      # Zoznam faktur
│   ├── invoice_form.html  # Formular faktury
│   ├── clients.html       # Sprava klientov
│   ├── settings.html      # Nastavenia
│   ├── terms.html         # Podmienky pouzivania
│   └── gdpr.html          # GDPR
├── utils/                 # Pomocne moduly
│   ├── helpers.py         # Pomocne funkcie
│   ├── pay_by_square.py   # PAY by square
│   └── company_lookup.py  # RPO vyhladavanie
├── requirements.txt       # Zavislosti
└── render.yaml            # Render.com konfiguracia
```

---

## 📱 Pouzitie

| Akcia | Postup |
|-------|--------|
| Nova faktura | Faktury → Nova faktura |
| Uprava faktury | Kliknite na cislo faktury |
| Oznacit ako uhradene | Detail faktury → Oznacit ako uhradene |
| Export | Faktury → Export CSV |
| PDF stiahnutie | Detail faktury → Stiahnut PDF |

---

## ☁️ Deployment

### Render.com (Odporucane)

1. Fork tohto repository
2. Prihlaste sa na [Render.com](https://render.com)
3. New → Web Service → Connect repository
4. Render automaticky detekuje konfiguraciu z `render.yaml`

### Ine platformy

- **Railway.app** - Jednoduche, free tier
- **Heroku** - Klasicka volba
- **PythonAnywhere** - Specialne pre Python

> ⚠️ Nikdy nedeployujte na GitHub Pages - Flask aplikacie vyzaduju server!

---

## 📄 Pravne

- [Podmienky pouzivania](/terms)
- [Ochrana osobnych udajov (GDPR)](/gdpr)

---

## 👨‍💻 Autor

<div align="center">

**Bc. Viktor Labovsky**

[![Portfolio](https://img.shields.io/badge/Portfolio-labovskyviktor--design.github.io-blue?style=flat-square)](https://labovskyviktor-design.github.io/portfolko/)
[![GitHub](https://img.shields.io/badge/GitHub-labovskyviktor--design-black?style=flat-square&logo=github)](https://github.com/labovskyviktor-design)
[![Email](https://img.shields.io/badge/Email-labovskyviktor%40gmail.com-red?style=flat-square&logo=gmail)](mailto:labovskyviktor@gmail.com)

</div>

---

## 📃 Licencia

Tento projekt je licencovany pod **CC0-1.0 License** - pozri [LICENSE](LICENSE) pre detaily.

---

<div align="center">

**❤️ Made with love in Slovakia**

© 2026 Bc. Viktor Labovsky. Vsetky prava vyhradene.

</div>
