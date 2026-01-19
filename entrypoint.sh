#!/bin/bash
echo "--- RUNTIME BINARY DISCOVERY START ---"

# 1. Nájdeme wkhtmltopdf
WK_PATH=$(which wkhtmltopdf 2>/dev/null)
if [ -z "$WK_PATH" ]; then
    WK_PATH=$(find /nix/store -name wkhtmltopdf -type f -executable -print -quit 2>/dev/null)
fi
echo "WKHTMLTOPDF_PATH=$WK_PATH"
export WKHTMLTOPDF_PATH="$WK_PATH"

# 2. Nájdeme xvfb-run
XVFB_PATH=$(which xvfb-run 2>/dev/null)
if [ -z "$XVFB_PATH" ]; then
    XVFB_PATH=$(find /nix/store -name xvfb-run -type f -executable -print -quit 2>/dev/null)
fi
echo "XVFB_PATH=$XVFB_PATH"
export XVFB_PATH="$XVFB_PATH"

echo "--- RUNTIME BINARY DISCOVERY END ---"

# Spustíme gunicorn
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120
