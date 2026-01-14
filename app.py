"""
FakturaÄŤnĂ˝ systĂ©m - Flask aplikĂˇcia
Klon systĂ©mov SuperFaktĂşra / Kros
"""
import os
import io
import csv
from datetime import date, timedelta
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, Response, jsonify
from models import db, Supplier, Client, Invoice, InvoiceItem, ActivityLog
from utils.company_lookup import lookup_company
from utils.pay_by_square import generate_qr_code_base64, generate_sepa_qr
import base64
from utils import (
    suma_slovom, format_currency, format_date_sk,
    get_payment_method_label, get_status_label, get_status_color,
    generate_pay_by_square
)

# Vytvoríme Flask aplikáciu
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tajny-kluc-pre-fakturacny-system-2024')

# Databáza - použijeme /tmp na Renderi (ephemeral storage)
if os.environ.get('RENDER'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/fakturacny_system.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fakturacny_system.db'
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializácia databázy
db.init_app(app)

# Registrácia pomocných funkcií do Jinja2
app.jinja_env.globals.update(
    suma_slovom=suma_slovom,
    format_currency=format_currency,
    format_date_sk=format_date_sk,
    get_payment_method_label=get_payment_method_label,
    get_status_label=get_status_label,
    get_status_color=get_status_color,
    generate_pay_by_square=generate_pay_by_square,
)


# ==============================================================================
# DASHBOARD
# ==============================================================================

@app.route('/')
def dashboard():
    """HlavnĂ˝ dashboard s prehÄľadom a analytics"""
    supplier = Supplier.query.first()
    
    # VĹˇetky faktĂşry
    invoices = Invoice.query.all()
    
    # AktualizujemeÂ stavy po splatnosti
    for inv in invoices:
        inv.check_overdue()
    db.session.commit()
    
    # ZĂˇkladnĂ© Ĺˇtatistiky
    total_invoices = len(invoices)
    paid_invoices = [i for i in invoices if i.status == Invoice.STATUS_PAID]
    overdue_invoices = [i for i in invoices if i.is_overdue]
    issued_invoices = [i for i in invoices if i.status == Invoice.STATUS_ISSUED]
    
    total_revenue = sum(i.total for i in paid_invoices)  # PrijatĂ© platby
    total_pending = sum(i.total for i in issued_invoices)  # ÄŚakĂˇ na Ăşhradu
    total_overdue = sum(i.total for i in overdue_invoices)  # Po splatnosti
    
    # === ANALYTICS ===
    # Celkovo fakturovanĂ© (vĹˇetky okrem stornovanĂ˝ch)
    active_invoices = [i for i in invoices if i.status != Invoice.STATUS_CANCELLED]
    total_invoiced = sum(i.total for i in active_invoices)
    
    # CelkovĂ˝ zisk (fakturovane - nĂˇkupnĂ© ceny)
    total_profit = sum(i.profit for i in paid_invoices)
    total_cost = sum(i.total_cost for i in paid_invoices)
    
    # PredpokladanĂ˝ prĂ­jem (faktĂşry v splatnosti)
    expected_income = total_pending
    
    # Top odberateľ
    client_totals = defaultdict(float)
    for inv in paid_invoices:
        client_totals[inv.client_id] += inv.total
    
    top_client = None
    top_client_amount = 0
    if client_totals:
        top_client_id = max(client_totals, key=client_totals.get)
        top_client = Client.query.get(top_client_id)
        top_client_amount = client_totals[top_client_id]
    
    # Mesačný prehľad (posledných 6 mesiacov)
    monthly_data = []
    today = date.today()
    for i in range(5, -1, -1):
        month_start = date(today.year, today.month, 1) - timedelta(days=30*i)
        month_name = month_start.strftime('%b %Y')
        month_revenue = sum(
            inv.total for inv in paid_invoices 
            if inv.paid_date and inv.paid_date.month == month_start.month and inv.paid_date.year == month_start.year
        )
        month_profit = sum(
            inv.profit for inv in paid_invoices 
            if inv.paid_date and inv.paid_date.month == month_start.month and inv.paid_date.year == month_start.year
        )
        monthly_data.append({
            'month': month_name,
            'revenue': month_revenue,
            'profit': month_profit
        })
    
    # PoslednĂˇ aktivita
    recent_activity = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(10).all()
    
    # PoslednĂ© faktĂşry
    recent_invoices = Invoice.query.order_by(Invoice.created_at.desc()).limit(10).all()
    
    return render_template('dashboard.html',
        supplier=supplier,
        total_invoices=total_invoices,
        paid_count=len(paid_invoices),
        overdue_count=len(overdue_invoices),
        issued_count=len(issued_invoices),
        total_revenue=total_revenue,
        total_pending=total_pending,
        total_overdue=total_overdue,
        # Analytics
        total_invoiced=total_invoiced,
        total_profit=total_profit,
        total_cost=total_cost,
        expected_income=expected_income,
        top_client=top_client,
        top_client_amount=top_client_amount,
        monthly_data=monthly_data,
        recent_activity=recent_activity,
        recent_invoices=recent_invoices
    )


# ==============================================================================
# KLIENTI
# ==============================================================================

@app.route('/clients')
def clients_list():
    """Zoznam klientov"""
    clients = Client.query.order_by(Client.name).all()
    return render_template('clients.html', clients=clients)


@app.route('/clients/add', methods=['GET', 'POST'])
def client_add():
    """Pridanie nového klienta"""
    if request.method == 'POST':
        client = Client(
            name=request.form['name'],
            contact_person=request.form.get('contact_person', ''),
            street=request.form['street'],
            city=request.form['city'],
            zip_code=request.form['zip_code'],
            country=request.form.get('country', 'Slovenská republika'),
            ico=request.form.get('ico', ''),
            dic=request.form.get('dic', ''),
            ic_dph=request.form.get('ic_dph', ''),
            email=request.form.get('email', ''),
            phone=request.form.get('phone', ''),
            note=request.form.get('note', '')
        )
        db.session.add(client)
        db.session.commit()
        flash(f'Klient "{client.name}" bol úspešne pridaný.', 'success')
        return redirect(url_for('clients_list'))
    
    return render_template('client_form.html', client=None)


@app.route('/clients/<int:client_id>/edit', methods=['GET', 'POST'])
def client_edit(client_id):
    """Úprava klienta"""
    client = Client.query.get_or_404(client_id)
    
    if request.method == 'POST':
        client.name = request.form['name']
        client.contact_person = request.form.get('contact_person', '')
        client.street = request.form['street']
        client.city = request.form['city']
        client.zip_code = request.form['zip_code']
        client.country = request.form.get('country', 'Slovenská republika')
        client.ico = request.form.get('ico', '')
        client.dic = request.form.get('dic', '')
        client.ic_dph = request.form.get('ic_dph', '')
        client.email = request.form.get('email', '')
        client.phone = request.form.get('phone', '')
        client.note = request.form.get('note', '')
        
        db.session.commit()
        flash(f'Klient "{client.name}" bol úspešne upravený.', 'success')
        return redirect(url_for('clients_list'))
    
    return render_template('client_form.html', client=client)


@app.route('/clients/<int:client_id>/delete', methods=['POST'])
def client_delete(client_id):
    """Vymazanie klienta"""
    client = Client.query.get_or_404(client_id)
    
    # Kontrola či nemá faktúry
    if client.invoices:
        flash(f'Klient "{client.name}" nemôže byť vymazaný, pretože má faktúry.', 'error')
        return redirect(url_for('clients_list'))
    
    name = client.name
    db.session.delete(client)
    db.session.commit()
    flash(f'Klient "{name}" bol úspešne vymazaný.', 'success')
    return redirect(url_for('clients_list'))


# ==============================================================================
# FAKTÚRY
# ==============================================================================

@app.route('/invoices')
def invoices_list():
    """Zoznam faktúr"""
    status_filter = request.args.get('status', '')
    search_query = request.args.get('q', '')
    
    query = Invoice.query
    
    # Aktualizujeme stavy pred filtrovaním
    all_invoices = Invoice.query.all()
    for inv in all_invoices:
        inv.check_overdue()
    db.session.commit()
    
    # Filtre
    if status_filter == 'overdue':
        # Filtrujeme faktúry po splatnosti
        query = query.filter(Invoice.is_overdue == True)
    elif status_filter:
        query = query.filter_by(status=status_filter)
    
    # Vyhľadávanie
    if search_query:
        query = query.join(Client).filter(
            (Invoice.invoice_number.contains(search_query)) |
            (Invoice.variable_symbol.contains(search_query)) |
            (Client.name.contains(search_query))
        )
    
    invoices = query.order_by(Invoice.created_at.desc()).all()
    
    return render_template('invoices.html', 
        invoices=invoices,
        status_filter=status_filter,
        search_query=search_query
    )


@app.route('/invoices/add', methods=['GET', 'POST'])
def invoice_add():
    """Vytvorenie novej faktúry"""
    supplier = Supplier.query.first()
    clients = Client.query.order_by(Client.name).all()
    
    if not supplier:
        flash('Najprv musíte nastaviť údaje dodávateľa.', 'error')
        return redirect(url_for('supplier_settings'))
    
    if not clients:
        flash('Najprv musíte pridať aspoň jedného klienta.', 'error')
        return redirect(url_for('client_add'))
    
    if request.method == 'POST':
        try:
            # Získame klienta
            client_id = request.form.get('client_id')
            if not client_id:
                flash('Vyberte klienta.', 'error')
                return redirect(url_for('invoice_add'))
            
            client = Client.query.get(client_id)
            if not client:
                flash('Klient neexistuje.', 'error')
                return redirect(url_for('invoice_add'))
            
            # Generujeme číslo faktúry
            invoice_number = supplier.get_next_invoice_number()
            
            # Vytvoríme faktúru
            invoice = Invoice(
                invoice_number=invoice_number,
                variable_symbol=invoice_number.replace('/', ''),
                supplier_id=supplier.id,
                client_id=client.id,
                issue_date=date.fromisoformat(request.form['issue_date']),
                delivery_date=date.fromisoformat(request.form['delivery_date']),
                due_date=date.fromisoformat(request.form['due_date']),
                payment_method=request.form.get('payment_method', 'prevod'),
                vat_rate=float(request.form.get('vat_rate', 0) or 0),
                note=request.form.get('note', ''),
                status=Invoice.STATUS_ISSUED
            )
            
            db.session.add(invoice)
            db.session.flush()
            
            # Pridáme položky
            descriptions = request.form.getlist('item_description[]')
            item_notes = request.form.getlist('item_note[]')
            quantities = request.form.getlist('item_quantity[]')
            units = request.form.getlist('item_unit[]')
            unit_prices = request.form.getlist('item_unit_price[]')
            cost_prices = request.form.getlist('item_cost_price[]')
            
            items_added = 0
            for i, desc in enumerate(descriptions):
                if desc and desc.strip():
                    try:
                        qty = float(quantities[i]) if i < len(quantities) and quantities[i] else 1
                        price = float(unit_prices[i]) if i < len(unit_prices) and unit_prices[i] else 0
                        cost = float(cost_prices[i]) if i < len(cost_prices) and cost_prices[i] else 0
                    except (ValueError, IndexError):
                        qty, price, cost = 1, 0, 0
                    
                    item = InvoiceItem(
                        invoice_id=invoice.id,
                        description=desc.strip(),
                        item_note=item_notes[i] if i < len(item_notes) else '',
                        quantity=qty,
                        unit=units[i] if i < len(units) and units[i] else 'ks',
                        unit_price=price,
                        cost_price=cost,
                        position=i
                    )
                    item.calculate_total()
                    db.session.add(item)
                    items_added += 1
            
            if items_added == 0:
                db.session.rollback()
                flash('Pridajte aspoň jednu položku.', 'error')
                return redirect(url_for('invoice_add'))
            
            db.session.flush()
            invoice.calculate_totals()
            
            # Activity log
            ActivityLog.log(
                ActivityLog.ACTION_INVOICE_CREATED,
                f'Faktúra {invoice.invoice_number} vytvorená pre {client.name}',
                invoice_id=invoice.id,
                client_id=client.id,
                extra_data={'total': invoice.total}
            )
            
            db.session.commit()
            
            flash(f'Faktúra {invoice.invoice_number} bola úspešne vytvorená.', 'success')
            return redirect(url_for('invoice_detail', invoice_id=invoice.id))
            
        except ValueError as e:
            db.session.rollback()
            print(f'ValueError pri vytváraní faktúry: {e}')
            import traceback
            traceback.print_exc()
            flash(f'Chyba vo formáte dát: {str(e)}', 'error')
            return redirect(url_for('invoice_add'))
            
        except Exception as e:
            db.session.rollback()
            print(f'Chyba pri vytváraní faktúry: {e}')
            import traceback
            traceback.print_exc()
            flash(f'Chyba pri vytváraní faktúry: {str(e)}', 'error')
            return redirect(url_for('invoice_add'))
    
    # Predvyplnené dátumy
    today = date.today()
    default_due_date = today + timedelta(days=14)
    
    return render_template('invoice_form.html',
        invoice=None,
        supplier=supplier,
        clients=clients,
        today=today,
        default_due_date=default_due_date
    )


@app.route('/invoices/<int:invoice_id>')
def invoice_detail(invoice_id):
    """Detail faktúry"""
    invoice = Invoice.query.get_or_404(invoice_id)
    
    # Generujeme QR kód
    qr_code = None
    if invoice.payment_method == 'prevod' and invoice.supplier.iban:
        try:
            qr_code = generate_qr_code_base64(
                amount=invoice.total,
                iban=invoice.supplier.iban,
                swift=invoice.supplier.swift or '',
                variable_symbol=invoice.variable_symbol,
                beneficiary_name=invoice.supplier.name,
                due_date=invoice.due_date.strftime('%Y%m%d')
            )
        except Exception as e:
            print(f"Chyba pri generovaní QR kódu: {e}")
    
    return render_template('invoice_detail.html',
        invoice=invoice,
        qr_code=qr_code
    )


@app.route('/invoices/<int:invoice_id>/pdf')
def invoice_pdf(invoice_id):
    """Stiahnutie faktúry ako PDF"""
    invoice = Invoice.query.get_or_404(invoice_id)
    
    # Generujeme QR kód
    qr_code = None
    if invoice.payment_method == 'prevod' and invoice.supplier.iban:
        try:
            qr_code = generate_qr_code_base64(
                amount=invoice.total,
                iban=invoice.supplier.iban,
                swift=invoice.supplier.swift or '',
                variable_symbol=invoice.variable_symbol,
                beneficiary_name=invoice.supplier.name,
                due_date=invoice.due_date.strftime('%Y%m%d')
            )
        except Exception as e:
            print(f"Chyba pri generovaní QR kódu: {e}")
    
    # Renderujeme HTML šablónu
    html = render_template('invoice_pdf.html',
        invoice=invoice,
        qr_code=qr_code
    )
    
    # Pokúsime sa použiť WeasyPrint
    try:
        from weasyprint import HTML, CSS
        
        css = CSS(string='''
            @page {
                size: A4;
                margin: 1cm;
            }
            body {
                font-family: Arial, sans-serif;
                font-size: 10pt;
            }
        ''')
        
        pdf = HTML(string=html).write_pdf(stylesheets=[css])
        
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=faktura_{invoice.invoice_number}.pdf'
        return response
        
    except ImportError:
        # Ak WeasyPrint nie je dostupný, vrátime HTML
        flash('WeasyPrint nie je nainštalovaný. Stiahnite HTML verziu.', 'warning')
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=faktura_{invoice.invoice_number}.html'
        return response


@app.route('/invoices/<int:invoice_id>/mark-paid', methods=['POST'])
def invoice_mark_paid(invoice_id):
    """Označiť faktúru ako uhradenú"""
    invoice = Invoice.query.get_or_404(invoice_id)
    invoice.status = Invoice.STATUS_PAID
    invoice.paid_date = date.today()
    
    ActivityLog.log(
        ActivityLog.ACTION_INVOICE_PAID,
        f'Faktúra {invoice.invoice_number} označená ako uhradená',
        invoice_id=invoice.id,
        client_id=invoice.client_id,
        extra_data={'total': invoice.total, 'paid_date': str(invoice.paid_date)}
    )
    
    db.session.commit()
    flash(f'Faktúra {invoice.invoice_number} bola označená ako uhradená.', 'success')
    return redirect(url_for('invoice_detail', invoice_id=invoice.id))


@app.route('/invoices/<int:invoice_id>/cancel', methods=['POST'])
def invoice_cancel(invoice_id):
    """Stornovať faktúru"""
    invoice = Invoice.query.get_or_404(invoice_id)
    invoice.status = Invoice.STATUS_CANCELLED
    
    ActivityLog.log(
        ActivityLog.ACTION_INVOICE_CANCELLED,
        f'Faktúra {invoice.invoice_number} stornovaná',
        invoice_id=invoice.id,
        client_id=invoice.client_id
    )
    
    db.session.commit()
    flash(f'Faktúra {invoice.invoice_number} bola stornovaná.', 'success')
    return redirect(url_for('invoice_detail', invoice_id=invoice.id))


@app.route('/invoices/<int:invoice_id>/delete', methods=['POST'])
def invoice_delete(invoice_id):
    """Vymazať faktúru"""
    invoice = Invoice.query.get_or_404(invoice_id)
    number = invoice.invoice_number
    client_id = invoice.client_id
    
    ActivityLog.log(
        ActivityLog.ACTION_INVOICE_DELETED,
        f'Faktúra {number} vymazaná',
        client_id=client_id
    )
    
    db.session.delete(invoice)
    db.session.commit()
    flash(f'Faktúra {number} bola vymazaná.', 'success')
    return redirect(url_for('invoices_list'))


@app.route('/invoices/<int:invoice_id>/edit', methods=['GET', 'POST'])
def invoice_edit(invoice_id):
    """Editácia existujúcej faktúry"""
    invoice = Invoice.query.get_or_404(invoice_id)
    supplier = Supplier.query.first()
    clients = Client.query.order_by(Client.name).all()
    
    if request.method == 'POST':
        # Aktualizujeme základné údaje
        invoice.client_id = int(request.form['client_id'])
        invoice.issue_date = date.fromisoformat(request.form['issue_date'])
        invoice.delivery_date = date.fromisoformat(request.form['delivery_date'])
        invoice.due_date = date.fromisoformat(request.form['due_date'])
        invoice.payment_method = request.form['payment_method']
        invoice.vat_rate = float(request.form.get('vat_rate', 0))
        invoice.note = request.form.get('note', '')
        invoice.internal_note = request.form.get('internal_note', '')
        
        # Vymažeme staré položky
        for item in invoice.items:
            db.session.delete(item)
        
        # Pridáme nové položky
        descriptions = request.form.getlist('item_description[]')
        item_notes = request.form.getlist('item_note[]')
        quantities = request.form.getlist('item_quantity[]')
        units = request.form.getlist('item_unit[]')
        unit_prices = request.form.getlist('item_unit_price[]')
        cost_prices = request.form.getlist('item_cost_price[]')
        
        for i, desc in enumerate(descriptions):
            if desc.strip():
                item = InvoiceItem(
                    invoice_id=invoice.id,
                    description=desc,
                    item_note=item_notes[i] if i < len(item_notes) else '',
                    quantity=float(quantities[i]) if quantities[i] else 1,
                    unit=units[i] if units[i] else 'ks',
                    unit_price=float(unit_prices[i]) if unit_prices[i] else 0,
                    cost_price=float(cost_prices[i]) if i < len(cost_prices) and cost_prices[i] else 0,
                    position=i
                )
                item.calculate_total()
                db.session.add(item)
        
        db.session.flush()
        invoice.calculate_totals()
        
        ActivityLog.log(
            ActivityLog.ACTION_INVOICE_EDITED,
            f'Faktúra {invoice.invoice_number} upravená',
            invoice_id=invoice.id,
            client_id=invoice.client_id,
            extra_data={'total': invoice.total}
        )
        
        db.session.commit()
        flash(f'Faktúra {invoice.invoice_number} bola aktualizovaná.', 'success')
        return redirect(url_for('invoice_detail', invoice_id=invoice.id))
    
    return render_template('invoice_form.html',
        invoice=invoice,
        supplier=supplier,
        clients=clients,
        today=invoice.issue_date,
        default_due_date=invoice.due_date
    )


@app.route('/invoices/<int:invoice_id>/clone', methods=['POST'])
def invoice_clone(invoice_id):
    """Klonovanie faktúry - vytvorí novú faktúru s rovnakými údajmi"""
    original = Invoice.query.get_or_404(invoice_id)
    supplier = Supplier.query.first()
    
    # Generujeme nové číslo faktúry
    invoice_number = supplier.get_next_invoice_number()
    today = date.today()
    
    # Vytvoríme novú faktúru
    new_invoice = Invoice(
        invoice_number=invoice_number,
        variable_symbol=invoice_number.replace('FV', '').replace('/', ''),
        supplier_id=supplier.id,
        client_id=original.client_id,
        issue_date=today,
        delivery_date=today,
        due_date=today + timedelta(days=14),
        payment_method=original.payment_method,
        vat_rate=original.vat_rate,
        note=original.note,
        status=Invoice.STATUS_ISSUED
    )
    
    db.session.add(new_invoice)
    db.session.flush()
    
    # Skopírujeme položky
    for orig_item in original.items:
        new_item = InvoiceItem(
            invoice_id=new_invoice.id,
            description=orig_item.description,
            item_note=orig_item.item_note,
            quantity=orig_item.quantity,
            unit=orig_item.unit,
            unit_price=orig_item.unit_price,
            cost_price=orig_item.cost_price,
            position=orig_item.position
        )
        new_item.calculate_total()
        db.session.add(new_item)
    
    db.session.flush()
    new_invoice.calculate_totals()
    
    ActivityLog.log(
        ActivityLog.ACTION_INVOICE_CREATED,
        f'Faktúra {new_invoice.invoice_number} vytvorena klonovaním z {original.invoice_number}',
        invoice_id=new_invoice.id,
        client_id=new_invoice.client_id,
        extra_data={'cloned_from': original.invoice_number}
    )
    
    db.session.commit()
    flash(f'Faktúra {new_invoice.invoice_number} bola vytvorená klonovaním.', 'success')
    return redirect(url_for('invoice_edit', invoice_id=new_invoice.id))


@app.route('/invoices/<int:invoice_id>/internal-note', methods=['POST'])
def invoice_internal_note(invoice_id):
    """Aktualizovať internú poznámku faktúry"""
    invoice = Invoice.query.get_or_404(invoice_id)
    invoice.internal_note = request.form.get('internal_note', '')
    db.session.commit()
    flash('Interná poznámka bola uložená.', 'success')
    return redirect(url_for('invoice_detail', invoice_id=invoice.id))


@app.route('/invoices/export/csv')
def invoices_export_csv():
    """Export faktúr do CSV"""
    invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    
    # Hlavička
    writer.writerow([
        'Číslo faktúry', 'Varia. symbol', 'Klient', 'IČO klienta',
        'Dátum vystavenia', 'Dátum splatnosti', 'Dátum úhrady',
        'Medzisúčet', 'DPH', 'Celkom', 'Stav', 'Forma úhrady'
    ])
    
    # Dáta
    for inv in invoices:
        writer.writerow([
            inv.invoice_number,
            inv.variable_symbol,
            inv.client.name,
            inv.client.ico or '',
            inv.issue_date.strftime('%d.%m.%Y'),
            inv.due_date.strftime('%d.%m.%Y'),
            inv.paid_date.strftime('%d.%m.%Y') if inv.paid_date else '',
            f"{inv.subtotal:.2f}".replace('.', ','),
            f"{inv.vat_amount:.2f}".replace('.', ','),
            f"{inv.total:.2f}".replace('.', ','),
            get_status_label(inv.status),
            get_payment_method_label(inv.payment_method)
        ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=faktury_export_{date.today().strftime("%Y%m%d")}.csv',
            'Content-Type': 'text/csv; charset=utf-8'
        }
    )


# ==============================================================================
# NASTAVENIA DODÁVATEĽA
# ==============================================================================

@app.route('/settings', methods=['GET', 'POST'])
def supplier_settings():
    """Nastavenia údajov dodávateľa"""
    supplier = Supplier.query.first()
    
    if request.method == 'POST':
        if supplier:
            # Aktualizácia
            supplier.name = request.form['name']
            supplier.street = request.form['street']
            supplier.city = request.form['city']
            supplier.zip_code = request.form['zip_code']
            supplier.country = request.form.get('country', 'Slovenská republika')
            supplier.ico = request.form['ico']
            supplier.dic = request.form.get('dic', '')
            supplier.ic_dph = request.form.get('ic_dph', '')
            supplier.is_vat_payer = 'is_vat_payer' in request.form
            supplier.bank_name = request.form.get('bank_name', '')
            supplier.iban = request.form.get('iban', '')
            supplier.swift = request.form.get('swift', '')
            supplier.email = request.form.get('email', '')
            supplier.phone = request.form.get('phone', '')
            supplier.web = request.form.get('web', '')
            supplier.invoice_prefix = request.form.get('invoice_prefix', '')
        else:
            # Vytvorenie nového
            supplier = Supplier(
                name=request.form['name'],
                street=request.form['street'],
                city=request.form['city'],
                zip_code=request.form['zip_code'],
                country=request.form.get('country', 'Slovenská republika'),
                ico=request.form['ico'],
                dic=request.form.get('dic', ''),
                ic_dph=request.form.get('ic_dph', ''),
                is_vat_payer='is_vat_payer' in request.form,
                bank_name=request.form.get('bank_name', ''),
                iban=request.form.get('iban', ''),
                swift=request.form.get('swift', ''),
                email=request.form.get('email', ''),
                phone=request.form.get('phone', ''),
                web=request.form.get('web', ''),
                invoice_prefix=request.form.get('invoice_prefix', '')
            )
            db.session.add(supplier)
        
        db.session.commit()
        flash('Nastavenia boli uložené.', 'success')
        return redirect(url_for('supplier_settings'))
    
    return render_template('settings.html', supplier=supplier)


# ==============================================================================
# API ENDPOINTS
# ==============================================================================

@app.route('/api/clients/create', methods=['POST'])
def api_client_create():
    """
    API endpoint pre vytvorenie nového klienta cez AJAX.
    Používa sa z formulára faktúry.
    """
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('street') or not data.get('city') or not data.get('zip_code'):
            return jsonify({'success': False, 'error': 'Vyplňte všetky povinné polia'}), 400
        
        client = Client(
            name=data.get('name', ''),
            contact_person=data.get('contact_person', ''),
            street=data.get('street', ''),
            city=data.get('city', ''),
            zip_code=data.get('zip_code', ''),
            country=data.get('country', 'Slovenská republika'),
            ico=data.get('ico', ''),
            dic=data.get('dic', ''),
            ic_dph=data.get('ic_dph', ''),
            email=data.get('email', ''),
            phone=data.get('phone', '')
        )
        
        db.session.add(client)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'client': {
                'id': client.id,
                'name': client.name,
                'city': client.city
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/rpo/lookup/<ico>')
def rpo_lookup(ico):
    """
    API endpoint pre vyhľadanie firmy v RPO podľa IČO.
    Používa sa cez AJAX z formulárov.
    """
    if not ico or len(ico.strip()) < 3:
        return jsonify({'error': 'IČO musí mať aspoň 3 znaky'}), 400
    
    result = lookup_company(ico)
    
    if result:
        return jsonify({
            'success': True,
            'data': result
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Firma s týmto IČO nebola nájdená'
        }), 404


@app.route('/api/upload-stamp', methods=['POST'])
def upload_stamp():
    """Nahrávanie pečiatky alebo podpisu"""
    supplier = Supplier.query.first()
    if not supplier:
        return jsonify({'success': False, 'error': 'Najprv nastavťe údaje dodávateľa'}), 400
    
    image_type = request.form.get('type', 'stamp')  # 'stamp' alebo 'signature'
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'Nebol nahraný žiaden súbor'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Nebol vybraný súbor'}), 400
    
    # Skontrolujeme typ súboru
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    
    if ext not in allowed_extensions:
        return jsonify({'success': False, 'error': 'Povolené sú len obrázky (PNG, JPG, GIF)'}), 400
    
    # Konvertujeme na Base64
    file_data = file.read()
    b64_data = base64.b64encode(file_data).decode('utf-8')
    mime_type = f'image/{ext}' if ext != 'jpg' else 'image/jpeg'
    data_uri = f'data:{mime_type};base64,{b64_data}'
    
    # Uložíme
    if image_type == 'signature':
        supplier.signature_image = data_uri
    else:
        supplier.stamp_image = data_uri
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'image_url': data_uri,
        'message': 'Obrázok bol nahraný'
    })


@app.route('/api/remove-stamp', methods=['POST'])
def remove_stamp():
    """Odstránenie pečiatky alebo podpisu"""
    supplier = Supplier.query.first()
    if not supplier:
        return jsonify({'success': False, 'error': 'Dodávateľ neexistuje'}), 400
    
    image_type = request.json.get('type', 'stamp')
    
    if image_type == 'signature':
        supplier.signature_image = None
    else:
        supplier.stamp_image = None
    
    db.session.commit()
    
    return jsonify({'success': True})


# ==============================================================================
# INICIALIZÁCIA DATABÁZY
# ==============================================================================

# Vytvoríme databázu pri importe (pre Gunicorn)
with app.app_context():
    db.create_all()


# ==============================================================================
# SPUSTENIE APLIKÁCIE
# ==============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
