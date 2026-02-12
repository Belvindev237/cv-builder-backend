from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # HTML ultra simple
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body { 
                background: red; 
                color: white; 
                padding: 50px;
                font-size: 30px;
            }
        </style>
    </head>
    <body>
        <h1>TEST PDF</h1>
        <p>Si vous voyez ceci, Playwright fonctionne!</p>
    </body>
    </html>
    """
    
    page.set_content(html)
    page.wait_for_timeout(1000)
    
    pdf_bytes = page.pdf(
        format='A4',
        print_background=True
    )
    
    with open('test_simple.pdf', 'wb') as f:
        f.write(pdf_bytes)
    
    browser.close()
    
    print(f"✅ PDF créé : {len(pdf_bytes)} octets")
    print("📄 Fichier : test_simple.pdf")