"""
Pomocné funkcie pre fakturačný systém
- Suma slovom v slovenčine
- PAY by square QR kód generátor
"""
import io
import base64
import binascii
import lzma
import struct
import qrcode
from decimal import Decimal


# ==============================================================================
# SUMA SLOVOM V SLOVENČINE
# ==============================================================================

JEDNOTKY = ['', 'jeden', 'dva', 'tri', 'štyri', 'päť', 'šesť', 'sedem', 'osem', 'deväť']
JEDNOTKY_ZENA = ['', 'jedna', 'dve', 'tri', 'štyri', 'päť', 'šesť', 'sedem', 'osem', 'deväť']
TEENS = ['desať', 'jedenásť', 'dvanásť', 'trinásť', 'štrnásť', 'pätnásť', 
         'šestnásť', 'sedemnásť', 'osemnásť', 'devätnásť']
DESIATKY = ['', '', 'dvadsať', 'tridsať', 'štyridsať', 'päťdesiat', 
            'šesťdesiat', 'sedemdesiat', 'osemdesiat', 'deväťdesiat']
STOVKY = ['', 'sto', 'dvesto', 'tristo', 'štyristo', 'päťsto', 
          'šesťsto', 'sedemsto', 'osemsto', 'deväťsto']


def _trojcifrie_slovom(n, zensky_rod=False):
    """Prevedie trojciferné číslo na slová"""
    if n == 0:
        return ''
    
    jednotky = JEDNOTKY_ZENA if zensky_rod else JEDNOTKY
    
    stovky = n // 100
    desiatky = (n % 100) // 10
    jednotky_val = n % 10
    
    result = []
    
    # Stovky
    if stovky > 0:
        result.append(STOVKY[stovky])
    
    # Desiatky a jednotky
    if desiatky == 1:
        result.append(TEENS[jednotky_val])
    else:
        if desiatky > 0:
            result.append(DESIATKY[desiatky])
        if jednotky_val > 0:
            result.append(jednotky[jednotky_val])
    
    return ''.join(result)


def suma_slovom(suma):
    """
    Prevedie sumu na slovenský text
    Napr: 1234.56 -> "tisícdvestotridsaťštyri eur 56 centov"
    """
    if suma == 0:
        return "nula eur"
    
    # Rozdelíme na eurá a centy
    suma = Decimal(str(suma))
    eura = int(suma)
    centy = int((suma - eura) * 100)
    
    result = []
    
    # Eurá
    if eura > 0:
        if eura >= 1000000000:
            miliardy = eura // 1000000000
            eura %= 1000000000
            if miliardy == 1:
                result.append('jednamiliarda')
            elif miliardy in [2, 3, 4]:
                result.append(_trojcifrie_slovom(miliardy, True) + 'miliardy')
            else:
                result.append(_trojcifrie_slovom(miliardy, True) + 'miliárd')
        
        if eura >= 1000000:
            miliony = eura // 1000000
            eura %= 1000000
            if miliony == 1:
                result.append('jedenmilión')
            elif miliony in [2, 3, 4]:
                result.append(_trojcifrie_slovom(miliony) + 'milióny')
            else:
                result.append(_trojcifrie_slovom(miliony) + 'miliónov')
        
        if eura >= 1000:
            tisice = eura // 1000
            eura %= 1000
            if tisice == 1:
                result.append('tisíc')
            elif tisice in [2, 3, 4]:
                result.append(_trojcifrie_slovom(tisice, True) + 'tisíc')
            else:
                result.append(_trojcifrie_slovom(tisice, True) + 'tisíc')
        
        if eura > 0:
            result.append(_trojcifrie_slovom(eura))
        
        # Skloňovanie "euro"
        celkove_eura = int(Decimal(str(suma)))
        if celkove_eura == 1:
            result.append('euro')
        elif celkove_eura in [2, 3, 4]:
            result.append('eurá')
        else:
            result.append('eur')
    
    # Centy
    if centy > 0:
        if eura > 0:
            result.append('')  # medzera
        result.append(_trojcifrie_slovom(centy))
        if centy == 1:
            result.append('cent')
        elif centy in [2, 3, 4]:
            result.append('centy')
        else:
            result.append('centov')
    elif eura == 0:
        result.append('nula eur')
    
    return ' '.join(result).replace('  ', ' ').strip()


def format_currency(amount):
    """Formátuje sumu s medzierami a desatinnou čiarkou"""
    return f"{amount:,.2f}".replace(",", " ").replace(".", ",")


# ==============================================================================
# PAY BY SQUARE - Slovenský bankový QR kód štandard
# ==============================================================================

def generate_pay_by_square(
    amount: float,
    iban: str,
    swift: str = "",
    variable_symbol: str = "",
    constant_symbol: str = "",
    specific_symbol: str = "",
    note: str = "",
    beneficiary_name: str = "",
    due_date: str = ""
) -> str:
    """
    Generuje PAY by square QR kód podľa slovenského štandardu.
    
    Vracia base64 encoded PNG obrázok.
    
    Parametre:
        amount: Suma v EUR
        iban: IBAN účtu príjemcu
        swift: SWIFT/BIC kód (voliteľné)
        variable_symbol: Variabilný symbol
        constant_symbol: Konštantný symbol
        specific_symbol: Špecifický symbol
        note: Poznámka pre príjemcu
        beneficiary_name: Meno príjemcu
        due_date: Dátum splatnosti vo formáte YYYYMMDD
    """
    # Odstránime medzery z IBAN
    iban = iban.replace(" ", "").upper()
    
    # Vytvoríme payment string podľa špecifikácie PAY by square
    # Formát: tabulátorom oddelené polia
    payment_data = _create_payment_string(
        amount=amount,
        currency="EUR",
        iban=iban,
        swift=swift,
        variable_symbol=variable_symbol,
        constant_symbol=constant_symbol,
        specific_symbol=specific_symbol,
        note=note,
        beneficiary_name=beneficiary_name,
        due_date=due_date
    )
    
    # Komprimujeme LZMA
    compressed = _compress_payment_data(payment_data)
    
    # Zakódujeme do base32hex
    encoded = _encode_to_base32hex(compressed)
    
    # Vygenerujeme QR kód
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(encoded)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Konvertujeme na base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def _create_payment_string(
    amount: float,
    currency: str,
    iban: str,
    swift: str,
    variable_symbol: str,
    constant_symbol: str,
    specific_symbol: str,
    note: str,
    beneficiary_name: str,
    due_date: str
) -> str:
    """
    Vytvorí payment string podľa PAY by square špecifikácie verzia 1.1.0
    """
    # Počet platieb (vždy 1)
    num_payments = "1"
    
    # Typ platby: 1 = payment order
    payment_type = "1"
    
    # Formátujeme sumu (bez desatinnej čiarky, v centoch)
    amount_str = f"{amount:.2f}"
    
    # Vytvoríme symboly string
    symbols = f"{variable_symbol}/{specific_symbol}/{constant_symbol}"
    
    # PAY by square data format (verzia 1.1.0):
    # Header: 0000 (verzia)
    # Počet platieb
    # Pre každú platbu:
    #   - typ platby
    #   - suma
    #   - mena
    #   - dátum splatnosti
    #   - symboly
    #   - poznámka
    #   - počet účtov
    #   - IBAN
    #   - SWIFT
    #   - meno príjemcu
    
    # Jednoduchšia implementácia - priamo string
    fields = [
        "",                # Invoice ID (prázdne)
        num_payments,      # Počet platieb
        "1",               # Payment options
        amount_str,        # Suma
        currency,          # Mena
        due_date,          # Dátum splatnosti
        variable_symbol,   # VS
        constant_symbol,   # KS  
        specific_symbol,   # SS
        "",                # Reference
        note,              # Poznámka
        "1",               # Počet účtov
        iban,              # IBAN
        swift,             # SWIFT
        "0",               # Standing order
        "0",               # Direct debit
        beneficiary_name,  # Meno príjemcu
        "",                # Adresa 1
        "",                # Adresa 2
    ]
    
    return "\t".join(fields)


def _compress_payment_data(data: str) -> bytes:
    """
    Komprimuje payment data pomocou LZMA podľa PAY by square štandardu
    """
    # Konvertujeme na bytes
    data_bytes = data.encode('utf-8')
    
    # Pridáme CRC32 checksum (4 bytes, little endian)
    crc = binascii.crc32(data_bytes) & 0xffffffff
    
    # Dáta s CRC
    data_with_crc = data_bytes + struct.pack('<I', crc)
    
    # LZMA kompresia s nastaveniami pre PAY by square
    compressed = lzma.compress(
        data_with_crc,
        format=lzma.FORMAT_RAW,
        filters=[{
            'id': lzma.FILTER_LZMA1,
            'lc': 3,
            'lp': 0,
            'pb': 2,
            'dict_size': 128 * 1024,
        }]
    )
    
    # Pridáme header s dĺžkou originálnych dát (2 bytes, little endian)
    header = struct.pack('<H', len(data_with_crc))
    
    return header + compressed


def _encode_to_base32hex(data: bytes) -> str:
    """
    Zakóduje bytes do base32hex (RFC 4648) s paddingom na 5-bit hranicu
    """
    # Zarovnanie na 5-bit hranicu
    bit_length = len(data) * 8
    padding_bits = (5 - (bit_length % 5)) % 5
    
    # Pridáme padding bity
    if padding_bits > 0:
        data = data + b'\x00' * ((padding_bits + 7) // 8)
    
    # Base32hex alphabet
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUV"
    
    # Konvertujeme na číslo
    num = int.from_bytes(data, 'big')
    
    # Počet znakov
    num_chars = (bit_length + padding_bits) // 5
    
    # Enkódujeme
    result = []
    for _ in range(num_chars):
        result.append(alphabet[num & 0x1F])
        num >>= 5
    
    return ''.join(reversed(result))


def get_qr_code_image_tag(qr_base64: str, size: int = 150) -> str:
    """
    Vráti HTML img tag s QR kódom
    """
    return f'<img src="data:image/png;base64,{qr_base64}" width="{size}" height="{size}" alt="PAY by square QR kód">'


# ==============================================================================
# POMOCNÉ FUNKCIE
# ==============================================================================

def format_date_sk(date_obj):
    """Formátuje dátum do slovenského formátu"""
    if date_obj:
        return date_obj.strftime("%d.%m.%Y")
    return ""


def get_payment_method_label(method):
    """Vráti slovenský názov formy úhrady"""
    labels = {
        'prevod': 'Bankový prevod',
        'hotovost': 'Hotovosť',
    }
    return labels.get(method, method)


def get_status_label(status):
    """Vráti slovenský názov stavu faktúry"""
    labels = {
        'draft': 'Koncept',
        'issued': 'Vystavená',
        'paid': 'Uhradená',
        'overdue': 'Po splatnosti',
        'cancelled': 'Stornovaná',
    }
    return labels.get(status, status)


def get_status_color(status):
    """Vráti CSS triedu pre farbu stavu"""
    colors = {
        'draft': 'bg-gray-100 text-gray-800',
        'issued': 'bg-blue-100 text-blue-800',
        'paid': 'bg-green-100 text-green-800',
        'overdue': 'bg-red-100 text-red-800',
        'cancelled': 'bg-gray-100 text-gray-500',
    }
    return colors.get(status, 'bg-gray-100 text-gray-800')
