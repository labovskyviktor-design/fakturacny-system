"""
ReportLab PDF Generator for Invoices

Pure Python PDF generation using ReportLab - no system dependencies required.
This module generates professional Slovak invoices in A4 portrait format.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import io


# Slovak month names
SLOVAK_MONTHS = [
    '', 'januára', 'februára', 'marca', 'apríla', 'mája', 'júna',
    'júla', 'augusta', 'septembra', 'októbra', 'novembra', 'decembra'
]


def format_date_slovak(date_obj):
    """Format date in Slovak format: DD. mesiaca YYYY"""
    if not date_obj:
        return ''
    return f"{date_obj.day}. {SLOVAK_MONTHS[date_obj.month]} {date_obj.year}"


def generate_invoice_pdf_reportlab(invoice, qr_code_base64=None):
    """
    Generate PDF invoice using ReportLab.
    
    Args:
        invoice: Invoice model object
        qr_code_base64: Optional base64 encoded QR code image
        
    Returns:
        bytes: PDF file content
    """
    buffer = io.BytesIO()
    
    # Create canvas
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Define colors
    primary_blue = HexColor('#1e40af')
    light_gray = HexColor('#f8fafc')
    border_gray = HexColor('#e2e8f0')
    text_gray = HexColor('#64748b')
    dark_text = HexColor('#1e293b')
    
    # Margins
    left_margin = 1.5 * cm
    right_margin = width - 1.5 * cm
    top_margin = height - 1.5 * cm
    
    y_position = top_margin
    
    # === HEADER ===
    c.setStrokeColor(primary_blue)
    c.setLineWidth(2)
    c.line(left_margin, y_position - 15, right_margin, y_position - 15)
    
    # Title
    c.setFillColor(primary_blue)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(left_margin, y_position - 10, "FAKTÚRA")
    
    # Invoice number
    c.setFillColor(text_gray)
    c.setFont("Helvetica", 12)
    c.drawString(left_margin, y_position - 30, f"číslo {invoice.invoice_number}")
    
    # Supplier info (right side)
    c.setFillColor(text_gray)
    c.setFont("Helvetica", 9)
    supplier_x = right_margin - 200
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(dark_text)
    c.drawRightString(right_margin, y_position - 10, invoice.supplier.name)
    
    c.setFont("Helvetica", 9)
    c.setFillColor(text_gray)
    c.drawRightString(right_margin, y_position - 25, invoice.supplier.street)
    c.drawRightString(right_margin, y_position - 38, 
                      f"{invoice.supplier.zip_code} {invoice.supplier.city}, {invoice.supplier.country}")
    
    y_position -= 70
    
    # === SUPPLIER AND CLIENT BOXES ===
    box_height = 130
    box_width = (right_margin - left_margin - 15) / 2
    
    # Supplier box
    c.setFillColor(light_gray)
    c.setStrokeColor(border_gray)
    c.roundRect(left_margin, y_position - box_height, box_width, box_height, 8, fill=1)
    
    c.setFillColor(text_gray)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(left_margin + 15, y_position - 20, "DODÁVATEĽ")
    
    c.setFillColor(primary_blue)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin + 15, y_position - 38, invoice.supplier.name)
    
    c.setFillColor(dark_text)
    c.setFont("Helvetica", 9.5)
    y = y_position - 53
    c.drawString(left_margin + 15, y, invoice.supplier.street)
    y -= 13
    c.drawString(left_margin + 15, y, f"{invoice.supplier.zip_code} {invoice.supplier.city}")
    y -= 13
    c.drawString(left_margin + 15, y, invoice.supplier.country)
    y -= 18
    
    if invoice.supplier.ico:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(left_margin + 15, y, "IČO: ")
        c.setFont("Helvetica", 9)
        c.drawString(left_margin + 40, y, invoice.supplier.ico)
        y -= 11
    
    if invoice.supplier.dic:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(left_margin + 15, y, "DIČ: ")
        c.setFont("Helvetica", 9)
        c.drawString(left_margin + 40, y, invoice.supplier.dic)
        y -= 11
    
    if invoice.supplier.ic_dph:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(left_margin + 15, y, "IČ DPH: ")
        c.setFont("Helvetica", 9)
        c.drawString(left_margin + 55, y, invoice.supplier.ic_dph)
    
    # Client box
    client_x = left_margin + box_width + 15
    c.setFillColor(light_gray)
    c.setStrokeColor(border_gray)
    c.roundRect(client_x, y_position - box_height, box_width, box_height, 8, fill=1)
    
    c.setFillColor(text_gray)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(client_x + 15, y_position - 20, "ODBERATEĽ")
    
    c.setFillColor(primary_blue)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(client_x + 15, y_position - 38, invoice.client.name)
    
    c.setFillColor(dark_text)
    c.setFont("Helvetica", 9.5)
    y = y_position - 53
    if invoice.client.contact_person:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(client_x + 15, y, invoice.client.contact_person)
        y -= 13
        c.setFont("Helvetica", 9.5)
    
    c.drawString(client_x + 15, y, invoice.client.street)
    y -= 13
    c.drawString(client_x + 15, y, f"{invoice.client.zip_code} {invoice.client.city}")
    y -= 13
    c.drawString(client_x + 15, y, invoice.client.country)
    y -= 18
    
    if invoice.client.ico:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(client_x + 15, y, "IČO: ")
        c.setFont("Helvetica", 9)
        c.drawString(client_x + 40, y, invoice.client.ico)
        y -= 11
    
    if invoice.client.dic:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(client_x + 15, y, "DIČ: ")
        c.setFont("Helvetica", 9)
        c.drawString(client_x + 40, y, invoice.client.dic)
        y -= 11
    
    if invoice.client.ic_dph:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(client_x + 15, y, "IČ DPH: ")
        c.setFont("Helvetica", 9)
        c.drawString(client_x + 55, y, invoice.client.ic_dph)
    
    y_position -= box_height + 25
    
    # === INVOICE INFO TABLE ===
    info_data = [
        ['Variabilný symbol:', invoice.variable_symbol, 'Dátum vystavenia:', format_date_slovak(invoice.issue_date)],
        ['Forma úhrady:', 'Bankový prevod' if invoice.payment_method == 'prevod' else 'Hotovosť', 
         'Dátum dodania:', format_date_slovak(invoice.delivery_date)],
        ['Mena:', 'EUR (€)', 'Dátum splatnosti:', format_date_slovak(invoice.due_date)]
    ]
    
    info_table = Table(info_data, colWidths=[90, 140, 90, 140])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), white),
        ('TEXTCOLOR', (0, 0), (0, -1), text_gray),
        ('TEXTCOLOR', (2, 0), (2, -1), text_gray),
        ('TEXTCOLOR', (1, 0), (1, -1), dark_text),
        ('TEXTCOLOR', (3, 0), (3, -1), dark_text),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTSIZE', (1, 0), (1, -1), 10),
        ('FONTSIZE', (3, 0), (3, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, border_gray),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    info_table.wrapOn(c, width, height)
    info_table.drawOn(c, left_margin, y_position - 65)
    
    y_position -= 90
    
    # === ITEMS TABLE ===
    items_data = [['Popis položky', 'Množ.', 'Jedn.', 'Cena/j.', 'Suma celkom']]
    
    for item in invoice.items:
        desc = item.description
        if item.item_note:
            desc += f"\n{item.item_note}"
        
        items_data.append([
            desc,
            str(item.quantity),
            item.unit,
            f"{item.unit_price:.2f} €",
            f"{item.total:.2f} €"
        ])
    
    items_table = Table(items_data, colWidths=[220, 50, 50, 80, 100])
    items_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), primary_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('ALIGN', (3, 0), (-1, 0), 'RIGHT'),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9.5),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        
        # Borders
        ('GRID', (0, 0), (-1, -1), 1, border_gray),
        ('LINEBELOW', (0, 0), (-1, 0), 2, primary_blue),
        
        # Padding
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    items_table.wrapOn(c, width, height)
    table_height = items_table._height
    items_table.drawOn(c, left_margin, y_position - table_height)
    
    y_position -= table_height + 30
    
    # === TOTALS ===
    totals_x = right_margin - 320
    
    c.setFont("Helvetica", 10)
    c.setFillColor(text_gray)
    c.drawString(totals_x, y_position, "Základ pre DPH:")
    c.setFillColor(dark_text)
    c.drawRightString(right_margin, y_position, f"{invoice.subtotal:.2f} €")
    
    y_position -= 18
    
    if invoice.vat_rate > 0:
        c.setFillColor(text_gray)
        c.drawString(totals_x, y_position, f"DPH ({int(invoice.vat_rate)}%):")
        c.setFillColor(dark_text)
        c.drawRightString(right_margin, y_position, f"{invoice.vat_amount:.2f} €")
        y_position -= 18
    
    # Total line
    c.setStrokeColor(primary_blue)
    c.setLineWidth(2)
    c.line(totals_x, y_position + 10, right_margin, y_position + 10)
    
    y_position -= 15
    
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(primary_blue)
    c.drawString(totals_x, y_position, "Celkom k úhrade:")
    c.drawRightString(right_margin, y_position, f"{invoice.total:.2f} €")
    
    y_position -= 30
    
    # Suma slovom
    from utils import suma_slovom
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(text_gray)
    c.drawString(left_margin, y_position, "Suma slovom: ")
    c.setFont("Helvetica", 9)
    c.setFillColor(dark_text)
    c.drawString(left_margin + 70, y_position, suma_slovom(invoice.total))
    
    y_position -= 30
    
    # === PAYMENT INFO (if bank transfer) ===
    if invoice.payment_method == 'prevod' and invoice.supplier.iban:
        c.setFillColor(light_gray)
        c.setStrokeColor(border_gray)
        c.roundRect(left_margin, y_position - 80, right_margin - left_margin, 80, 8, fill=1)
        
        c.setFillColor(text_gray)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left_margin + 15, y_position - 20, "BANKOVÉ SPOJENIE")
        
        y = y_position - 40
        c.setFont("Helvetica", 9)
        c.setFillColor(dark_text)
        
        if invoice.supplier.bank_name:
            c.setFont("Helvetica-Bold", 9)
            c.drawString(left_margin + 15, y, "Banka: ")
            c.setFont("Helvetica", 9)
            c.drawString(left_margin + 60, y, invoice.supplier.bank_name)
            y -= 15
        
        c.setFont("Helvetica-Bold", 9)
        c.drawString(left_margin + 15, y, "IBAN: ")
        c.setFont("Helvetica", 11)
        c.setFillColor(primary_blue)
        c.drawString(left_margin + 60, y, invoice.supplier.iban)
        c.setFillColor(dark_text)
        
        # QR code placeholder (if provided)
        if qr_code_base64:
            # Note: Would need to decode base64 and draw image
            # For now, just note the position
            pass
        
        y_position -= 100
    
    # === FOOTER ===
    y_position = 80
    
    c.setStrokeColor(border_gray)
    c.line(left_margin, y_position, right_margin, y_position)
    
    c.setFont("Helvetica", 8)
    c.setFillColor(text_gray)
    footer_text = "Nie sme platcami DPH podľa §4 zákona č. 222/2004 Z.z. o DPH." if not invoice.supplier.is_vat_payer else "Platca DPH."
    c.drawCentredString(width / 2, y_position - 15, footer_text)
    c.drawCentredString(width / 2, y_position - 28, "Generované systémom FakturaSK")
    
    # Watermarks for status
    if invoice.status == 'cancelled':
        c.saveState()
        c.translate(width / 2, height / 2)
        c.rotate(45)
        c.setFont("Helvetica-Bold", 100)
        c.setFillColor(HexColor('#dc2626'))
        c.setFillAlpha(0.08)
        c.drawCentredString(0, 0, "STORNO")
        c.restoreState()
    
    if invoice.status == 'paid':
        c.saveState()
        c.translate(width - 100, height - 150)
        c.rotate(-15)
        c.setStrokeColor(HexColor('#22c55e'))
        c.setLineWidth(6)
        c.setFillAlpha(0)
        c.roundRect(-60, -25, 120, 50, 12)
        c.setFillColor(HexColor('#22c55e'))
        c.setFillAlpha(0.7)
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(0, -10, "UHRADENÉ")
        c.restoreState()
    
    # Save PDF
    c.showPage()
    c.save()
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
