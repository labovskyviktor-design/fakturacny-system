from flask import current_app
from itsdangerous import URLSafeTimedSerializer

class TokenGenerator:
    """Helper pre generovanie a overovanie tokenov"""
    
    @staticmethod
    def generate_token(email, salt):
        """Vygeneruje bezpečný token pre daný email"""
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=salt)

    @staticmethod
    def confirm_token(token, salt, expiration=3600):
        """
        Overí token a vráti email.
        expiration: platnosť v sekundách (default 1 hodina)
        """
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=salt,
                max_age=expiration
            )
            return email
        except Exception:
            return False
