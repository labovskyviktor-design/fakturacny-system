"""
PDF Generation Diagnostics Utility

This module provides diagnostic functions to verify that the PDF generation
environment is properly configured with all necessary dependencies.
"""
import logging
import os
import sys

logger = logging.getLogger(__name__)


def verify_pdf_environment():
    """
    Verify that all PDF generation prerequisites are met.
    
    Returns:
        tuple: (success: bool, diagnostics: dict)
    """
    diagnostics = {
        'weasyprint_available': False,
        'libraries_available': {},
        'fonts_available': {},
        'environment_vars': {},
        'errors': []
    }
    
    # Check WeasyPrint import
    try:
        import weasyprint
        diagnostics['weasyprint_available'] = True
        diagnostics['weasyprint_version'] = weasyprint.__version__
    except ImportError as e:
        diagnostics['errors'].append(f"WeasyPrint import failed: {str(e)}")
    except Exception as e:
        diagnostics['errors'].append(f"WeasyPrint error: {str(e)}")
    
    # Check system libraries using ctypes
    try:
        import ctypes
        from ctypes.util import find_library
        
        libs_to_check = ['cairo', 'pango-1.0', 'gobject-2.0', 'gdk_pixbuf-2.0', 'ffi', 'fontconfig']
        for lib in libs_to_check:
            try:
                found = find_library(lib)
                if found:
                    # Try to load it
                    ctypes.CDLL(found)
                    diagnostics['libraries_available'][lib] = f"✓ {found}"
                else:
                    diagnostics['libraries_available'][lib] = "✗ NOT FOUND"
                    diagnostics['errors'].append(f"Library {lib} not found")
            except Exception as e:
                diagnostics['libraries_available'][lib] = f"✗ LOAD ERROR: {str(e)}"
                diagnostics['errors'].append(f"Library {lib} load error: {str(e)}")
    except Exception as e:
        diagnostics['errors'].append(f"Library check failed: {str(e)}")
    
    # Check font availability
    try:
        import subprocess
        result = subprocess.run(['fc-list', ':lang=sk'], capture_output=True, text=True, timeout=5)
        slovak_fonts = result.stdout.strip().split('\n') if result.returncode == 0 else []
        diagnostics['fonts_available']['slovak_fonts_count'] = len([f for f in slovak_fonts if f])
        
        # Check for DejaVu Sans specifically
        dejavu_fonts = [f for f in slovak_fonts if 'DejaVu Sans' in f]
        diagnostics['fonts_available']['dejavu_sans'] = '✓' if dejavu_fonts else '✗'
        
        if not dejavu_fonts:
            diagnostics['errors'].append("DejaVu Sans font not found for Slovak characters")
    except FileNotFoundError:
        diagnostics['fonts_available']['fontconfig'] = '✗ fc-list not available'
    except Exception as e:
        diagnostics['errors'].append(f"Font check failed: {str(e)}")
    
    # Check environment variables
    env_vars = ['LD_LIBRARY_PATH', 'FONTCONFIG_FILE', 'FONTCONFIG_PATH', 'XDG_DATA_DIRS']
    for var in env_vars:
        diagnostics['environment_vars'][var] = os.environ.get(var, 'NOT SET')
    
    # Test simple PDF generation
    if diagnostics['weasyprint_available']:
        try:
            from weasyprint import HTML
            import io
            
            test_html = """
            <!DOCTYPE html>
            <html>
            <head><meta charset="UTF-8"></head>
            <body style="font-family: 'DejaVu Sans', Arial, sans-serif;">
                <h1>Test PDF</h1>
                <p>Slovak characters: á č ď é í ľ ň ó ŕ š ť ú ý ž</p>
                <p>ÁČĎÉÍĽŇÓŔŠŤÚÝŽ</p>
            </body>
            </html>
            """
            
            pdf_file = io.BytesIO()
            HTML(string=test_html).write_pdf(pdf_file)
            pdf_data = pdf_file.getvalue()
            
            if len(pdf_data) > 0:
                diagnostics['test_pdf_generation'] = f"✓ Generated {len(pdf_data)} bytes"
            else:
                diagnostics['test_pdf_generation'] = "✗ Empty PDF generated"
                diagnostics['errors'].append("Test PDF generation produced empty file")
                
        except Exception as e:
            diagnostics['test_pdf_generation'] = f"✗ FAILED: {str(e)}"
            diagnostics['errors'].append(f"Test PDF generation failed: {str(e)}")
    
    success = diagnostics['weasyprint_available'] and len(diagnostics['errors']) == 0
    return success, diagnostics


def log_diagnostics():
    """
    Run diagnostics and log the results.
    """
    success, diag = verify_pdf_environment()
    
    logger.info("=" * 60)
    logger.info("PDF GENERATION DIAGNOSTICS")
    logger.info("=" * 60)
    
    logger.info(f"WeasyPrint Available: {diag.get('weasyprint_available', False)}")
    if 'weasyprint_version' in diag:
        logger.info(f"WeasyPrint Version: {diag['weasyprint_version']}")
    
    logger.info("\nSystem Libraries:")
    for lib, status in diag.get('libraries_available', {}).items():
        logger.info(f"  {lib}: {status}")
    
    logger.info("\nFonts:")
    for font, status in diag.get('fonts_available', {}).items():
        logger.info(f"  {font}: {status}")
    
    logger.info("\nEnvironment Variables:")
    for var, value in diag.get('environment_vars', {}).items():
        logger.info(f"  {var}: {value}")
    
    if 'test_pdf_generation' in diag:
        logger.info(f"\nTest PDF Generation: {diag['test_pdf_generation']}")
    
    if diag.get('errors'):
        logger.error("\nERRORS:")
        for error in diag['errors']:
            logger.error(f"  - {error}")
    
    logger.info("=" * 60)
    logger.info(f"Overall Status: {'✓ PASS' if success else '✗ FAIL'}")
    logger.info("=" * 60)
    
    return success, diag


if __name__ == '__main__':
    # Allow running as standalone script
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    success, diag = log_diagnostics()
    sys.exit(0 if success else 1)
