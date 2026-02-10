from flask import Flask

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return "Hello from Minimal Vercel App! If you see this, the runtime is working."
