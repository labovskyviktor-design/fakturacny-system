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
        
        # Register fonts immediately
        self.font_reg, self.font_bold = register_fonts()
        
        # Styles
        styles = getSampleStyleSheet()
        self.style_normal = ParagraphStyle(
            'SlovakNormal', 
            parent=styles['Normal'],
            fontName=self.font_reg,
            fontSize=9,
            textColor=TEXT_COLOR,
            leading=12
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
            fontSize=24,
            textColor=PRIMARY_COLOR,
            spaceAfter=20
        )
        
    def _create_header(self):
        """Header with Title and Supplier Quick Info"""
        # Right side: Supplier partial info
        supplier_text = f"""
        <b>{self.invoice.supplier.name}</b><br/>
        {self.invoice.supplier.street}<br/>
        {self.invoice.supplier.zip_code} {self.invoice.supplier.city}
        """
        
        data = [
            [Paragraph("FAKTÚRA", self.style_title), 
             Paragraph(supplier_text, ParagraphStyle('HeaderRight', parent=self.style_normal, alignment=TA_RIGHT))]
        ]
        
        t = Table(data, colWidths=[10*cm, 9*cm])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LINEBELOW', (0,0), (-1,-1), 2, PRIMARY_COLOR),
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ]))
        return t

    def _create_info_grid(self):
        """Supplier and Client Boxes"""
        # Function to build address paragraph
        def build_addr(obj, title):
            lines = [f"<b>{title}</b>", f"<font size=12 color={PRIMARY_COLOR}>{obj.name}</font>"]
            lines.append(f"{obj.street}")
            lines.append(f"{obj.zip_code} {obj.city}")
            lines.append(f"{obj.country}")
            lines.append(f"<br/>") # Spacer
            if obj.ico: lines.append(f"<b>IČO:</b> {obj.ico}")
            if obj.dic: lines.append(f"<b>DIČ:</b> {obj.dic}")
            if hasattr(obj, 'ic_dph') and obj.ic_dph: lines.append(f"<b>IČ DPH:</b> {obj.ic_dph}")
            return Paragraph("<br/>".join(lines), self.style_normal)

        supplier_p = build_addr(self.invoice.supplier, "DODÁVATEĽ")
        client_p = build_addr(self.invoice.client, "ODBERATEĽ")
        
        data = [[supplier_p, client_p]]
        t = Table(data, colWidths=[9.5*cm, 9.5*cm])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('grid', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('BACKGROUND', (0,0), (0,0), colors.HexColor('#f8fafc')), # Light gray background for supplier
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ]))
        return t

    def _create_meta_table(self):
        """Dates and Numbers"""
        data = [
            [
                f"Variabilný symbol:\n<b>{self.invoice.variable_symbol}</b>",
                f"Dátum vystavenia:\n<b>{format_date_sk(self.invoice.issue_date)}</b>"
            ],
            [
                f"Forma úhrady:\n<b>{'Bankový prevod' if self.invoice.payment_method=='prevod' else 'Hotovosť'}</b>",
                f"Dátum dodania:\n<b>{format_date_sk(self.invoice.delivery_date)}</b>"
            ],
            [
                f"Mena:\n<b>EUR</b>",
                f"Dátum splatnosti:\n<font color='red'><b>{format_date_sk(self.invoice.due_date)}</b></font>"
            ],
            [  # Add Invoice Number here neatly
               f"Číslo faktúry:\n<b>{self.invoice.invoice_number}</b>",
               ""
            ]

        ]
        
        # Convert strings to Paragraphs
        p_data = []
        for row in data:
            p_row = []
            for cell in row:
                if cell:
                    p_row.append(Paragraph(cell.replace('\n', '<br/>'), self.style_normal))
                else:
                    p_row.append('')
            p_data.append(p_row)
            
        t = Table(p_data, colWidths=[9.5*cm, 9.5*cm])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    def _create_items_table(self):
        """Line items"""
        headers = ["Popis položky", "Množstvo", "Jedn.", "Cena/j.", "Spolu"]
        data = [headers]
        
        for item in self.invoice.items:
            desc = item.description
            if item.item_note:
                desc += f"<br/><font size=8 color='#64748b'>{item.item_note}</font>"
            
            row = [
                Paragraph(desc, self.style_normal),
                f"{item.quantity}",
                item.unit,
                format_currency(item.unit_price),
                format_currency(item.total)
            ]
            data.append(row)
            
        t = Table(data, colWidths=[8*cm, 2.5*cm, 2*cm, 3*cm, 3.5*cm])
        
        # Styles
        style = [
            ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), self.font_bold),
            ('ALIGN', (0,0), (-1,0), 'LEFT'),
            ('ALIGN', (1,0), (-1,-1), 'RIGHT'), # Numbers right aligned
            ('FONTNAME', (0,1), (-1,-1), self.font_reg),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (0,-1), 10), # Padding for description
        ]
        t.setStyle(TableStyle(style))
        return t
        
    def _create_totals(self):
        """Totals section"""
        data = []
        data.append(["Základ pre DPH:", format_currency(self.invoice.subtotal)])
        if self.invoice.vat_rate > 0:
            data.append([f"DPH ({int(self.invoice.vat_rate)}%):", format_currency(self.invoice.vat_amount)])
        
        # Total
        total_p = Paragraph(f"<b>Celkom k úhrade:</b>", ParagraphStyle('TotalLabel', parent=self.style_normal, fontSize=12))
        total_val = Paragraph(f"<b>{format_currency(self.invoice.total)}</b>", ParagraphStyle('TotalVal', parent=self.style_normal, fontSize=14, textColor=PRIMARY_COLOR, alignment=TA_RIGHT))
        
        data.append([total_p, total_val])
        
        t = Table(data, colWidths=[14*cm, 5*cm])
        t.setStyle(TableStyle([
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('LINEABOVE', (0,-1), (-1,-1), 1, PRIMARY_COLOR),
            ('TOPPADDING', (0,-1), (-1,-1), 10),
            ('FONTNAME', (0,0), (-1,-1), self.font_reg),
        ]))
        return t

    def _create_qr_and_bank(self):
        """Bank details and QR code"""
        if self.invoice.payment_method != 'prevod':
            return Spacer(1, 1)

        # Bank info text
        bank_lines = [
            f"<b>BANKOVÉ SPOJENIE</b>",
            f"IBAN: <font color={PRIMARY_COLOR} size=11><b>{self.invoice.supplier.iban}</b></font>"
        ]
        if self.invoice.supplier.bank_name:
            bank_lines.append(f"Banka: {self.invoice.supplier.bank_name}")
            
        bank_p = Paragraph("<br/>".join(bank_lines), self.style_normal)
        
        # QR Code
        qr_img = None
        if self.qr_code_base64:
            try:
                # Remove header if present
                img_data = self.qr_code_base64.split(',')[1] if ',' in self.qr_code_base64 else self.qr_code_base64
                img_bytes = base64.b64decode(img_data)
                qr_stream = io.BytesIO(img_bytes)
                qr_img = PlatypusImage(qr_stream, width=3.5*cm, height=3.5*cm)
            except Exception as e:
                print(f"QR Error: {e}")

        # Label for QR
        qr_label = Paragraph("PAY by square", ParagraphStyle('Small', parent=self.style_normal, fontSize=7, alignment=TA_CENTER))

        # Layout: Bank Info | QR Code
        if qr_img:
            data = [[bank_p, [qr_img, qr_label]]]
            col_widths = [14*cm, 5*cm]
        else:
            data = [[bank_p, ""]]
            col_widths = [14*cm, 5*cm]

        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (1,0), (1,-1), 'CENTER'),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('LEFTPADDING', (0,0), (-1,-1), 15),
            ('TOPPADDING', (0,0), (-1,-1), 15),
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ('ROUNDEDCORNERS', [8, 8, 8, 8]), # Note: ReportLab table rounded corners isn't direct, but we can fake background
        ]))
        return t

    def footer(self, canvas, doc):
        """Fixed footer"""
        canvas.saveState()
        canvas.setFont(self.font_reg, 8)
        canvas.setFillColor(colors.gray)
        
        # Center text
        text = f"Generované systémom FakturaSK | v3.0 Platypus | Strana {doc.page}"
        canvas.drawCentredString(A4[0]/2, 10*mm, text)
        
        # Font usage debug
        canvas.setFillColor(colors.blue)
        canvas.drawString(10*mm, A4[1]-10*mm, f"FONT: {self.font_reg} (Arial)")
        
        canvas.restoreState()

    def generate(self):
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        story.append(self._create_header())
        story.append(Spacer(1, 10*mm))
        
        story.append(self._create_info_grid())
        story.append(Spacer(1, 5*mm))
        
        story.append(self._create_meta_table())
        story.append(Spacer(1, 10*mm))
        
        story.append(self._create_items_table())
        story.append(Spacer(1, 10*mm))
        
        story.append(self._create_totals())
        story.append(Spacer(1, 10*mm))
        
        from utils import suma_slovom
        slovom = suma_slovom(self.invoice.total)
        story.append(Paragraph(f"<b>Suma slovom:</b> {slovom}", self.style_normal))
        story.append(Spacer(1, 10*mm))
        
        story.append(self._create_qr_and_bank())
        
        # Build
        doc.build(story, onFirstPage=self.footer)
        
        return self.buffer.getvalue()


def generate_invoice_pdf_reportlab(invoice, qr_code_base64=None):
    """Wrapper function to match existing interface"""
    pdf = InvoicePDF(invoice, qr_code_base64)
    return pdf.generate()
