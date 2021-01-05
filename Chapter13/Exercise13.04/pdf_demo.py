from weasyprint import HTML

def generate_pdf(url, pdf_file):
    """Generate PDF version of the provided URL."""
    print("Generating PDF...")
    HTML(url).write_pdf(pdf_file)

if __name__ == '__main__':
    url = 'http://text.npr.org'
    pdf_file = 'demo_page.pdf'
    generate_pdf(url, pdf_file)
