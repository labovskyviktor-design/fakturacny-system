import os
import sys

# Add the current directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
except Exception as e:
    # Fallback app for debugging
    from flask import Flask
    import traceback
    
    app = Flask(__name__)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        error = traceback.format_exc()
        return f"""
        <html>
            <head><title>Application Error</title></head>
            <body style="font-family: monospace; padding: 20px;">
                <h1 style="color: red;">Application Import Error</h1>
                <p>The application failed to start due to an error during import.</p>
                <div style="background: #f0f0f0; padding: 15px; border-radius: 5px; overflow: auto;">
                    <pre>{error}</pre>
                </div>
                <h3>Environment:</h3>
                <ul>
                    <li>Python: {sys.version}</li>
                    <li>CWD: {os.getcwd()}</li>
                    <li>Content of .: {str(os.listdir('.'))}</li>
                </ul>
            </body>
        </html>
        """, 500
