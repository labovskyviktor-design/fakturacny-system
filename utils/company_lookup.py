"""
Vyhľadávanie firiem cez Ekosystém.Digital API
Obsahuje dáta priamo z RPO (Register právnických osôb)
"""
import requests
from typing import Optional, Dict, Any, List
import re
from utils.sk_companies_db import SLOVAK_COMPANIES
from utils.cache import cached


class CompanyLookup:
    """Služba pre vyhľadávanie firiem v slovenských registroch"""
    
    # Ekosystém.Digital API (Slovensko.Digital) - primárny zdroj
    EKOSYSTEM_API_URL = "https://autoform.ekosystem.slovensko.digital/api/corporate_bodies"
    
    # Alternatívny endpoint
    EKOSYSTEM_SEARCH_URL = "https://autoform.ekosystem.slovensko.digital/api/corporate_bodies/search"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FakturaSK/2.0 (Slovak Invoice System)',
            'Accept': 'application/json',
            'Accept-Language': 'sk-SK,sk;q=0.9'
        })
    
    @cached(timeout=600, key_prefix='company_lookup')
    def lookup(self, ico: str) -> Optional[Dict[str, Any]]:
        """
        Vyhľadá firmu podľa IČO.
        Používa Ekosystém.Digital API ako primárny zdroj.
        """
        ico = self._clean_ico(ico)
        if not ico:
            return None
        
        # 1. Primárne: Ekosystém.Digital API
        result = self._try_ekosystem_api(ico)
        if result:
            return result
        
        # 2. Fallback na lokálnu databázu
        result = self._get_local_data(ico)
        if result:
            return result
        
        return None
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Vyhľadá firmy podľa názvu alebo IČO.
        """
        if not query or len(query) < 2:
            return []
        
        try:
            # Skúsime Ekosystém.Digital search
            url = f"{self.EKOSYSTEM_SEARCH_URL}"
            params = {'q': query, 'limit': limit}
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                items = data if isinstance(data, list) else data.get('results', data.get('items', []))
                
                for item in items[:limit]:
                    parsed = self._parse_ekosystem_response(item)
                    if parsed and parsed.get('name'):
                        results.append(parsed)
                
                return results
                
        except Exception as e:
            print(f"Search error: {e}")
        
        # Fallback na lokálnu databázu
        return self._search_local(query, limit)
    
    def _clean_ico(self, ico: str) -> str:
        """Očistí a validuje IČO"""
        ico = re.sub(r'\D', '', ico)
        if len(ico) < 6 or len(ico) > 8:
            return ''
        return ico.zfill(8)
    
    def _try_ekosystem_api(self, ico: str) -> Optional[Dict[str, Any]]:
        """
        Získa údaje z Ekosystém.Digital API.
        Tento API poskytuje dáta priamo z RPO.
        """
        try:
            # Priamy lookup podľa IČO
            url = f"{self.EKOSYSTEM_API_URL}/{ico}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_ekosystem_response(data)
            
            # Skúsime search endpoint
            url = self.EKOSYSTEM_SEARCH_URL
            params = {'q': ico}
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # API môže vrátiť list alebo objekt
                items = data if isinstance(data, list) else data.get('results', data.get('items', []))
                
                if items:
                    # Nájdeme presný match podľa IČO
                    for item in items:
                        item_ico = str(item.get('cin', item.get('ico', ''))).zfill(8)
                        if item_ico == ico:
                            return self._parse_ekosystem_response(item)
                    
                    # Ak nie je presný match, vrátime prvý výsledok
                    return self._parse_ekosystem_response(items[0])
                    
        except requests.exceptions.Timeout:
            print("Ekosystém API timeout")
        except requests.exceptions.ConnectionError:
            print("Ekosystém API connection error")
        except Exception as e:
            print(f"Ekosystém API error: {e}")
        
        return None
    
    def _parse_ekosystem_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parsuje odpoveď z Ekosystém.Digital API"""
        result = {
            'name': '',
            'street': '',
            'city': '',
            'zip_code': '',
            'ico': '',
            'dic': '',
            'ic_dph': '',
            'legal_form': '',
            'established_on': '',
            'terminated_on': ''
        }
        
        if not data:
            return result
        
        # Názov firmy
        name_keys = ['name', 'formatted_name', 'full_name', 'nazov', 'obchodne_meno']
        for key in name_keys:
            if data.get(key):
                result['name'] = str(data[key]).strip()
                break
        
        # IČO (CIN = Corporate Identification Number)
        ico = data.get('cin', data.get('ico', data.get('id', '')))
        result['ico'] = str(ico).zfill(8) if ico else ''
        
        # DIČ
        dic_keys = ['tin', 'dic', 'tax_id']
        for key in dic_keys:
            if data.get(key):
                result['dic'] = str(data[key])
                break
        
        # IČ DPH
        vat_keys = ['vatin', 'ic_dph', 'vat_id']
        for key in vat_keys:
            if data.get(key):
                result['ic_dph'] = str(data[key])
                break
        
        # Právna forma
        legal_form = data.get('legal_form', data.get('pravna_forma', {}))
        if isinstance(legal_form, dict):
            result['legal_form'] = legal_form.get('name', legal_form.get('value', ''))
        elif isinstance(legal_form, str):
            result['legal_form'] = legal_form
        
        # Adresa - môže byť v rôznych formátoch
        address = data.get('formatted_address', data.get('address', data.get('sidlo', {})))
        
        if isinstance(address, str):
            # Parsujeme textovú adresu
            parsed = self._parse_address_string(address)
            result.update(parsed)
        elif isinstance(address, dict):
            # Štruktúrovaná adresa
            result['street'] = self._get_street_from_address(address)
            result['city'] = address.get('municipality', address.get('city', address.get('obec', '')))
            result['zip_code'] = str(address.get('postal_code', address.get('zip', address.get('psc', '')))).replace(' ', '')
        
        # Ak nemáme ulicu, skúsime alternatívne polia
        if not result['street']:
            street_keys = ['street', 'ulica', 'street_name']
            for key in street_keys:
                if data.get(key):
                    result['street'] = str(data[key])
                    break
        
        # Dátumy
        result['established_on'] = data.get('established_on', data.get('datum_vzniku', ''))
        result['terminated_on'] = data.get('terminated_on', data.get('datum_zaniku', ''))
        
        return result
    
    def _get_street_from_address(self, address: dict) -> str:
        """Zostaví ulicu z adresných komponentov"""
        parts = []
        
        street = address.get('street', address.get('ulica', address.get('street_name', '')))
        if street:
            parts.append(str(street))
        
        reg_number = address.get('reg_number', address.get('cislo_registra', ''))
        building_number = address.get('building_number', address.get('orientacne_cislo', address.get('cislo_domu', '')))
        
        if reg_number and building_number:
            parts.append(f'{reg_number}/{building_number}')
        elif building_number:
            parts.append(str(building_number))
        elif reg_number:
            parts.append(str(reg_number))
        
        return ' '.join(parts)
    
    def _parse_address_string(self, address: str) -> Dict[str, str]:
        """Parsuje textovú adresu"""
        result = {'street': '', 'city': '', 'zip_code': ''}
        
        if not address:
            return result
        
        # Hľadáme PSČ (5 číslic)
        psc_match = re.search(r'(\d{3}\s?\d{2})', address)
        if psc_match:
            result['zip_code'] = psc_match.group(1).replace(' ', '')
            address = address.replace(psc_match.group(0), '').strip()
        
        # Rozdelíme podľa čiarky
        parts = [p.strip() for p in address.split(',') if p.strip()]
        
        if len(parts) >= 2:
            result['street'] = parts[0]
            result['city'] = parts[-1]
        elif len(parts) == 1:
            result['street'] = parts[0]
        
        return result
    
    def _get_local_data(self, ico: str) -> Optional[Dict[str, Any]]:
        """Získa údaje z lokálnej databázy"""
        return SLOVAK_COMPANIES.get(ico)
    
    def _search_local(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Vyhľadá v lokálnej databáze"""
        query_lower = query.lower()
        results = []
        
        for ico, data in SLOVAK_COMPANIES.items():
            if query_lower in data.get('name', '').lower() or query_lower in ico:
                results.append(data)
                if len(results) >= limit:
                    break
        
        return results


def lookup_company(ico: str) -> Optional[Dict[str, Any]]:
    """Helper funkcia pre vyhľadanie firmy podľa IČO"""
    service = CompanyLookup()
    return service.lookup(ico)


def search_companies(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Helper funkcia pre vyhľadanie firiem"""
    service = CompanyLookup()
    return service.search(query, limit)
