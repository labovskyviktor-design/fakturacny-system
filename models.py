"""
Databázové modely pre fakturačný systém
"""
from datetime import datetime, date, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Supplier(db.Model):
    """Dodávateľ - moje firemné údaje"""
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # Názov firmy
    street = db.Column(db.String(200), nullable=False)  # Ulica a číslo
    city = db.Column(db.String(100), nullable=False)  # Mesto
    zip_code = db.Column(db.String(10), nullable=False)  # PSČ
    country = db.Column(db.String(50), default='Slovenská republika')
    ico = db.Column(db.String(20), nullable=False)  # IČO
    dic = db.Column(db.String(20))  # DIČ
    ic_dph = db.Column(db.String(20))  # IČ DPH (ak je platca)
    is_vat_payer = db.Column(db.Boolean, default=False)  # Platca DPH
    bank_name = db.Column(db.String(100))  # Názov banky
    iban = db.Column(db.String(34))  # IBAN
    swift = db.Column(db.String(11))  # SWIFT/BIC
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    web = db.Column(db.String(100))
    invoice_prefix = db.Column(db.String(10), default='')  # Prefix pre čísla faktúr
    next_invoice_number = db.Column(db.Integer, default=1)  # Ďalšie číslo faktúry
    
    # Pečiatka a podpis (Base64 kódované obrázky)
    stamp_image = db.Column(db.Text)  # Pečiatka (Base64)
    signature_image = db.Column(db.Text)  # Podpis (Base64)
    
    invoices = db.relationship('Invoice', backref='supplier', lazy=True)
    
    def get_next_invoice_number(self):
        """Vygeneruje ďalšie číslo faktúry"""
        year = datetime.now().year
        number = f"{self.invoice_prefix}{year}{self.next_invoice_number:04d}"
        self.next_invoice_number += 1
        return number


class Client(db.Model):
    """Klient - adresár odberateľov"""
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # Názov firmy / Meno
    contact_person = db.Column(db.String(100))  # Kontaktná osoba
    street = db.Column(db.String(200), nullable=False)  # Ulica a číslo
    city = db.Column(db.String(100), nullable=False)  # Mesto
    zip_code = db.Column(db.String(10), nullable=False)  # PSČ
    country = db.Column(db.String(50), default='Slovenská republika')
    ico = db.Column(db.String(20))  # IČO
    dic = db.Column(db.String(20))  # DIČ
    ic_dph = db.Column(db.String(20))  # IČ DPH
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    note = db.Column(db.Text)  # Poznámka
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    invoices = db.relationship('Invoice', backref='client', lazy=True)
    
    def __repr__(self):
        return f'<Client {self.name}>'


class Invoice(db.Model):
    """Faktúra"""
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(20), unique=True, nullable=False)  # Číslo faktúry
    variable_symbol = db.Column(db.String(20), nullable=False)  # Variabilný symbol
    
    # Dátumy
    issue_date = db.Column(db.Date, nullable=False, default=date.today)  # Dátum vystavenia
    delivery_date = db.Column(db.Date, nullable=False, default=date.today)  # Dátum dodania
    due_date = db.Column(db.Date, nullable=False)  # Dátum splatnosti
    
    # Forma úhrady
    PAYMENT_TRANSFER = 'prevod'
    PAYMENT_CASH = 'hotovost'
    PAYMENT_CHOICES = [
        (PAYMENT_TRANSFER, 'Bankový prevod'),
        (PAYMENT_CASH, 'Hotovosť'),
    ]
    payment_method = db.Column(db.String(20), default=PAYMENT_TRANSFER)
    
    # Vzťahy
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    # Sumy (ukladané pre históriu)
    subtotal = db.Column(db.Float, default=0.0)  # Medzisúčet bez DPH
    vat_rate = db.Column(db.Float, default=0.0)  # Sadzba DPH (0 alebo 20)
    vat_amount = db.Column(db.Float, default=0.0)  # Suma DPH
    total = db.Column(db.Float, default=0.0)  # Celková suma
    
    # Stav
    STATUS_DRAFT = 'draft'
    STATUS_ISSUED = 'issued'
    STATUS_PAID = 'paid'
    STATUS_OVERDUE = 'overdue'
    STATUS_CANCELLED = 'cancelled'
    status = db.Column(db.String(20), default=STATUS_ISSUED)
    paid_date = db.Column(db.Date)  # Dátum úhrady
    
    # Poznámky
    note = db.Column(db.Text)  # Poznámka na faktúre
    internal_note = db.Column(db.Text)  # Interná poznámka
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Položky faktúry
    items = db.relationship('InvoiceItem', backref='invoice', lazy=True, cascade='all, delete-orphan')
    
    def calculate_totals(self):
        """Prepočíta sumy faktúry"""
        self.subtotal = sum(item.total for item in self.items)
        if self.vat_rate > 0:
            self.vat_amount = round(self.subtotal * (self.vat_rate / 100), 2)
        else:
            self.vat_amount = 0.0
        self.total = round(self.subtotal + self.vat_amount, 2)
    
    def check_overdue(self):
        """Skontroluje či je faktúra po splatnosti"""
        if self.status == self.STATUS_ISSUED and self.due_date < date.today():
            self.status = self.STATUS_OVERDUE
    
    @property
    def is_paid(self):
        return self.status == self.STATUS_PAID
    
    @property
    def is_overdue(self):
        return self.status == self.STATUS_OVERDUE or (
            self.status == self.STATUS_ISSUED and self.due_date < date.today()
        )
    
    @property
    def total_cost(self):
        """Celková nákupná cena"""
        return sum((item.cost_price or 0) * item.quantity for item in self.items)
    
    @property
    def profit(self):
        """Celkový zisk z faktúry"""
        return round(self.subtotal - self.total_cost, 2)
    
    def __repr__(self):
        return f'<Invoice {self.invoice_number}>'


class InvoiceItem(db.Model):
    """Položka faktúry"""
    __tablename__ = 'invoice_items'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    
    description = db.Column(db.String(500), nullable=False)  # Názov položky
    item_note = db.Column(db.Text)  # Samostatný popis/poznámka k položke
    quantity = db.Column(db.Float, default=1.0)  # Množstvo
    unit = db.Column(db.String(20), default='ks')  # Jednotka (ks, hod, ...)
    unit_price = db.Column(db.Float, nullable=False)  # Jednotková cena
    cost_price = db.Column(db.Float, default=0.0)  # Nákupná cena (pre výpočet zisku)
    total = db.Column(db.Float, nullable=False)  # Celkom za položku
    
    position = db.Column(db.Integer, default=0)  # Poradie položky
    
    def calculate_total(self):
        """Vypočíta celkovú cenu položky"""
        self.total = round(self.quantity * self.unit_price, 2)
    
    @property
    def profit(self):
        """Vypočíta zisk z položky"""
        cost = (self.cost_price or 0) * self.quantity
        return round(self.total - cost, 2)
    
    def __repr__(self):
        return f'<InvoiceItem {self.description[:30]}>'


class ActivityLog(db.Model):
    """Audit log - história akcií v systéme"""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Typ akcie
    ACTION_INVOICE_CREATED = 'invoice_created'
    ACTION_INVOICE_EDITED = 'invoice_edited'
    ACTION_INVOICE_PAID = 'invoice_paid'
    ACTION_INVOICE_CANCELLED = 'invoice_cancelled'
    ACTION_INVOICE_DELETED = 'invoice_deleted'
    ACTION_CLIENT_CREATED = 'client_created'
    ACTION_CLIENT_EDITED = 'client_edited'
    
    action = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    # Referencie
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id', ondelete='SET NULL'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='SET NULL'), nullable=True)
    
    # Dodatočné údaje (JSON)
    extra_data = db.Column(db.Text)  # JSON s dodatočnými informáciami
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Vzťahy
    invoice = db.relationship('Invoice', backref=db.backref('activity_logs', lazy=True))
    client = db.relationship('Client', backref=db.backref('activity_logs', lazy=True))
    
    @classmethod
    def log(cls, action, description, invoice_id=None, client_id=None, extra_data=None):
        """Pomocná metóda na vytvorenie záznamu"""
        import json
        log_entry = cls(
            action=action,
            description=description,
            invoice_id=invoice_id,
            client_id=client_id,
            extra_data=json.dumps(extra_data) if extra_data else None
        )
        db.session.add(log_entry)
        return log_entry
    
    def __repr__(self):
        return f'<ActivityLog {self.action}: {self.description[:30]}>'
