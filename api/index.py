import os
import sys

# Add the current directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
except Exception as e:
    # Fallback app for debugging startup errors
    from flask import Flask
    import traceback
    
    app = Flask(__name__)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        error = traceback.format_exc()
        return f"""
        <!DOCTYPE html>
        <html>
            <head><title>Application Startup Error</title></head>
            <body style="font-family: monospace; padding: 20px;">
                <h1 style="color: red;">Application Startup Error</h1>
                <p>The application failed to import or initialize on Vercel.</p>
                <p><strong>This usually means a configuration error in Environment Variables or a missing dependency.</strong></p>
                <div style="background: #f0f0f0; padding: 15px; border-radius: 5px; overflow: auto; max-width: 100%;">
                    <pre style="white-space: pre-wrap;">{error}</pre>
                </div>
                <h3>Environment Info:</h3>
                <ul>
                    <li>Python: {sys.version}</li>
                    <li>CWD: {os.getcwd()}</li>
                    <li>FLASK_ENV: {os.environ.get('FLASK_ENV', 'unknown')}</li>
                    <li>DATABASE_URL present: {'Yes' if os.environ.get('DATABASE_URL') else 'No'}</li>
                    <li>SECRET_KEY check: {'Valid' if os.environ.get('SECRET_KEY') and '<' not in os.environ.get('SECRET_KEY') else 'INVALID (< or > found)'}</li>
                </ul>
            </body>
        </html>
        """, 500
