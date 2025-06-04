from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_invoice_pdf(invoice_data, pdf_filename):
    """Generate a PDF for the given invoice data."""
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Add header
    elements.append(Paragraph("INVOICE", styles['Title']))
    elements.append(Paragraph(f"Invoice ID: {invoice_data['invoice_id']}", styles['Heading2']))
    elements.append(Paragraph("Billing Management System", styles['Heading3']))
    elements.append(Paragraph("123 Business Street, City, Country", styles['Normal']))
    elements.append(Paragraph("Phone: +1-234-567-8900 | Email: billing@example.com", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Add customer details
    elements.append(Paragraph("Bill To:", styles['Heading3']))
    elements.append(Paragraph(f"Customer Name: {invoice_data['customer_name']}", styles['Normal']))
    elements.append(Paragraph(f"Customer Phone: {invoice_data['customer_phone']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Add table header and rows
    data = [["Product", "Price (Rs.)", "Quantity", "Total (Rs.)"]]
    for item in invoice_data['items']:
        data.append([item['name'], f"{item['price']:.2f}", item['quantity'], f"{item['total_price']:.2f}"])
    data.append(["", "", "Total Amount", f"Rs.{invoice_data['total_amount']:.2f}"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    # Add footer
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Thank you for your business!", styles['Normal']))
    elements.append(Paragraph("This is a computer-generated invoice and does not require a signature.", styles['Normal']))

    # Build the PDF
    doc.build(elements)
