"""
Vercel serverless function entry point for Flask app
"""
from app import app

# Vercel expects a variable named 'app' or a handler function
# Flask app is already named 'app', so we just need to export it
