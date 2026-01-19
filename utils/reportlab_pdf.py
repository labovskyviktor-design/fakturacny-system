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

    def _create_header_and_details_layout(self):
        """
        Asymmetric Layout based on Reference Image:
        Left Column (50%): Supplier Info -> Dotted Line -> Bank Info
        Right Column (50%): Title (Big) -> Dotted Line -> Client Info -> Dotted Line -> Dates
        """
        
        # --- LEFT COLUMN CONTENT ---
        # 1. Supplier
        supplier_lines = [
            Paragraph("DODÁVATEĽ:", self.style_label),
            Paragraph(f"<b>{self.invoice.supplier.name}</b>", self.style_normal),
            Paragraph(f"{self.invoice.supplier.street}", self.style_normal),
            Paragraph(f"{self.invoice.supplier.zip_code} {self.invoice.supplier.city}", self.style_normal),
            Paragraph(f"{self.invoice.supplier.country}", self.style_normal),
            Spacer(1, 4),
        ]
        if self.invoice.supplier.ico: supplier_lines.append(Paragraph(f"IČO: {self.invoice.supplier.ico}", self.style_normal))
        if self.invoice.supplier.dic: supplier_lines.append(Paragraph(f"DIČ: {self.invoice.supplier.dic}", self.style_normal))
        if self.invoice.supplier.ic_dph: supplier_lines.append(Paragraph(f"IČ DPH: {self.invoice.supplier.ic_dph}", self.style_normal))

        # 2. Bank Info (Left, below supplier)
        bank_lines = [Spacer(1, 10), Paragraph("BANKOVÉ SPOJENIE:", self.style_label)]
        if self.invoice.supplier.bank_name:
             bank_lines.append(Paragraph(f"{self.invoice.supplier.bank_name}", self.style_normal))
        
        # IBAN/SWIFT formatting
        iban_text = f"<b>{self.invoice.supplier.iban}</b>"
        bank_lines.append(Paragraph(iban_text, self.style_normal))
        
        # Variable Symbol
        bank_lines.append(Spacer(1, 5))
        bank_lines.append(Paragraph(f"Variabilný symbol: <b>{self.invoice.variable_symbol}</b>", self.style_normal))
        
        # Combine Left
        left_content = supplier_lines + [Spacer(1, 15)] + bank_lines
        
        
        # --- RIGHT COLUMN CONTENT ---
        # 1. Title (Big, Top Right)
        title_content = [
             Paragraph(f"Faktúra &nbsp; {self.invoice.invoice_number}", self.style_title),
             Spacer(1, 15)
        ]
        
        # 2. Client (Mid Right)
        client_lines = [
            Paragraph("ODBERATEĽ:", self.style_label),
            Paragraph(f"<b>{self.invoice.client.name}</b>", self.style_normal_big),
            Paragraph(f"{self.invoice.client.street}", self.style_normal),
            Paragraph(f"{self.invoice.client.zip_code} {self.invoice.client.city}", self.style_normal),
            Paragraph(f"{self.invoice.client.country}", self.style_normal),
        ]
        if self.invoice.client.ico: client_lines.append(Paragraph(f"IČO: {self.invoice.client.ico}", self.style_normal))
        if self.invoice.client.dic: client_lines.append(Paragraph(f"DIČ: {self.invoice.client.dic}", self.style_normal))
        if self.invoice.client.ic_dph: client_lines.append(Paragraph(f"IČ DPH: {self.invoice.client.ic_dph}", self.style_normal))

        # 3. Dates (Lower Right)
        dates_data = [
            [Paragraph("Dátum vystavenia:", self.style_normal), Paragraph(format_date_sk(self.invoice.issue_date), self.style_right)],
            [Paragraph("Dátum dodania:", self.style_normal), Paragraph(format_date_sk(self.invoice.delivery_date), self.style_right)],
            [Paragraph("Dátum splatnosti:", self.style_normal), Paragraph(f"<b>{format_date_sk(self.invoice.due_date)}</b>", self.style_right)],
        ]
        dates_table = Table(dates_data, colWidths=[3.5*cm, 4*cm])
        dates_table.setStyle(TableStyle([
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))

        right_content = title_content + client_lines + [Spacer(1, 15)] + [dates_table]

        # --- GRID ASSEMBLY ---
        # We use a 2-column invisible table.
        # To simulate the "dashed lines", we can apply them to specific cells or draw them manually.
        # ReportLab TableStyle supports 'GRID' but dashed is harder in TableStyle (needs dashArray).
        # We will use 'LINEBELOW' with dashArray if possible, or just standard lines.
        # Reference image uses DOTTED lines. 
        
        main_data = [[left_content, right_content]]
        t = Table(main_data, colWidths=[9.5*cm, 9.5*cm])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (0,0), 0),    # Left col padding
            ('RIGHTPADDING', (0,0), (0,0), 10),
            ('LEFTPADDING', (1,0), (1,0), 10),   # Right col padding
            ('RIGHTPADDING', (1,0), (1,0), 0),
            # Vertical Separator (Solid for now to prevent crash)
            ('LINEBEFORE', (1,0), (1,-1), 0.5, self.c_border), # Middle line
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
        """Reference Style Footer: QR Left, Totals Right (Big), Signature Middle"""
        
        # --- LEFT: Note + QR ---
        note_text = "Nie sme platcami DPH."
        if self.invoice.supplier.is_vat_payer: note_text = "Sme platci DPH."
        
        left_elements = [
            Paragraph(f"Poznámka: {note_text}", self.style_normal_small),
            Spacer(1, 5)
        ]
        
        if self.qr_code_base64:
             try:
                img_data = self.qr_code_base64.split(',')[1] if ',' in self.qr_code_base64 else self.qr_code_base64
                img_bytes = base64.b64decode(img_data)
                # Ensure valid image
                qr_img = PlatypusImage(io.BytesIO(img_bytes), width=3*cm, height=3*cm)
                left_elements.append(qr_img)
                left_elements.append(Paragraph("PAY by square", self.style_label))
             except: pass

        # --- CENTER/RIGHT: Signature & Stamp ---
        sig_elements = []
        # Check for Stamp
        if self.invoice.supplier.stamp_image:
            try:
                s_data = self.invoice.supplier.stamp_image.split(',')[1] if ',' in self.invoice.supplier.stamp_image else self.invoice.supplier.stamp_image
                s_bytes = base64.b64decode(s_data)
                stamp_img = PlatypusImage(io.BytesIO(s_bytes), width=3.5*cm, height=3.5*cm, kind='proportional')
                sig_elements.append(stamp_img)
            except: pass
            
        # Check for Signature (overlay or adjacent?) -> stacked for now
        if self.invoice.supplier.signature_image:
            try:
                sig_data = self.invoice.supplier.signature_image.split(',')[1] if ',' in self.invoice.supplier.signature_image else self.invoice.supplier.signature_image
                sig_bytes = base64.b64decode(sig_data)
                # Signature often wider
                sig_img = PlatypusImage(io.BytesIO(sig_bytes), width=4*cm, height=2*cm, kind='proportional')
                sig_elements.append(sig_img)
            except: pass
            
        if not sig_elements:
            sig_elements.append(Paragraph("Podpis a pečiatka:", self.style_label))


        # --- RIGHT: Totals ---
        total_p = Paragraph(f"{format_currency(self.invoice.total)}", ParagraphStyle('TotalBig', parent=self.style_bold, fontSize=18, textColor=colors.black, alignment=TA_RIGHT))
        
        totals_list = []
        totals_list.append([Paragraph("Základ:", self.style_normal), format_currency(self.invoice.subtotal)])
        if self.invoice.vat_rate > 0:
             totals_list.append([Paragraph(f"DPH {int(self.invoice.vat_rate)}%:", self.style_normal), format_currency(self.invoice.vat_amount)])
        totals_list.append([Paragraph("Celkom:", self.style_bold_big), total_p])

        totals_table = Table(totals_list, colWidths=[3*cm, 4*cm])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LINEABOVE', (0,-1), (-1,-1), 1, self.c_border),
            ('TOPPADDING', (0,-1), (-1,-1), 8),
        ]))
        
        # Assembly: 3 Columns [ QR | Signature/Stamp | Totals ]
        data = [[left_elements, sig_elements, totals_table]]
        t = Table(data, colWidths=[6*cm, 6*cm, 7*cm])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (0,-1), 'LEFT'),   # QR Left
            ('ALIGN', (1,0), (1,-1), 'CENTER'), # Sig Center
            ('ALIGN', (2,0), (2,-1), 'RIGHT'),  # Totals Right
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    def footer_canvas(self, canvas, doc):
        """Fixed footer"""
        canvas.saveState()
        canvas.setFont(self.font_reg, 7)
        canvas.setFillColor(self.c_text_light)
        # Center text
        text = f"Generované systémom FakturaSK | v3.3 Reference | Strana {doc.page}"
        canvas.drawCentredString(A4[0]/2, 10*mm, text)
        canvas.restoreState()

    def generate(self):
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )
        
        # Custom Styles for Reference Look
        self.style_normal_big = ParagraphStyle('NormBig', parent=self.style_normal, fontSize=11, spaceAfter=2)
        self.style_bold_big = ParagraphStyle('BoldBig', parent=self.style_bold, fontSize=14)
        self.style_normal_small = ParagraphStyle('Small', parent=self.style_normal, fontSize=7, textColor=self.c_text_light)
        self.style_right = ParagraphStyle('Right', parent=self.style_normal, alignment=TA_RIGHT)
        
        story = []
        story.append(self._create_header_and_details_layout())
        story.append(Spacer(1, 1*cm))
        
        # Items Table (Full Width)
        story.append(self._create_items_table())
        story.append(Spacer(1, 0.5*cm))
        
        # Horizontal Line
        # story.append(HRFlowable(width="100%", thickness=1, color=self.c_border))
        
        story.append(self._create_footer_section())
        doc.build(story, onFirstPage=self.footer_canvas)
        return self.buffer.getvalue()


def generate_invoice_pdf_reportlab(invoice, qr_code_base64=None):
    """Wrapper function with Error Handling"""
    try:
        pdf = InvoicePDF(invoice, qr_code_base64)
        return pdf.generate()
    except Exception as e:
        # Fallback: Generate a simple PDF with the error message
        import traceback
        error_trace = traceback.format_exc()
        print(f"PDF GENERATION ERROR: {e}")
        print(error_trace)
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.setFont("Helvetica", 10) # Fallback to standard font
        c.setFillColor(colors.red)
        c.drawString(2*cm, A4[1]-3*cm, "CRITICAL ERROR: PDF Generation Failed")
        c.setFillColor(colors.black)
        c.drawString(2*cm, A4[1]-4*cm, f"Error: {str(e)}")
        
        # Print trace lines
        y = A4[1]-5*cm
        for line in error_trace.split('\n')[-10:]: # Last 10 lines
            c.drawString(2*cm, y, line.strip())
            y -= 12
            
        c.save()
        return buffer.getvalue()
