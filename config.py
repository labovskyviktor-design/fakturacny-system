import os
import socket
import re
from datetime import timedelta


class Config:
    """Základná konfigurácia"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Databáza
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'fakturacny_system.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(
        seconds=int(os.environ.get('PERMANENT_SESSION_LIFETIME', 3600))
    )
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    UPLOAD_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}
    
    # API konfigurácia
    EKOSYSTEM_API_URL = "https://autoform.ekosystem.slovensko.digital/api/corporate_bodies"
    FREEBYSQUARE_API_URL = "https://api.freebysquare.sk/pay/v1/generate-png"
    ENABLE_QR_CODES = os.environ.get('ENABLE_QR_CODES', 'True') == 'True'
    
    # Rate limiting
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', 'True') == 'True'
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    
    # Cache konfigurácia
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minút
    
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    
    # Email konfigurácia (SendGrid)
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'  # SendGrid vyžaduje toto username
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@fakturask.sk')
    
    # Monitoring (Sentry)
    SENTRY_DSN = os.environ.get('SENTRY_DSN')


class DevelopmentConfig(Config):
    """Vývojová konfigurácia"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Produkčná konfigurácia"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    # PostgreSQL pre production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        Config.SQLALCHEMY_DATABASE_URI
    
    # Helper to force IPv4 resolution
    @staticmethod
    def resolve_db_host(uri):
        try:
            # Extract hostname and port from URI
            # Format: postgresql://user:pass@host:port/db
            match = re.search(r'@([^:/]+)(?::(\d+))?', uri)
            if match:
                host = match.group(1)
                port = match.group(2)
                
                # Resolve host to IPv4
                ipv4 = socket.gethostbyname(host)
                
                # Replace host with IPv4 in URI
                uri = uri.replace(f'@{host}', f'@{ipv4}')
                
                # Ensure sslmode is set (required when using IP to bypass hostname check)
                if 'sslmode=' not in uri:
                    sep = '&' if '?' in uri else '?'
                    uri += f'{sep}sslmode=require'
                
                # If verify-full is set, downgrade to require because IP won't match cert
                uri = uri.replace('sslmode=verify-full', 'sslmode=require')
                
                print(f"Resolved DB host {host} to {ipv4}")
        except Exception as e:
            print(f"Failed to resolve DB host: {e}")
        return uri

    # Ak je DATABASE_URL z Heroku/Render, oprav postgres:// na postgresql://
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    # Pre Vercel serverless: Supabase vyžaduje connection pooler (port 6543)
    if SQLALCHEMY_DATABASE_URI and 'supabase.co:5432' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(':5432/', ':6543/')
        if '?' not in SQLALCHEMY_DATABASE_URI:
            SQLALCHEMY_DATABASE_URI += '?options=-c%20search_path%3Dpublic'
            
    # Force IPv4 resolution for Vercel/Supabase compatibility
    if SQLALCHEMY_DATABASE_URI and 'supabase.co' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = resolve_db_host.__func__(SQLALCHEMY_DATABASE_URI)
    
    # Serverless-optimized pool settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 60,
        'pool_size': 2,
        'max_overflow': 3,
    }


class TestingConfig(Config):
    """Testovacia konfigurácia"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False


# Mapa konfigurácií
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Vráti konfiguráciu podľa FLASK_ENV"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
