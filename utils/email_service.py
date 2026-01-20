"""
Služba pre odosielanie emailov (SendGrid cez Flask-Mail)
"""
from flask_mail import Mail, Message
from flask import current_app, render_template, render_template_string
from threading import Thread
import traceback
import os

mail = Mail()


def send_async_email(app, msg):
    """Asynchrónne odoslanie emailu (aby neblokovalo request)"""
    with app.app_context():
        try:
            mail.send(msg)
            app.logger.info(f"Email sent successfully to: {msg.recipients}")
        except Exception as e:
            app.logger.error(f"Failed to send email to {msg.recipients}: {e}")
            app.logger.error(traceback.format_exc())


def send_email(subject, recipient, body=None, html_body=None, template=None, **kwargs):
    """
    Odošle email pomocou Flask-Mail
    
    Args:
        subject: Predmet emailu
        recipient: Email príjemcu (alebo list emailov)
        body: Textová verzia emailu (fallback)
        html_body: HTML verzia emailu (priama)
        template: Cesta k šablóne (napr. 'emails/activation.html')
        **kwargs: Premenné do šablóny
    """
    try:
        # Kontrola API kľúča
        if not current_app.config.get('MAIL_PASSWORD'):
            if current_app.config.get('DEBUG'):
                current_app.logger.warning(f"Email simulation (missing API key): To={recipient}, Subject={subject}")
                return True # V dev mode sa tvárime že prešlo
            
            current_app.logger.error("Email not sent: SENDGRID_API_KEY is missing")
            return False

        msg = Message(
            subject=subject,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[recipient] if isinstance(recipient, str) else recipient
        )
        
        # Renderovanie šablóny ak je zadaná
        if template:
            try:
                msg.html = render_template(template, **kwargs)
            except Exception as e:
                current_app.logger.error(f"Error rendering values for email template: {e}")
                # Fallback ak zlyhá render
                msg.body = body or "Error rendering email."
        elif html_body:
            msg.html = html_body
        else:
            msg.body = body or ""

        # Odoslať v novom vlákne
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
        current_app.logger.info(f"Email to {recipient} queued. Subject: {subject}")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Error preparing email for {recipient}: {e}")
        current_app.logger.error(traceback.format_exc())
        return False

def send_activation_email(user):
    """Odošle aktivačný email novému používateľovi"""
    from flask import url_for
    from utils.tokens import TokenGenerator
    
    token = TokenGenerator.generate_token(user.email, salt='activate-account')
    confirm_url = url_for('activate_account', token=token, _external=True)
    
    subject = "Aktivácia účtu - FakturaSK"
    
    return send_email(
        subject=subject, 
        recipient=user.email,
        template='emails/activation_email.html',
        user=user,
        confirm_url=confirm_url,
        body=f"Pre aktiváciu kliknite na: {confirm_url}" # Fallback
    )


def send_reset_email(user):
    """Odošle email pre obnovu zabudnutého hesla"""
    from flask import url_for
    from utils.tokens import TokenGenerator
    
    token = TokenGenerator.generate_token(user.email, salt='recover-key')
    recover_url = url_for('reset_password_token', token=token, _external=True)
    
    subject = "Obnova hesla - FakturaSK"
    
    return send_email(
        subject=subject,
        recipient=user.email,
        template='emails/reset_password_email.html',
        user=user,
        recover_url=recover_url,
        body=f"Pre obnovu hesla kliknite na: {recover_url}" # Fallback
    )
