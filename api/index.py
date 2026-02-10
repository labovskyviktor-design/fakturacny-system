import sys
import os

# Add the parent directory to python path so we can import the main app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the actual Flask application
from app import app

# Vercel will use this 'app' object as the WSGI application
# No need to define routes here - they're all in app.py
