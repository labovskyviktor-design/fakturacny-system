"""
Služba pre odosielanie emailov (SendGrid cez Flask-Mail)
"""
from flask_mail import Mail, Message
from flask import current_app, render_template_string
from threading import Thread
import traceback

mail = Mail()


def send_async_email(app, msg):
    """Asynchrónne odoslanie emailu (aby neblokovalo request)"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            app.logger.error(f"Failed to send email: {e}")


def send_email(subject, recipient, body, html_body=None, attachments=None):
    """
    Odošle email pomocou Flask-Mail
    
    Args:
        subject: Predmet emailu
        recipient: Email príjemcu (alebo list emailov)
        body: Textová verzia emailu
        html_body: HTML verzia emailu (voliteľné)
        attachments: Zoznam príloh [('filename', 'mimetype', data)]
    """
    try:
        if not current_app.config.get('MAIL_PASSWORD'):
            current_app.logger.warning("Email not sent: SENDGRID_API_KEY is missing")
            return False

        msg = Message(
            subject=subject,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[recipient] if isinstance(recipient, str) else recipient
        )
        msg.body = body
        if html_body:
            msg.html = html_body
            
        if attachments:
            for filename, content_type, data in attachments:
                msg.attach(filename, content_type, data)
        
        # Odoslať v novom vlákne
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
        current_app.logger.info(f"Email to {recipient} queued for sending (Subject: {subject})")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Error preparing email for {recipient}: {e}")
        current_app.logger.error(traceback.format_exc())
        return False
