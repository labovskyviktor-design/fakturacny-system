# PDF Generation Fix - Deployment Instructions

## Changes Made

### 1. Enhanced System Dependencies
**File:** `nixpacks.toml`
- Added `freetype` for font rendering
- Added `liberation_ttf` for additional font support
- Added `xorg.libX11` and `xorg.libXrender` for X11 rendering support

### 2. PDF Diagnostics Utility
**File:** `utils/pdf_diagnostics.py`
- Verifies WeasyPrint availability
- Checks system library availability (Cairo, Pango, etc.)
- Tests font availability for Slovak characters
- Validates environment variables
- Performs test PDF generation

### 3. Enhanced Error Logging
**File:** `app.py` - Function `_get_invoice_pdf_data()`
- Added pre-flight environment diagnostics
- Comprehensive error logging with full tracebacks
- Specific error type identification (Cairo, Pango, font issues)
- Environment variable logging for debugging

### 4. Diagnostic Script
**File:** `check_pdf_env.py`
- Standalone script to verify PDF environment
- Can be run on Railway to diagnose issues

---

## Deployment Steps

### 1. Commit and Push Changes

```bash
git add .
git commit -m "Fix: Enhanced PDF generation with better diagnostics and dependencies"
git push origin main
```

### 2. Railway Deployment

Railway will automatically detect the changes and rebuild with the new `nixpacks.toml` configuration.

**Monitor the build logs for:**
- Successful installation of new Nix packages
- No errors during dependency resolution

### 3. Post-Deployment Verification

#### A. Check Diagnostic Endpoint

Access: `https://your-railway-app.railway.app/debug/pdf-test`

**Expected Output:**
- All libraries show "FOUND and LOADED ✓"
- Nix library folder exists
- Sample .so files are listed

#### B. Test Direct PDF Generation

Access: `https://your-railway-app.railway.app/test-direct-pdf`

**Expected Result:**
- Browser downloads a PDF file (not HTML)
- PDF contains "SUCCESS: WeasyPrint is working!"

#### C. Test Invoice PDF Generation

1. Log in to your Railway deployment
2. Navigate to an existing invoice or create a new one
3. Click "Stiahnuť PDF" (Download PDF)

**Verify:**
- ✓ File downloads as `.pdf` (not `.html`)
- ✓ No warning flash message about HTML fallback
- ✓ PDF opens correctly in PDF viewer
- ✓ Slovak diacritics render properly (á, č, ď, é, í, ľ, ň, ó, ŕ, š, ť, ú, ý, ž)
- ✓ A4 portrait format is maintained
- ✓ QR code is visible (if payment method is bank transfer)

### 4. Check Railway Logs

If PDF generation still fails, check the Railway logs for detailed error messages:

```bash
# In Railway dashboard, go to Deployments → View Logs
```

**Look for:**
- Lines starting with `===` (diagnostic output)
- `Starting PDF generation for invoice...`
- `PDF environment check passed ✓` or error messages
- Specific library errors (Cairo, Pango, font issues)

---

## Troubleshooting

### If PDF Generation Still Fails

#### 1. Run Diagnostic Script on Railway

SSH into Railway container (if available) or add a temporary route:

```python
@app.route('/run-diagnostics')
@login_required
def run_diagnostics():
    from utils.pdf_diagnostics import log_diagnostics
    success, diag = log_diagnostics()
    return jsonify(diag)
```

#### 2. Check for Missing Libraries

Look in logs for messages like:
- `Library cairo not found`
- `Library pango-1.0 not found`
- `Font check failed`

**Solution:** Verify `nixpacks.toml` was properly deployed

#### 3. Font Issues

If Slovak characters don't render:
- Check logs for "DejaVu Sans font not found"
- Verify `dejavu_fonts` and `liberation_ttf` are in nixpacks.toml

#### 4. Environment Variables

Ensure these are set in Railway:
- `LD_LIBRARY_PATH` (set automatically by nixpacks)
- `FONTCONFIG_FILE` (set automatically by nixpacks)

---

## Local Testing (Optional)

Before deploying to Railway, you can test locally:

### 1. Run Diagnostic Script

```bash
python check_pdf_env.py
```

**Expected:** All checks pass

### 2. Test PDF Generation

```bash
python app.py
# Open http://localhost:5000
# Create/view invoice and download PDF
```

---

## Success Criteria

✅ **PDF generation works on Railway**
✅ **Slovak diacritics render correctly**
✅ **A4 portrait format is maintained**
✅ **QR codes are visible**
✅ **No HTML fallback warnings**

---

## Rollback Plan

If issues persist, you can rollback:

```bash
git revert HEAD
git push origin main
```

Then investigate further using the diagnostic tools provided.
