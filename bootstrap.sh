#!/bin/bash
echo "--- STARTING PDF BINARY BOOTSTRAP ---"

# 1. Hladanie wkhtmltopdf
echo "Searching for wkhtmltopdf in /nix/store..."
WKBIN=$(find /nix/store -name wkhtmltopdf -type f -executable -print -quit 2>/dev/null)

if [ -n "$WKBIN" ]; then
    echo "Found wkhtmltopdf at: $WKBIN"
    ln -sf "$WKBIN" /app/wkhtmltopdf_local
    chmod +x /app/wkhtmltopdf_local
    echo "Created stable symlink: /app/wkhtmltopdf_local"
else
    echo "ERROR: wkhtmltopdf NOT FOUND in /nix/store"
fi

# 2. Hladanie xvfb-run
echo "Searching for xvfb-run in /nix/store..."
XVFBBIN=$(find /nix/store -name xvfb-run -type f -executable -print -quit 2>/dev/null)

if [ -n "$XVFBBIN" ]; then
    echo "Found xvfb-run at: $XVFBBIN"
    ln -sf "$XVFBBIN" /app/xvfb_run_local
    chmod +x /app/xvfb_run_local
    echo "Created stable symlink: /app/xvfb_run_local"
else
    echo "ERROR: xvfb-run NOT FOUND in /nix/store"
fi

echo "--- BOOTSTRAP COMPLETE ---"

# 3. Spustenie gunicorn
echo "Starting Gunicorn..."
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120
