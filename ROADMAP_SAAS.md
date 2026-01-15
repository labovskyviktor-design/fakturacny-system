# 🚀 Roadmap: Od Hobby Projektu k Profitabilnému SaaS

Tento dokument slúži ako strategický plán pre transformáciu **FakturaSK** na verejný, komerčný produkt.

---

## 🏗️ 1. Technická Stabilita (Priorita č. 1)

Nič nezabije SaaS rýchlejšie ako výpadky a stratené dáta. Pred spustením pre verejnosť **musíte** vyriešiť tieto body:

### 🛑 Kritické (Must-Have)
- [ ] **Databáza:** Migrácia z SQLite na **PostgreSQL**.
    - *Dôvod:* SQLite (aj s mojimi opravami) nezvládne 100+ používateľov naraz. PostgreSQL je priemyselný štandard.
- [ ] **Zálohovanie:** Automatické denné zálohy databázy (napr. na AWS S3 alebo cez Railway Backups).
    - *Stratégia:* 30-dňová história záloh.
- [ ] **Emailing:** Integrácia transakčného email providera (SendGrid, Postmark, AWS SES).
    - *Dôvod:* Gmail SMTP limituje počet emailov a často končí v spame.
- [ ] **Monitoring:** Nasadenie **Sentry** (pre chyby) a **UptimeRobot** (pre dostupnosť).

### ⚡ Výkon
- [ ] **Redis:** Pre session management a cachovanie.
- [ ] **Background Jobs:** Celery/Redis Queue pre generovanie PDF a posielanie emailov (aby to nebrzdilo web).

---

## 💎 2. Produktové Vylepšenia (Value Proposition)

Aby ľudia platili, systém musí byť lepší ako Excel alebo konkurencia zadarmo.

### 🌟 Kľúčové funkcie
- [ ] **Automatizácia:**
    - Pravidelné faktúry (Subscription billing) - "nastav a zabudni".
    - Automatické upomienky po splatnosti.
- [ ] **Integrácie:**
    - Bankové pohyby (import výpisov / API napojenie na banky).
    - Účtovné systémy (export do Pohody, Krosu).
- [ ] **Dashboard:**
    - Pokročilé grafy (Cashflow, DPH, Očakávané príjmy).
    - "Health check" podnikania.
- [ ] **Tímová spolupráca:** Viac používateľov pod jedným firemným účtom (účtovník + majiteľ).

---

## 💰 3. Biznis Model & Monetizácia

### Stratégia: Freemium
- **FREE:** Do 5 faktúr mesačne, základné funkcie. (Slúži na marketing).
- **PRO (5-9 €/mesiac):** Neobmedzené faktúry, PDF na email, vlastné logo, exporty.
- **ENTERPRISE (19+ €/mesiac):** API, viac používateľov, prioritná podpora.

### Platobná brána
- **Stripe:** Najjednoduchšia implementácia pre predplatné (Subscriptions).
- Automatická fakturácia za používanie systému (fakturačný systém, ktorý fakturuje sám seba!).

---

## ⚖️ 4. Legislatíva a Dôvera

### GDPR & Legal
- [ ] **VOP (Všeobecné obchodné podmienky):** Musíte mať jasne definované pravidlá.
- [ ] **GDPR Súhlasy:** Spracovateľská zmluva (keďže držíte dáta ich klientov).
- [ ] **SLA (Service Level Agreement):** Garancia dostupnosti (napr. 99.9%).

---

## 📅 Akčný Plán (Next Steps)

### Fáza 1: Hardening (1 mesiac)
1. Nasadiť PostgreSQL na Railway.
2. Nastaviť Sentry monitoring.
3. Implementovať SendGrid pre emaily.

### Fáza 2: Features (1-2 mesiace)
1. Dokončiť "Recurring Invoices".
2. Vytvoriť exporty pre účtovníkov (Pohoda XML).
3. Vylepšiť dizajn faktúr (viac šablón).

### Fáza 3: Launch (BETA)
1. Spustiť "Closed Beta" pre 10-20 známych/firiem zadarmo.
2. Zbierať feedback a opravovať chyby.
3. Pripraviť marketingový web (Landing page).

---

### 💡 Tip na záver
**Nekonkurujte cenou.** SuperFaktúra a iKros sú zabehnuté. Konkurujte **UX (používateľským zážitkom)**, rýchlosťou a špecifickými funkciami pre malých živnostníkov (napr. jednoduchosť).
