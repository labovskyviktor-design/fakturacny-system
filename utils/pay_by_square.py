"""
PAY by square generátor
Korektná implementácia podľa SBA/bsqr.co štandardu
https://bsqr.co/schema/
"""
import base64
import struct
import lzma
from io import BytesIO
from typing import Optional
import qrcode
import requests


def generate_qr_code_external(
    amount: float,
    iban: str,
    swift: str = '',
    variable_symbol: str = '',
    constant_symbol: str = '',
    specific_symbol: str = '',
    beneficiary_name: str = '',
    beneficiary_address_1: str = '',
    beneficiary_address_2: str = '',
    note: str = '',
    due_date: str = '',
    currency: str = 'EUR'
) -> Optional[str]:
    """
    Generuje PAY by square QR kód pomocou externého API freebysquare.sk (v2)
    """
    try:
        # Params dict for v2 function
        params = {
            'amount': amount,
            'currencyCode': currency,
            'iban': iban,
            'bic': swift,
            'variableSymbol': variable_symbol,
            'constantSymbol': constant_symbol,
            'specificSymbol': specific_symbol,
            'paymentNote': note,
            'dueDate': due_date,
            'beneficiaryName': beneficiary_name,
            'beneficiaryAddressLine1': beneficiary_address_1,
            'beneficiaryAddressLine2': beneficiary_address_2
        }
        
        print(f"Volám externé API v2 (Primary) pre IBAN: {iban[:4]}...")
        return _generate_qr_code_external_v2(params)
        
    except Exception as e:
        print(f"Chyba pri príprave API v2: {e}")
        return None

def _generate_qr_code_external_v2(params: dict) -> Optional[str]:
    """Fallback na v2 POST API - vyžaduje inú štruktúru JSON"""
    try:
        api_url = "https://api.freebysquare.sk/pay/v1/generate-png-v2"
        
        # Transformácia params na v2 štruktúru
        v2_data = {
            "size": 300,
            "color": 1,
            "transparent": False,
            "payments": [
                {
                    "amount": float(params.get('amount', 0)),
                    "currencyCode": params.get('currencyCode', 'EUR'),
                    "paymentDueDate": params.get('dueDate', ''),
                    "variableSymbol": params.get('variableSymbol', ''),
                    "constantSymbol": params.get('constantSymbol', ''),
                    "specificSymbol": params.get('specificSymbol', ''),
                    "paymentNote": params.get('paymentNote', ''),
                    "beneficiaryName": params.get('beneficiaryName', ''),
                    "beneficiaryAddressLine1": params.get('beneficiaryAddressLine1', ''),
                    "beneficiaryAddressLine2": params.get('beneficiaryAddressLine2', ''),
                    "bankAccounts": [
                        {
                            "iban": params.get('iban', ''),
                            "bic": params.get('bic', '')
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(api_url, json=v2_data, timeout=10)
        
        if response.status_code == 200:
            png_bytes = response.content
            b64_string = base64.b64encode(png_bytes).decode('ascii')
            print("✓ QR kód vygenerovaný pomocou freebysquare.sk API v2")
            return f"data:image/png;base64,{b64_string}"
    except Exception as e:
        print(f"Chyba pri v2 fallback: {e}")
    return None


def crc32_bsqr(data: bytes) -> int:
    """
    CRC32 podľa bsqr.co špecifikácie (XOR so štandardným CRC32).
    """
    import binascii
    return binascii.crc32(data) & 0xFFFFFFFF


def lzma_compress_bysquare(data: bytes) -> bytes:
    """
    LZMA kompresia podľa bysquare špecifikácie.
    Používa LZMA1 s properties byte na začiatku.
    """
    # LZMA properties: lc=3, lp=0, pb=2 -> properties byte = (pb * 5 + lp) * 9 + lc = 93 = 0x5D
    # Dict size = 128KB = 0x00020000 (little-endian)
    lzma_props = b'\x5d\x00\x00\x02\x00'
    
    compressed = lzma.compress(
        data,
        format=lzma.FORMAT_RAW,
        filters=[{
            'id': lzma.FILTER_LZMA1,
            'lc': 3,
            'lp': 0,
            'pb': 2,
            'dict_size': 128 * 1024
        }]
    )
    
    # Vrátime properties + compressed data
    return lzma_props + compressed


def generate_pay_by_square_string(
    amount: float,
    iban: str,
    swift: str = '',
    variable_symbol: str = '',
    constant_symbol: str = '',
    specific_symbol: str = '',
    beneficiary_name: str = '',
    beneficiary_address_1: str = '',
    beneficiary_address_2: str = '',
    note: str = '',
    due_date: str = '',
    currency: str = 'EUR'
) -> str:
    """
    Generuje PAY by square string podľa SBA špecifikácie v1.1.0
    
    Štruktúra dát (tab-separated):
    0: InvoiceID (voliteľné)
    1: Payments (počet platieb, vždy "1")
    2: PaymentOptions (0=platba, 1=standing order, vždy "1" pre bežnú platbu)
    3: Amount
    4: CurrencyCode
    5: PaymentDueDate (YYYYMMDD)
    6: VariableSymbol
    7: ConstantSymbol
    8: SpecificSymbol
    9: OriginatorsReferenceInformation (voliteľné)
    10: PaymentNote
    11: BankAccounts (počet účtov, vždy "1")
    12: IBAN
    13: BIC (SWIFT)
    14: StandingOrderExt (0 = žiadne)
    15: DirectDebitExt (0 = žiadne)
    16: BeneficiaryName
    17: BeneficiaryAddressLine1
    18: BeneficiaryAddressLine2
    """
    # Očistíme IBAN od medzier
    iban = iban.replace(' ', '').replace('-', '').upper()
    
    # Formátujeme sumu na 2 desatinné miesta
    amount_str = f'{amount:.2f}'
    
    # Zostavíme dátový reťazec podľa špecifikácie
    # Všetky polia oddelené tabulátormi
    fields = [
        '',                          # 0: InvoiceID
        '1',                         # 1: Payments (počet)
        '1',                         # 2: PaymentOptions (regular payment)
        amount_str,                  # 3: Amount
        currency,                    # 4: CurrencyCode
        due_date,                    # 5: PaymentDueDate
        variable_symbol,             # 6: VariableSymbol
        constant_symbol,             # 7: ConstantSymbol  
        specific_symbol,             # 8: SpecificSymbol
        '',                          # 9: OriginatorsReferenceInformation
        note[:140] if note else '',  # 10: PaymentNote (max 140)
        '1',                         # 11: BankAccounts (počet)
        iban,                        # 12: IBAN
        swift.upper() if swift else '',  # 13: BIC
        '0',                         # 14: StandingOrderExt
        '0',                         # 15: DirectDebitExt
        beneficiary_name[:70] if beneficiary_name else '',  # 16: BeneficiaryName
        beneficiary_address_1[:70] if beneficiary_address_1 else '',  # 17
        beneficiary_address_2[:70] if beneficiary_address_2 else '',  # 18
    ]
    
    # Spojíme tabulátormi
    data_string = '\t'.join(fields)
    data_bytes = data_string.encode('utf-8')
    
    # Vypočítame CRC32
    crc = crc32_bsqr(data_bytes)
    
    # LZMA kompresia
    try:
        compressed = lzma_compress_bysquare(data_bytes)
    except Exception as e:
        print(f"LZMA compression failed: {e}")
        # Fallback - použijeme nekomprimované dáta s headerom
        compressed = b'\x00\x00' + data_bytes
    
    # Zostavíme výsledný paket podľa bsqr.co špecifikácie:
    # [2B header] + [4B CRC32 LE] + [LZMA compressed data with props]
    
    # Header: horných 4 bitov = 0 (typ pay by square), dolných 12 bitov = dĺžka v bajtoch
    # Dĺžka = 2 (header) + 4 (CRC32) + len(compressed)
    total_length = len(compressed)
    
    # Header je big-endian: [type:4bit][reserved:4bit][length:8bit] - celkom 16 bit
    # Type 0 = PAY, length v bajtoch
    header_value = (0x00 << 12) | (total_length & 0x0FFF)
    header = struct.pack('>H', header_value)
    
    # CRC32 little-endian
    crc_bytes = struct.pack('<I', crc)
    
    # Kompletný paket
    packet = header + crc_bytes + compressed
    
    # Padding na násobok 5 pre Base32
    padding_needed = (5 - (len(packet) % 5)) % 5
    packet += b'\x00' * padding_needed
    
    # Base32 encoding (uppercase, bez paddingu =)
    encoded = base64.b32encode(packet).decode('ascii').rstrip('=')
    
    return encoded


def generate_qr_code_base64(
    amount: float,
    iban: str,
    swift: str = '',
    variable_symbol: str = '',
    constant_symbol: str = '',
    specific_symbol: str = '',
    beneficiary_name: str = '',
    beneficiary_address_1: str = '',
    beneficiary_address_2: str = '',
    note: str = '',
    due_date: str = '',
    currency: str = 'EUR'
) -> Optional[str]:
    """
    Generuje PAY by square QR kód.
    Priorita: Externé API (freebysquare.sk) -> Lokálne generovanie (fallback)
    """
    # Pokus 1: Externé API (overené, funguje s bankovými aplikáciami)
    qr_code = generate_qr_code_external(
        amount=amount,
        iban=iban,
        swift=swift,
        variable_symbol=variable_symbol,
        constant_symbol=constant_symbol,
        specific_symbol=specific_symbol,
        beneficiary_name=beneficiary_name,
        beneficiary_address_1=beneficiary_address_1,
        beneficiary_address_2=beneficiary_address_2,
        note=note,
        due_date=due_date,
        currency=currency
    )
    
    if qr_code:
        print("✓ QR kód vygenerovaný pomocou externého API")
        return qr_code
    
    # Pokus 2: Lokálne generovanie (fallback)
    print("⚠ Externé API nedostupné, používam lokálne generovanie")
    try:
        from utils.helpers import generate_pay_by_square
        
        # Očistíme IBAN
        iban = iban.replace(' ', '').upper()
        
        # Konvertujeme dátum ak je to string
        if isinstance(due_date, str):
            due_date = due_date.replace('-', '')
            
        qr_data_uri = generate_pay_by_square(
            amount=amount,
            iban=iban,
            swift=swift,
            variable_symbol=variable_symbol,
            constant_symbol=constant_symbol,
            specific_symbol=specific_symbol,
            note=note,
            beneficiary_name=beneficiary_name,
            due_date=due_date
        )
        print("✓ QR kód vygenerovaný lokálne")
        return qr_data_uri
        
    except Exception as e:
        print(f"✗ Chyba pri lokálnom generovaní QR: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_sepa_qr(
    amount: float,
    iban: str,
    bic: str = '',
    beneficiary_name: str = '',
    reference: str = '',
    note: str = ''
) -> Optional[str]:
    """
    Generuje SEPA QR kód (EPC QR) - európsky štandard.
    Funguje vo väčšine európskych bankových aplikácií.
    """
    try:
        iban = iban.replace(' ', '').upper()
        
        # EPC QR formát (verzia 002)
        lines = [
            'BCD',
            '002',
            '1',
            'SCT',
            bic.upper() if bic else '',
            beneficiary_name[:70] if beneficiary_name else '',
            iban,
            f'EUR{amount:.2f}',
            '',
            reference[:35] if reference else '',
            note[:140] if note else '',
            '',
        ]
        
        data = '\n'.join(lines)
        
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color='black', back_color='white')
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        b64_string = base64.b64encode(buffer.getvalue()).decode('ascii')
        return f'data:image/png;base64,{b64_string}'
        
    except Exception as e:
        print(f'Chyba pri generovaní SEPA QR: {e}')
        return None
