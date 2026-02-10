import sys
import os
import traceback

# Add the parent directory to python path so we can import the main app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
except Exception as e:
    # If the main app fails to import, create a minimal debug app
    from flask import Flask
    app = Flask(__name__)
    
    error_msg = f"Failed to import app: {e}\n{traceback.format_exc()}"
    
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def error_page(path):
        return f"""<html><body style="font-family: monospace; white-space: pre-wrap;">
APP IMPORT ERROR:
{error_msg}
</body></html>""", 500
