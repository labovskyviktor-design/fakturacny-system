from flask import Flask, make_response
import traceback
import sys
import os

# Add the current directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LazyApp:
    def __init__(self):
        self.app = None
        self.error = None
        
    def get_app(self):
        if self.app:
            return self.app
            
        if self.error:
            return None

        try:
            # Attempt to import the real app
            from app import app as real_app
            self.app = real_app
            return self.app
        except Exception:
            self.error = traceback.format_exc()
            return None

    def __call__(self, environ, start_response):
        app = self.get_app()
        
        if app:
            return app(environ, start_response)
        else:
            # Return error response
            status = '500 Internal Server Error'
            response_headers = [('Content-type', 'text/html')]
            start_response(status, response_headers)
            
            error_html = f"""
            <!DOCTYPE html>
            <html>
                <head><title>Startup Error via LazyApp</title></head>
                <body style="font-family: monospace; padding: 20px;">
                    <h1 style="color: red;">Application Import Failed</h1>
                    <p>The application failed to initialize at runtime.</p>
                    <div style="background: #f0f0f0; padding: 15px; border-radius: 5px; overflow: auto;">
                        <pre>{self.error}</pre>
                    </div>
                </body>
            </html>
            """
            return [error_html.encode('utf-8')]

# Export the lazy app as 'app' for Vercel
app = LazyApp()
