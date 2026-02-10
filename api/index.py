from flask import Flask

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    try:
        import psycopg2
        import PIL
        import reportlab
        import requests
        import sentry_sdk
        deps = "psycopg2, PIL, reportlab, requests, sentry_sdk LOADED!"
    except Exception as e:
        deps = f"Dependency Error: {e}"
        
    return f"Hello from Minimal Vercel App! Runtime is working. Dependencies: {deps}"
