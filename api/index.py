from flask import Flask, request
import traceback
import sys
import os

# Add the current directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def probe(path):
    # Get step from query param, default to 0
    # Usage: /?step=1, /?step=2, etc.
    step = request.args.get('step', '0')
    limit = int(step) if step.isdigit() else 0
    
    logs = [f"Probe Level {limit} started.", "----------------"]
    
    try:
        # Step 0: Basic imports (already tested, but verify)
        if limit >= 0:
            logs.append("Step 0: Core libs...")
            import psycopg2
            import PIL
            import reportlab
            logs.append("OK.")
            
        # Step 1: Config
        if limit >= 1:
            logs.append("Step 1: Importing config...")
            import config
            logs.append("OK.")

        # Step 2: Utils
        if limit >= 2:
            logs.append("Step 2: Importing utils...")
            import utils.email_service
            import utils.company_lookup
            import utils.pay_by_square
            logs.append("OK.")

        # Step 3: Models
        if limit >= 3:
            logs.append("Step 3: Importing models...")
            import models
            logs.append("OK.")

        # Step 4: Full App
        if limit >= 4:
            logs.append("Step 4: Importing app...")
            from app import app as real_app
            logs.append("OK. App object created.")
            
    except Exception as e:
        logs.append(f"EXCEPTION CAUGHT: {e}")
        logs.append(traceback.format_exc())

    return f"""
    <html>
        <body style="font-family: monospace; white-space: pre-wrap;">
{'<br>'.join(logs)}
        </body>
    </html>
    """
