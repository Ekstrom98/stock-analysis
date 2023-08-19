import streamlit as st
import pandas as pd
import pandasql as ps
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from utilities.stock_utils import magic_formula, filter_dataframe_based_on_selections()

# Streamlit app configuration
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="💰",
    layout="centered",
)

# App title and separator
st.title("Stock Analysis")
st.markdown("---")

# Read the data into a DataFrame
company_data = pd.read_csv('./backups/company_data.csv',usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], header=None)
company_data.columns = ['id', 'company_name', 'company_symbol', 'industry', 'sector', 'full_time_employees',
                        'return_on_assets', 'return_on_equity', 'market_cap', 'current_price', 'trailing_eps',
                        'current_pe', 'business_summary']

# Radio buttons for user options
col1, col2 = st.columns(2)
with col1:
    selection_option = st.radio("Choose an option:", ["Show All", "Filter Data"], index=0)
with col2:
    magic_option = st.radio("Show magic score:", ["Yes", "No"], index=1)

# Input for stock search
company_name = st.text_input("Search for stock (leave it blank to view all available stocks)")

# If the user choose to filter the data, enable some more options.
if selection_option == "Filter Data":

    # Input fields for filtering criteria
    roa = st.number_input('Exclude all stocks with an ROA [%] lower than:', value=0.0, format="%.1f", step=1.0)/100
    pe = st.number_input('Exclude all stocks with a P/E lower than:', value=0.0, format="%.1f", step=0.1)
   
    # SQL query to filter stocks based on ROA and P/E ratio
    query = \
    f"""
    WITH roa_screening AS 
    (
    SELECT * 
    FROM company_data 
    WHERE return_on_assets >= {roa}
    )
    SELECT company_name Name, company_symbol Symbol, sector Sector, ROUND(return_on_assets*100, 1) ROA, ROUND(current_pe,1) PE
    FROM roa_screening
    WHERE current_pe >= {pe}
    ORDER BY current_pe;
    """
    result = ps.sqldf(query, locals())
    result = filter_dataframe_based_on_selections(result, magic_option, company_name)
    
    st.dataframe(result)

else: 
    # If the user decides to not filter the data, we can use a different SQL query.
    query = \
    f"""
    SELECT company_name Name, company_symbol Symbol, sector Sector, ROUND(return_on_assets*100,1) ROA, ROUND(current_pe,1) PE
    FROM company_data
    ORDER BY company_name;
    """

    result = ps.sqldf(query, locals())
    result = filter_dataframe_based_on_selections(result, magic_option, company_name)
    st.dataframe(result)
st.write(f"Based on your current selections, there are {len(result)} results.")

#--------------------------------------GENERATE REPORT--------------------------------------#
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
if selection_option == 'Show All':
    if magic_option == 'Yes':
        desc = f"This report is based on your selection to show all records and include a magic score.\
                Below you'll find a table with {len(result)} records ordered by their magic score in descending order."
    else:
        desc = f"This report is based on your selection to show all records and not include a magic score.\
                Below you'll find a table with {len(result)} records ordered by their magic score in descending order."
else:
    if magic_option == 'Yes':
        desc = f"This report is based on your selection to filter records and include a magic score.\
                Below you'll find a table with {len(result)} records ordered by their magic score in descending order. \
                Based on your applied filters, only records with a return on assets greater than or equal to {roa*100}% \
                and a P/E-ratio greater than or equal to {pe} are included."
    else:
        desc = f"This report is based on your selection to show all records and not include a magic score.\
                elow you'll find a table with {len(result)} records ordered by their magic score in descending order. \
                Based on your applied filters, only records with a return on assets greater than or equal to {roa*100}% \
                and a P/E-ratio greater than or equal to {pe} are included."

description = Paragraph(desc, desc_style)
story.append(description)
story.append(Spacer(1, 12))

# Table
data = [result.columns.tolist()] + result.values.tolist()
table = Table(data)
table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#E5E4E2')])
table.setStyle(table_style)
story.append(table)
story.append(Spacer(1, 12))

# Build the PDF
doc.build(story)
buffer.seek(0)


st.download_button(
    label="Generate Report",
    data=buffer,
    file_name="magic_stock_analysis.pdf",
    mime="application/pdf"
)

st.markdown("---")