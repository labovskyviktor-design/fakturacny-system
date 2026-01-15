
## [2.1.1] - 2026-01-15 (Hotfix)

### Opravené
- 🐛 **Kritická chyba databázy** - Opravené zamykanie SQLite databázy inštaláciou Single Worker režimu
- 🐛 **Stuck Transactions** - Pridaný `db.session.rollback()` do global error handlerov
- 🐛 **Cache Error** - Opravené nesprávne použitie `@cached` dekorátora na metódach triedy
- ⚡ **Gunicorn Config** - Optimalizované pre Railway (1 worker, 4 threads, autorestart)
- 🎨 **500 Error Page** - Pridaná užívateľsky prívetivá stránka pre chyby servera

