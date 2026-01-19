"""
ReportLab PDF Generator - Platypus Engine
Modern, grid-based layout with strict font enforcement.
"""
import io
import os
import base64
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as PlatypusImage
from reportlab.pdfgen import canvas

# === CONFIGURATION ===
PRIMARY_COLOR = colors.HexColor('#1e40af')  # Blue
TEXT_COLOR = colors.HexColor('#1e293b')     # Dark Gray/Slate
BORDER_COLOR = colors.HexColor('#e2e8f0')   # Light Gray

def register_fonts():
    """
    Registers the bundled Arial fonts.
    Raises error if not found (we want to fail fast rather than produce bad output).
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_dir = os.path.join(base_dir, 'fonts')
    
    regular = os.path.join(font_dir, 'Arial.ttf')
    bold = os.path.join(font_dir, 'Arial-Bold.ttf')
    
    # Debug info
    print(f"DEBUG: Registering fonts from {font_dir}")
    
    if not os.path.exists(regular):
        raise FileNotFoundError(f"Missing font: {regular}")
        
    pdfmetrics.registerFont(TTFont('SlovakFont', regular))
    pdfmetrics.registerFont(TTFont('SlovakFont-Bold', bold if os.path.exists(bold) else regular))
    
    return 'SlovakFont', 'SlovakFont-Bold'


def format_currency(value):
    return f"{value:.2f} €"

def format_date_sk(date_obj):
    if not date_obj: return ""
    months = ['', 'januára', 'februára', 'marca', 'apríla', 'mája', 'júna',
              'júla', 'augusta', 'septembra', 'októbra', 'novembra', 'decembra']
    return f"{date_obj.day}. {months[date_obj.month]} {date_obj.year}"


class InvoicePDF:
    def __init__(self, invoice, qr_code_base64=None):
        self.invoice = invoice
        self.qr_code_base64 = qr_code_base64
        self.buffer = io.BytesIO()
        self.font_reg, self.font_bold = register_fonts()
        
        # Modern Color Palette
        self.c_primary = colors.HexColor('#2563eb')    # Bright Blue
        self.c_text = colors.HexColor('#334155')       # Slate 700
        self.c_text_light = colors.HexColor('#64748b') # Slate 500
        self.c_border = colors.HexColor('#cbd5e1')     # Slate 300
        self.c_bg_light = colors.HexColor('#f8fafc')   # Slate 50
        
        # Styles
        styles = getSampleStyleSheet()
        self.style_normal = ParagraphStyle(
            'SlovakNormal', 
            parent=styles['Normal'],
            fontName=self.font_reg,
            fontSize=8.5, # Compact font
            textColor=self.c_text,
            leading=10,
            allowWidows=0,
            allowOrphans=0
        )
        self.style_label = ParagraphStyle(
            'SlovakLabel',
            parent=self.style_normal,
            fontSize=7,
            textColor=self.c_text_light,
            textTransform='uppercase'
        )
        self.style_bold = ParagraphStyle(
            'SlovakBold', 
            parent=self.style_normal,
            fontName=self.font_bold,
        )
        self.style_title = ParagraphStyle(
            'SlovakTitle',
            parent=styles['Heading1'],
            fontName=self.font_bold,
            fontSize=22,
            textColor=self.c_primary,
            spaceAfter=5
        )

    def _create_header(self):
        """Compact Header"""
        supplier_block = [
            Paragraph("DODÁVATEĽ", self.style_label),
            Paragraph(f"<b>{self.invoice.supplier.name}</b>", self.style_normal),
            Paragraph(f"{self.invoice.supplier.street}", self.style_normal),
            Paragraph(f"{self.invoice.supplier.zip_code} {self.invoice.supplier.city}", self.style_normal),
            Paragraph(f"{self.invoice.supplier.country}", self.style_normal),
            Spacer(1, 2),
            Paragraph(f"IČO: {self.invoice.supplier.ico}", self.style_normal) if self.invoice.supplier.ico else "",
            Paragraph(f"DIČ: {self.invoice.supplier.dic}", self.style_normal) if self.invoice.supplier.dic else "",
        ]
        
        client_block = [
            Paragraph("ODBERATEĽ", self.style_label),
            Paragraph(f"<b>{self.invoice.client.name}</b>", self.style_normal),
            Paragraph(f"{self.invoice.client.street}", self.style_normal),
            Paragraph(f"{self.invoice.client.zip_code} {self.invoice.client.city}", self.style_normal),
            Paragraph(f"{self.invoice.client.country}", self.style_normal),
            Spacer(1, 2),
            Paragraph(f"IČO: {self.invoice.client.ico}", self.style_normal) if self.invoice.client.ico else "",
            Paragraph(f"DIČ: {self.invoice.client.dic}", self.style_normal) if self.invoice.client.dic else "",
        ]
        
        # Meta info (Dates/Numbers) as a clean list
        meta_data = [
            [Paragraph("Faktúra č.:", self.style_label), Paragraph(f"<b>{self.invoice.invoice_number}</b>", self.style_normal)],
            [Paragraph("Dátum vystavenia:", self.style_label), Paragraph(f"{format_date_sk(self.invoice.issue_date)}", self.style_normal)],
            [Paragraph("Dátum dodania:", self.style_label), Paragraph(f"{format_date_sk(self.invoice.delivery_date)}", self.style_normal)],
            [Paragraph("Dátum splatnosti:", self.style_label), Paragraph(f"<b>{format_date_sk(self.invoice.due_date)}</b>", self.style_normal)],
            [Paragraph("Variabilný symbol:", self.style_label), Paragraph(f"{self.invoice.variable_symbol}", self.style_normal)],
        ]
        
        meta_table = Table(meta_data, colWidths=[3.5*cm, 4*cm])
        meta_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        
        # Main Layout: 3 Columns [Supplier | Client | Meta]
        main_data = [[
            [Paragraph("FAKTÚRA", self.style_title), Spacer(1,5)] + supplier_block,
            client_block,
            meta_table
        ]]
        
        t = Table(main_data, colWidths=[7*cm, 7*cm, 5*cm])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, self.c_border),
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('ROUNDEDCORNERS', [0,0,0,0]),
        ]))
        return t

    def _create_items_table(self):
        """Modern Striped Items Table"""
        headers = ["Popis položky/Služby", "Množstvo", "MJ", "Cena za j.", "Spolu"]
        data = [[Paragraph(h, ParagraphStyle('Header', parent=self.style_label, textColor=colors.white)) for h in headers]]
        
        for i, item in enumerate(self.invoice.items):
            desc = item.description
            if item.item_note:
                desc += f"<br/><font size=7 color='#64748b'>{item.item_note}</font>"
            
            row = [
                Paragraph(desc, self.style_normal),
                f"{item.quantity}",
                item.unit,
                format_currency(item.unit_price),
                format_currency(item.total)
            ]
            data.append(row)
            
        t = Table(data, colWidths=[8.5*cm, 2.5*cm, 1.5*cm, 3*cm, 3.5*cm], repeatRows=1)
        
        # Zebra Striping
        styles = [
            ('BACKGROUND', (0,0), (-1,0), self.c_primary), # Header Bg
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,0), 'LEFT'),
            ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, self.c_bg_light),
        ]
        
        # Add alternating background
        for i in range(1, len(data)):
            if i % 2 == 0:
                styles.append(('BACKGROUND', (0,i), (-1,i), self.c_bg_light))
                
        t.setStyle(TableStyle(styles))
        return t
        
    def _create_footer_section(self):
        """Totals + Payment + QR in one compact block"""
        
        # Totals Table
        totals_data = []
        totals_data.append([Paragraph("Základ DPH:", self.style_normal), format_currency(self.invoice.subtotal)])
        if self.invoice.vat_rate > 0:
             totals_data.append([Paragraph(f"DPH {int(self.invoice.vat_rate)}%:", self.style_normal), format_currency(self.invoice.vat_amount)])
        
        total_p = Paragraph(f"<b>{format_currency(self.invoice.total)}</b>", ParagraphStyle('TotalBig', parent=self.style_bold, fontSize=16, textColor=self.c_primary, alignment=TA_RIGHT))
        totals_data.append([Paragraph("<b>K ÚHRADE SPOLU:</b>", self.style_bold), total_p])
        
        totals_table = Table(totals_data, colWidths=[4*cm, 4*cm])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('LINEABOVE', (0,-1), (-1,-1), 1, self.c_primary),
            ('TOPPADDING', (0,-1), (-1,-1), 8),
        ]))
        
        # Payment Info
        pay_lines = [Paragraph("PLATOBNÉ ÚDAJE", self.style_label)]
        if self.invoice.payment_method == 'prevod' and self.invoice.supplier.iban:
            pay_lines.append(Paragraph(f"IBAN: <b>{self.invoice.supplier.iban}</b>", self.style_normal))
            if self.invoice.supplier.bank_name:
                pay_lines.append(Paragraph(f"Banka: {self.invoice.supplier.bank_name}", self.style_normal))
        else:
            pay_lines.append(Paragraph(f"Forma úhrady: {self.invoice.payment_method}", self.style_normal))
            
        pay_col = [pay_lines] # Column 1 content
        
        # QR Code
        qr_flowable = Spacer(1,1)
        if self.qr_code_base64:
             try:
                img_data = self.qr_code_base64.split(',')[1] if ',' in self.qr_code_base64 else self.qr_code_base64
                img_bytes = base64.b64decode(img_data)
                qr_img = PlatypusImage(io.BytesIO(img_bytes), width=3*cm, height=3*cm)
                qr_flowable = qr_img
             except: pass
             
        # Combined Footer Table: [ Payment Info | QR Code | Totals ]
        foot_data = [[
            pay_col,
            [qr_flowable, Paragraph("PAY by square", self.style_label)] if self.qr_code_base64 else "",
            totals_table
        ]]
        
        t = Table(foot_data, colWidths=[7*cm, 4*cm, 8*cm])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (2,0), (2,-1), 'RIGHT'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    def footer_canvas(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(self.font_reg, 7)
        canvas.setFillColor(self.c_text_light)
        canvas.drawCentredString(A4[0]/2, 10*mm, "Faktúra slúži zároveň ako dodací list. • Vygenerované cez FakturaSK")
        canvas.restoreState()

    def generate(self):
        # Minimized margins for max space
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1*cm,
            bottomMargin=1.5*cm
        )
        
        story = []
        story.append(self._create_header())
        story.append(Spacer(1, 0.8*cm))
        story.append(self._create_items_table())
        story.append(Spacer(1, 1*cm))
        story.append(self._create_footer_section())
        
        doc.build(story, onFirstPage=self.footer_canvas)
        return self.buffer.getvalue()


def generate_invoice_pdf_reportlab(invoice, qr_code_base64=None):
    """Wrapper function to match existing interface"""
    pdf = InvoicePDF(invoice, qr_code_base64)
    return pdf.generate()
