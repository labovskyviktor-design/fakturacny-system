# Playwright PDF Generation - Deployment Summary

## What Changed

### Complete replacement of WeasyPrint with Playwright

**Why:** After 20+ failed attempts with WeasyPrint, wkhtmltopdf, xhtml2pdf, and pdfkit - all failing on Railway's Nix environment library issues - we switched to **Playwright** which bundles its own Chromium browser.

## Files Modified

1. **requirements.txt** - Replaced `weasyprint` with `playwright>=1.40.0`
2. **nixpacks.toml** - Removed all system library dependencies, added `playwright install --with-deps chromium`
3. **app.py** - Rewrote `_get_invoice_pdf_data()` to use Playwright instead of WeasyPrint

## How It Works

Playwright launches a headless Chromium browser, renders the HTML template, and generates PDF using Chrome's native print engine. This avoids all system library issues because:
- ✅ Chromium is bundled with Playwright
- ✅ No dependency on system libraries (Cairo, Pango, GObject, etc.)
- ✅ Perfect HTML/CSS rendering
- ✅ Works identically on all platforms

## Deployment Status

Changes pushed to Railway. Build will:
1. Install Python dependencies including Playwright
2. Run `playwright install --with-deps chromium` to download Chromium (~200MB)
3. Start application with Gunicorn

## Testing After Deployment

1. **Check Railway logs** for successful Chromium installation
2. **Generate PDF** from any invoice
3. **Verify** Slovak diacritics render correctly
4. **Confirm** A4 portrait format

## Expected Result

✅ PDF generation works on Railway
✅ No more "libgobject-2.0-0 not found" errors
✅ Slovak characters render perfectly
✅ QR codes visible
✅ Professional PDF output

## If It Still Fails

Check Railway logs for:
- Chromium installation errors
- Memory issues (Chromium needs ~200MB RAM)
- Timeout errors (increase gunicorn timeout if needed)

This solution **should work** because Playwright is designed for exactly this use case and is widely used in production environments including Railway.
