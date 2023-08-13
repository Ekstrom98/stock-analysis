import streamlit as st
import pandas as pd
import pandasql as ps
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO

# Function to calculate the magic score for stocks based on ROA and P/E ratio
def magic_formula(df: pd.DataFrame, roa_col: str, pe_col: str) -> pd.DataFrame:
    # Drop rows with missing ROA or P/E values
    df.dropna(inplace=True, subset=[roa_col, pe_col])
    
    # Sort dataframe based on ROA values
    df_roa_sorted = df.sort_values(by=roa_col, ascending=True)
    df_roa_sorted.reset_index(inplace=True, drop=True)

    # Sort previously sorted dataframe based on P/E values
    df_pe_sorted = df_roa_sorted.sort_values(by=pe_col, ascending=False)
    df_pe_sorted.reset_index(inplace=True, drop=False)
    
    # Renaming columns to store scores
    df_roa_score = df_pe_sorted.rename(columns={"index": "roa_score"})
    df_pe_sorted = df_roa_score.reset_index(drop=False)
    df_pe_sorted = df_pe_sorted.rename(columns={"index": "pe_score"})
    
    # Calculate Magic Score as the sum of roa_score and pe_score
    df_magic = df_pe_sorted.copy()
    df_magic['Magic Score'] = df_magic['pe_score'] + df_magic['roa_score']
    df_magic = df_magic.sort_values(by='Magic Score', ascending=False)
    
    # Drop unnecessary columns and reset index
    df_magic.drop(inplace=True, columns=['pe_score', 'roa_score'])
    df_magic.reset_index(inplace=True, drop=True)
    
    return df_magic

def query_gen(df: pd.DataFrame, magic_option: str, company_name: str) -> pd.DataFrame:
    # Check if user wants to see the magic score. If yes, then calculate and display the magic score.
    if magic_option == 'Yes':
        df = magic_formula(df, roa_col = 'ROA', pe_col = 'PE')
        # Enable the user to search for specific stocks
        if company_name != '':
            name_query = \
                    f"""
                    SELECT Name, Symbol, Sector, ROA, PE, "Magic Score"
                    FROM df
                    WHERE LOWER(Name) LIKE LOWER('%{company_name}%')
                    ORDER BY "Magic Score" DESC;
                    """
        else:
            # If the user doesn't search for a specific stock, disregard the WHERE clause.
            name_query = \
                    f"""
                    SELECT Name, Symbol, Sector, ROA, PE, "Magic Score"
                    FROM df
                    ORDER BY "Magic Score" DESC;
                    """
    else:
        if company_name != '':
            name_query = \
                    f"""
                    SELECT Name, Symbol, Sector, ROA, PE
                    FROM df
                    WHERE LOWER(Name) LIKE LOWER('%{company_name}%')
                    ORDER BY Name;
                    """
        else:
            name_query = \
                    f"""
                    SELECT Name, Symbol, Sector, ROA, PE
                    FROM df
                    ORDER BY Name;
                    """
    
    # Create and display the report in Streamlit
    result = ps.sqldf(name_query, locals())
    return result

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
    result = query_gen(result, magic_option, company_name)
    
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
    result = query_gen(result, magic_option, company_name)
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