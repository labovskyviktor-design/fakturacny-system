#!/bin/bash
# Wrapper pre wkhtmltopdf na Railway/Headless server
# Spúšťa generátor cez virtuálnu obrazovku (Xvfb)

if command -v xvfb-run > /dev/null 2>&1; then
    xvfb-run --server-args="-screen 0 1024x768x24" wkhtmltopdf "$@"
else
    wkhtmltopdf "$@"
fi
