from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer#, TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import pandas as pd

def generate_report(df: pd.DataFrame, filename: str):

    # Create a new document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = TA_CENTER  # Set the alignment to center
    desc_style = styles['BodyText']

    # Title
    title = Paragraph("Magic Stock Analysis", title_style)
    story.append(title)
    story.append(Spacer(1, 12))

    # Description
    description = Paragraph("Your description paragraph here...", desc_style)
    story.append(description)
    story.append(Spacer(1, 12))

    # Table (Assuming df is your DataFrame)
    data = [df.columns.tolist()] + df.values.tolist()
    table = Table(data)
    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#E5E4E2')])
    table.setStyle(table_style)
    story.append(table)
    story.append(Spacer(1, 12))

    # Summary
    summary = Paragraph("Your summary content here...", desc_style)
    story.append(summary)

    # Table of Contents
    #toc = TableOfContents()
    #toc.levelStyles = [
    #     ParagraphStyle(fontName='Times-Bold', fontSize=14, name='TOCHeading1', leftIndent=20),
    #     ParagraphStyle(fontSize=12, name='TOCHeading2', leftIndent=40)
    # ]

    #story.append(toc)

    # Build the PDF
    doc.build(story)

# Example usage
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'San Francisco', 'Los Angeles']
})

generate_report(df, "magic_stock_analysis.pdf")