"""
Cache wrapper pre API volania
Znižuje počet requestov na externé API
"""
from functools import wraps
from datetime import datetime, timedelta
import json


class SimpleCache:
    """Jednoduchý in-memory cache"""
    
    def __init__(self):
        self._cache = {}
        self._timestamps = {}
    
    def get(self, key):
        """Získa hodnotu z cache"""
        if key in self._cache:
            # Skontroluj expiraciu
            if key in self._timestamps:
                if datetime.now() < self._timestamps[key]:
                    return self._cache[key]
                else:
                    # Expirované - vymaž
                    del self._cache[key]
                    del self._timestamps[key]
        return None
    
    def set(self, key, value, timeout=300):
        """Uloží hodnotu do cache
        
        Args:
            key: Kľúč
            value: Hodnota
            timeout: Čas expirácie v sekundách (default 5 minút)
        """
        self._cache[key] = value
        self._timestamps[key] = datetime.now() + timedelta(seconds=timeout)
    
    def delete(self, key):
        """Vymaže hodnotu z cache"""
        if key in self._cache:
            del self._cache[key]
        if key in self._timestamps:
            del self._timestamps[key]
    
    def clear(self):
        """Vymaže celý cache"""
        self._cache.clear()
        self._timestamps.clear()
    
    def cleanup(self):
        """Vymaže expirované záznamy"""
        now = datetime.now()
        expired_keys = [
            key for key, timestamp in self._timestamps.items()
            if now >= timestamp
        ]
        for key in expired_keys:
            self.delete(key)


# Globálny cache instance
_cache = SimpleCache()


def cached(timeout=300, key_prefix=''):
    """Dekorátor pre cachovanie funkcií
    
    Args:
        timeout: Čas expirácie v sekundách
        key_prefix: Prefix pre cache kľúč
    
    Example:
        @cached(timeout=600, key_prefix='company')
        def lookup_company(ico):
            # ... expensive API call
            return result
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Vytvor cache kľúč
            cache_key = f"{key_prefix}:{f.__name__}:{str(args)}:{str(kwargs)}"
            
            # Skús získať z cache
            result = _cache.get(cache_key)
            if result is not None:
                return result
            
            # Zavolaj funkciu
            result = f(*args, **kwargs)
            
            # Ulož do cache
            if result is not None:
                _cache.set(cache_key, result, timeout)
            
            return result
        return decorated_function
    return decorator


def get_cache():
    """Vráti cache instanciu"""
    return _cache


def clear_cache():
    """Vymaže celý cache"""
    _cache.clear()


def cleanup_cache():
    """Vymaže expirované záznamy"""
    _cache.cleanup()
