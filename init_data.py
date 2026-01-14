"""
Inicializačný skript pre fakturačný systém
Vytvorí databázu, pridá dodávateľa, klienta Slovak Security Agency
a vygeneruje prvú faktúru za webové služby.
"""
from datetime import date, timedelta
from app import app, db
from models import Supplier, Client, Invoice, InvoiceItem


def init_database():
    """Inicializuje databázu s ukážkovými dátami"""
    
    with app.app_context():
        # Vymazanie existujúcich dát (pre čistý štart)
        db.drop_all()
        db.create_all()
        
        print("=" * 60)
        print("INICIALIZÁCIA FAKTURAČNÉHO SYSTÉMU")
        print("=" * 60)
        
        # ==================================================================
        # 1. DODÁVATEĽ (Vaše firemné údaje - upravte podľa potreby)
        # ==================================================================
        supplier = Supplier(
            name="WebDev Solutions s.r.o.",
            street="Hlavná 123",
            city="Bratislava",
            zip_code="811 01",
            country="Slovenská republika",
            ico="12345678",
            dic="2012345678",
            ic_dph="",  # Neplatca DPH
            is_vat_payer=False,
            bank_name="Slovenská sporiteľňa",
            iban="SK89 0900 0000 0000 1234 5678",
            swift="GIBASKBX",
            email="info@webdev-solutions.sk",
            phone="+421 900 123 456",
            web="www.webdev-solutions.sk",
            invoice_prefix="FV",
            next_invoice_number=1
        )
        db.session.add(supplier)
        print("\n✓ Dodávateľ vytvorený: WebDev Solutions s.r.o.")
        
        # ==================================================================
        # 2. KLIENT - Slovak Security Agency (pán Čurma)
        # ==================================================================
        client_ssa = Client(
            name="Slovak Security Agency",
            contact_person="pán Čurma",
            street="Bezpečnostná 45",
            city="Bratislava",
            zip_code="821 08",
            country="Slovenská republika",
            ico="55667788",
            dic="2055667788",
            email="info@slovaksecurityagency.sk",
            phone="+421 905 555 555",
            note="Bezpečnostná agentúra - webové služby"
        )
        db.session.add(client_ssa)
        print("✓ Klient vytvorený: Slovak Security Agency (pán Čurma)")
        
        db.session.flush()  # Získame ID
        
        # ==================================================================
        # 3. FAKTÚRA - Za webové služby
        # ==================================================================
        invoice_number = supplier.get_next_invoice_number()
        today = date.today()
        
        invoice = Invoice(
            invoice_number=invoice_number,
            variable_symbol=invoice_number.replace('FV', ''),  # Len čísla
            supplier_id=supplier.id,
            client_id=client_ssa.id,
            issue_date=today,
            delivery_date=today,
            due_date=today + timedelta(days=14),
            payment_method='prevod',
            vat_rate=0,  # Neplatca DPH
            status=Invoice.STATUS_ISSUED,
            note="Ďakujeme za spoluprácu. V prípade otázok nás neváhajte kontaktovať."
        )
        db.session.add(invoice)
        db.session.flush()
        
        # ==================================================================
        # 4. POLOŽKY FAKTÚRY
        # ==================================================================
        items = [
            {
                'description': 'Registrácia domény slovaksecurityagency.sk (1 rok)',
                'quantity': 1,
                'unit': 'rok',
                'unit_price': 14.90
            },
            {
                'description': 'Webhosting Premium (1 rok) - 10GB SSD, SSL certifikát, email',
                'quantity': 1,
                'unit': 'rok',
                'unit_price': 59.90
            },
            {
                'description': 'Zálohovanie webu - automatické denné zálohy (1 rok)',
                'quantity': 1,
                'unit': 'rok',
                'unit_price': 24.90
            }
        ]
        
        for i, item_data in enumerate(items):
            item = InvoiceItem(
                invoice_id=invoice.id,
                description=item_data['description'],
                quantity=item_data['quantity'],
                unit=item_data['unit'],
                unit_price=item_data['unit_price'],
                position=i
            )
            item.calculate_total()
            db.session.add(item)
        
        db.session.flush()
        
        # Prepočítame sumy faktúry
        invoice.calculate_totals()
        db.session.commit()
        
        print(f"✓ Faktúra vytvorená: {invoice.invoice_number}")
        print(f"  - Odberateľ: {client_ssa.name}")
        print(f"  - Počet položiek: {len(items)}")
        print(f"  - Celková suma: {invoice.total:.2f} €")
        print(f"  - Splatnosť: {invoice.due_date.strftime('%d.%m.%Y')}")
        
        print("\n" + "=" * 60)
        print("INICIALIZÁCIA DOKONČENÁ")
        print("=" * 60)
        print(f"\nSpustite aplikáciu príkazom:")
        print(f"  python app.py")
        print(f"\nPotom otvorte prehliadač na adrese:")
        print(f"  http://localhost:5000")
        print("=" * 60)


if __name__ == '__main__':
    init_database()
