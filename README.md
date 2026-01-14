# 📄 Fakturačný Systém

Moderný fakturačný systém pre slovenské firmy s podporou PAY by square QR kódov, RPO integráciou a profesionálnym vzhľadom.

## ✨ Funkcie

### 💼 Správa faktúr
- Vytváranie, úprava a mazanie faktúr
- Automatické generovanie čísel faktúr
- Evidencia položiek s nákupnými a predajnými cenami
- Výpočet DPH a celkovej sumy
- Sledovanie stavu faktúr (vystavené, uhradené, po splatnosti, stornované)
- Hromadné operácie (označiť ako uhradené, vymazať)
- Export do CSV

### 👥 Správa klientov
- Evidencia klientov s kompletými údajmi
- Automatické vyhľadávanie firiem v RPO podľa IČO
- História fakturácie pre každého klienta

### 🏢 Nastavenia dodávateľa
- Kompletné údaje o vašej firme
- Nahrávanie pečiatky a podpisu
- Bankové údaje pre platby

### 📊 Dashboard a analytika
- Prehľad príjmov a ziskov
- Grafy mesačného vývoja
- Top odberatelia
- Klikateľné štatistiky s filtrovaním

### 🎨 Moderný dizajn
- Profesionálny vzhľad s Tailwind CSS
- Plne funkčný dark mode
- Responzívny dizajn pre mobily a tablety
- Animácie a interaktívne prvky

### 💳 PAY by square
- Automatické generovanie QR kódov pre platby
- Integrácia s FreeBySquare API
- Kompatibilné so slovenským bankovým systémom

## 🚀 Inštalácia

### Požiadavky
- Python 3.8+
- pip

### Kroky

1. **Klonujte repository**
```bash
git clone https://github.com/labovskyviktor-design/fakturacny-system.git
cd fakturacny-system
```

2. **Vytvorte virtuálne prostredie**
```bash
python -m venv venv
```

3. **Aktivujte virtuálne prostredie**
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. **Nainštalujte závislosti**
```bash
pip install -r requirements.txt
```

5. **Inicializujte databázu**
```bash
python init_data.py
```

6. **Spustite aplikáciu**
```bash
python app.py
```

7. **Otvorte prehliadač**
Prejdite na `http://localhost:5000`

## 📦 Závislosti

- Flask - Web framework
- Flask-SQLAlchemy - ORM pre databázu
- requests - HTTP knižnica pre API volania
- qrcode - Generovanie QR kódov
- Pillow - Práca s obrázkami
- WeasyPrint (voliteľné) - Generovanie PDF

## 🗄️ Štruktúra projektu

```
fakturacny_system/
├── app.py                 # Hlavná Flask aplikácia
├── models.py              # Databázové modely
├── init_data.py          # Inicializačný script
├── templates/            # HTML šablóny
│   ├── base.html
│   ├── dashboard.html
│   ├── invoices.html
│   ├── invoice_form.html
│   ├── invoice_detail.html
│   ├── invoice_pdf.html
│   ├── clients.html
│   └── settings.html
├── utils/                # Pomocné moduly
│   ├── helpers.py
│   ├── pay_by_square.py
│   ├── company_lookup.py
│   └── sk_companies_db.py
└── fakturacny_system.db # SQLite databáza
```

## 🔧 Konfigurácia

### Dodávateľ
Pri prvom spustení prejdite do **Nastavenia** a vyplňte údaje o vašej firme:
- Názov, adresa, IČO, DIČ
- Bankové údaje (IBAN, SWIFT)
- Email, telefón, web
- Prefix faktúr

### Klienti
Pridajte klientov cez **Klienti → Nový klient**
- Použite tlačidlo "Overiť RPO" pre automatické vyplnenie údajov podľa IČO

## 📱 Použitie

1. **Vytvorenie faktúry**: Faktúry → Nová faktúra
2. **Úprava faktúry**: Kliknite na číslo faktúry
3. **Označenie ako uhradené**: Detail faktúry → Označiť ako uhradené
4. **Export**: Faktúry → Export CSV
5. **PDF stiahnutie**: Detail faktúry → Stiahnuť PDF

## 🌙 Dark Mode

Systém automaticky detekuje preferovaný režim z vášho operačného systému.
Pre manuálne prepnutie kliknite na ikonu mesiaca/slnka v navigácii.

## 📄 Licencia

CC0-1.0 License - Verejná doména

## 👨‍💻 Autor

Viktor Labovský - [GitHub](https://github.com/labovskyviktor-design)

## 🤝 Prispievanie

Contributions, issues a feature requests sú vítané!

## ⚠️ Poznámky

- Tento systém je určený pre malé a stredné firmy na Slovensku
- Pre produkčné nasadenie odporúčame PostgreSQL namiesto SQLite
- Pravidelne zálohujte databázu
- Pre deployment odporúčame služby ako Heroku, Railway alebo Render

## 🚀 Deployment

Pre nasadenie do produkcie odporúčame:
- **Railway.app** - Najjednoduchšie, free tier dostupný
- **Render.com** - Dobré pre Python aplikácie
- **Heroku** - Klasická voľba
- **PythonAnywhere** - Špeciálne pre Python

Nikdy nedeployujte na GitHub Pages - Flask aplikácie vyžadujú server!
