"""
Unit testy pre fakturačný systém
"""
import unittest
from datetime import date, timedelta
from app import app, db
from models import User, Supplier, Client, Invoice, InvoiceItem


class TestModels(unittest.TestCase):
    """Testy pre databázové modely"""
    
    def setUp(self):
        """Nastavenie testovacieho prostredia"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.app = app
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Vyčistenie po testoch"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_user_creation(self):
        """Test vytvorenia používateľa"""
        with app.app_context():
            user = User(
                email='test@example.com',
                name='Test User'
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            # Overenie
            saved_user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(saved_user)
            self.assertEqual(saved_user.name, 'Test User')
            self.assertTrue(saved_user.check_password('password123'))
            self.assertFalse(saved_user.check_password('wrongpassword'))
    
    def test_supplier_creation(self):
        """Test vytvorenia dodávateľa"""
        with app.app_context():
            user = User(email='test@example.com', name='Test')
            user.set_password('password')
            db.session.add(user)
            db.session.flush()
            
            supplier = Supplier(
                user_id=user.id,
                name='Test s.r.o.',
                street='Hlavná 1',
                city='Bratislava',
                zip_code='81101',
                ico='12345678'
            )
            db.session.add(supplier)
            db.session.commit()
            
            # Overenie
            saved_supplier = Supplier.query.filter_by(ico='12345678').first()
            self.assertIsNotNone(saved_supplier)
            self.assertEqual(saved_supplier.name, 'Test s.r.o.')
    
    def test_invoice_number_generation(self):
        """Test generovania čísla faktúry"""
        with app.app_context():
            user = User(email='test@example.com', name='Test')
            user.set_password('password')
            db.session.add(user)
            db.session.flush()
            
            supplier = Supplier(
                user_id=user.id,
                name='Test s.r.o.',
                street='Hlavná 1',
                city='Bratislava',
                zip_code='81101',
                ico='12345678',
                invoice_prefix='FV',
                next_invoice_number=1
            )
            db.session.add(supplier)
            db.session.commit()
            
            # Generovanie čísla
            invoice_number = supplier.get_next_invoice_number()
            year = date.today().year
            
            self.assertTrue(invoice_number.startswith('FV'))
            self.assertIn(str(year), invoice_number)
            self.assertEqual(supplier.next_invoice_number, 2)
    
    def test_invoice_totals_calculation(self):
        """Test výpočtu súm faktúry"""
        with app.app_context():
            user = User(email='test@example.com', name='Test')
            user.set_password('password')
            db.session.add(user)
            db.session.flush()
            
            supplier = Supplier(
                user_id=user.id,
                name='Test s.r.o.',
                street='Hlavná 1',
                city='Bratislava',
                zip_code='81101',
                ico='12345678'
            )
            db.session.add(supplier)
            db.session.flush()
            
            client = Client(
                user_id=user.id,
                name='Klient s.r.o.',
                street='Ulica 1',
                city='Košice',
                zip_code='04001'
            )
            db.session.add(client)
            db.session.flush()
            
            invoice = Invoice(
                user_id=user.id,
                supplier_id=supplier.id,
                client_id=client.id,
                invoice_number='FV20260001',
                variable_symbol='20260001',
                issue_date=date.today(),
                delivery_date=date.today(),
                due_date=date.today() + timedelta(days=14),
                vat_rate=20.0
            )
            db.session.add(invoice)
            db.session.flush()
            
            # Pridanie položiek
            item1 = InvoiceItem(
                invoice_id=invoice.id,
                description='Služba 1',
                quantity=2,
                unit_price=100.0
            )
            item1.calculate_total()
            db.session.add(item1)
            
            item2 = InvoiceItem(
                invoice_id=invoice.id,
                description='Služba 2',
                quantity=1,
                unit_price=50.0
            )
            item2.calculate_total()
            db.session.add(item2)
            
            db.session.flush()
            
            # Výpočet súm
            invoice.calculate_totals()
            
            # Overenie
            self.assertEqual(invoice.subtotal, 250.0)  # 2*100 + 1*50
            self.assertEqual(invoice.vat_amount, 50.0)  # 20% z 250
            self.assertEqual(invoice.total, 300.0)  # 250 + 50


class TestHelpers(unittest.TestCase):
    """Testy pre pomocné funkcie"""
    
    def test_suma_slovom(self):
        """Test konverzie sumy na slová"""
        from utils.helpers import suma_slovom
        
        self.assertIn('euro', suma_slovom(1))
        self.assertIn('eurá', suma_slovom(2))
        self.assertIn('eur', suma_slovom(5))
        self.assertIn('tisíc', suma_slovom(1000))
    
    def test_format_currency(self):
        """Test formátovania meny"""
        from utils.helpers import format_currency
        
        result = format_currency(1234.56)
        self.assertIn('1', result)
        self.assertIn('234', result)
        self.assertIn('56', result)


if __name__ == '__main__':
    unittest.main()
