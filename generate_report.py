from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_CENTER
import pandas as pd
from io import BytesIO

def generate_report(df: pd.DataFrame):
    buffer = BytesIO()

    # Create a new document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
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

    # Build the PDF
    doc.build(story)
    buffer.seek(0)
    return buffer