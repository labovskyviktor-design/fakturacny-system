"""
RPO Service - Integrácia so slovenským Registrom právnických osôb (RPO)
Dokumentácia API: https://susrrpo.docs.apiary.io/
"""
import requests
from typing import Optional, Dict, Any


class RPOService:
    """Služba pre vyhľadávanie firiem v slovenskom RPO"""
    
    # Základná URL pre RPO API
    BASE_URL = "https://rpo.statistics.sk/rpo/api/v1"
    
    # Alternatívna URL (Oracle Object Storage pre bulk data)
    BULK_URL = "https://frkqbrydxwdp.compat.objectstorage.eu-frankfurt-1.oraclecloud.com/susr-rpo"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'FakturacnySystem/1.0'
        })
    
    def lookup_by_ico(self, ico: str) -> Optional[Dict[str, Any]]:
        """
        Vyhľadá firmu podľa IČO v RPO.
        
        Args:
            ico: IČO firmy (8 číslic)
            
        Returns:
            Slovník s údajmi firmy alebo None ak nebola nájdená
        """
        # Očistíme IČO od medzier a doplníme nuly na začiatok
        ico = ico.strip().replace(' ', '')
        
        # IČO by malo mať 8 číslic
        if not ico.isdigit():
            return None
        
        ico = ico.zfill(8)  # Doplníme nuly na začiatok
        
        try:
            # Skúsime hlavné API
            result = self._try_main_api(ico)
            if result:
                return result
            
            # Ak hlavné API zlyhá, skúsime alternatívne zdroje
            result = self._try_finstat_api(ico)
            if result:
                return result
                
            return None
            
        except Exception as e:
            print(f"RPO lookup error: {e}")
            return None
    
    def _try_main_api(self, ico: str) -> Optional[Dict[str, Any]]:
        """Skúsi hlavné RPO API"""
        try:
            # Endpoint pre vyhľadávanie podľa IČO
            url = f"{self.BASE_URL}/organizations/{ico}"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_rpo_response(data)
            
            # Skúsime alternatívny endpoint
            url = f"{self.BASE_URL}/search?ico={ico}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list) and len(data) > 0:
                    return self._parse_rpo_response(data[0])
                elif data and isinstance(data, dict):
                    return self._parse_rpo_response(data)
            
        except requests.RequestException:
            pass
        
        return None
    
    def _try_finstat_api(self, ico: str) -> Optional[Dict[str, Any]]:
        """
        Skúsi alternatívne verejné API (FinStat alebo podobné)
        Toto je záložný zdroj ak hlavné RPO API nefunguje
        """
        try:
            # Skúsime slovenský ORSR (obchodný register)
            url = f"https://www.orsr.sk/hladaj_ico.asp?ICO={ico}&SID=0"
            
            # Toto je len ukážka - v reálnej implementácii by sme parsovali HTML
            # alebo použili iné API
            
        except Exception:
            pass
        
        return None
    
    def _parse_rpo_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parsuje odpoveď z RPO API do štandardného formátu
        
        Štruktúra RPO odpovede môže obsahovať:
        - nazov / name / full_name
        - sidlo / address (mesto, ulica, psc)
        - ico
        - dic
        - ic_dph
        - pravna_forma / legal_form
        - statutari / representatives
        """
        result = {
            'name': '',
            'street': '',
            'city': '',
            'zip_code': '',
            'ico': '',
            'dic': '',
            'ic_dph': '',
            'legal_form': '',
            'representatives': []
        }
        
        # Názov
        result['name'] = (
            data.get('nazov') or 
            data.get('name') or 
            data.get('full_name') or 
            data.get('obchodne_meno') or
            data.get('company_name') or
            ''
        )
        
        # IČO
        result['ico'] = str(data.get('ico', data.get('ICO', ''))).zfill(8)
        
        # DIČ
        result['dic'] = data.get('dic') or data.get('DIC') or data.get('tax_id') or ''
        
        # IČ DPH
        result['ic_dph'] = (
            data.get('ic_dph') or 
            data.get('IC_DPH') or 
            data.get('vat_id') or 
            ''
        )
        
        # Adresa - môže byť vnorená alebo flat
        address = data.get('sidlo') or data.get('address') or data.get('adresa') or {}
        
        if isinstance(address, dict):
            result['street'] = (
                address.get('ulica') or 
                address.get('street') or 
                address.get('ulica_cislo') or
                ''
            )
            result['city'] = (
                address.get('mesto') or 
                address.get('city') or 
                address.get('obec') or
                ''
            )
            result['zip_code'] = str(
                address.get('psc') or 
                address.get('zip_code') or 
                address.get('postal_code') or
                ''
            ).replace(' ', '')
        elif isinstance(address, str):
            # Pokus o parsovanie textovej adresy
            result['street'] = address
        
        # Ak nie je adresa vo vnorenom objekte, skúsime flat štruktúru
        if not result['street']:
            result['street'] = data.get('ulica') or data.get('street') or ''
        if not result['city']:
            result['city'] = data.get('mesto') or data.get('obec') or data.get('city') or ''
        if not result['zip_code']:
            result['zip_code'] = str(data.get('psc') or data.get('zip_code') or '').replace(' ', '')
        
        # Právna forma
        result['legal_form'] = (
            data.get('pravna_forma') or 
            data.get('legal_form') or 
            ''
        )
        
        # Štatutári
        representatives = data.get('statutari') or data.get('representatives') or []
        if isinstance(representatives, list):
            result['representatives'] = representatives
        
        return result


def lookup_company(ico: str) -> Optional[Dict[str, Any]]:
    """
    Pomocná funkcia pre vyhľadanie firmy podľa IČO.
    
    Args:
        ico: IČO firmy
        
    Returns:
        Slovník s údajmi firmy alebo None
    """
    service = RPOService()
    return service.lookup_by_ico(ico)


# Testovací mock pre vývoj (keď API nie je dostupné)
MOCK_DATA = {
    '36421928': {
        'name': 'Slovak Security Agency s.r.o.',
        'street': 'Hlavná 123',
        'city': 'Bratislava',
        'zip_code': '81101',
        'ico': '36421928',
        'dic': '2021234567',
        'ic_dph': 'SK2021234567',
        'legal_form': 's.r.o.',
        'representatives': ['Ján Čurma']
    },
    '35697270': {
        'name': 'Slovenská sporiteľňa, a.s.',
        'street': 'Tomášikova 48',
        'city': 'Bratislava',
        'zip_code': '83237',
        'ico': '35697270',
        'dic': '2020417809',
        'ic_dph': 'SK2020417809',
        'legal_form': 'a.s.',
        'representatives': []
    },
    '00151742': {
        'name': 'Železnice Slovenskej republiky',
        'street': 'Klemensova 8',
        'city': 'Bratislava',
        'zip_code': '81361',
        'ico': '00151742',
        'dic': '2020480121',
        'ic_dph': '',
        'legal_form': 'štátny podnik',
        'representatives': []
    }
}


def lookup_company_with_fallback(ico: str) -> Optional[Dict[str, Any]]:
    """
    Vyhľadá firmu s fallback na mock dáta pre testovanie.
    
    V produkcii by sa mali použiť len reálne API volania.
    """
    # Očistíme IČO
    ico = ico.strip().replace(' ', '').zfill(8)
    
    # Najprv skúsime reálne API
    service = RPOService()
    result = service.lookup_by_ico(ico)
    
    if result and result.get('name'):
        return result
    
    # Fallback na mock dáta (pre vývoj/demo)
    if ico in MOCK_DATA:
        return MOCK_DATA[ico]
    
    return None
