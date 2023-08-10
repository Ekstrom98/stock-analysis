import streamlit as st
import pandas as pd
import pandasql as ps
# python -m streamlit run streamlit_app.py

st.set_page_config(
    page_title="Stock Analysis",
    page_icon="💰",
    layout="centered",
)

st.title("Stock Analysis")
st.markdown("---")
company_data = pd.read_csv('./backups/company_data.csv',usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], header=None)
company_data.columns = ['id', 'company_name', 'company_symbol', 'industry', 'sector', 'full_time_employees',
                        'return_on_assets', 'return_on_equity', 'market_cap', 'current_price', 'trailing_eps', 'current_pe']
#option = st.selectbox("Choose an option:", ["Show All", "Filter Data"], index=0)
option = st.radio("Choose an option:", ["Show All", "Filter Data"], index=0)
company_name = st.text_input("Search for stock (leave it blank to view all available stocks)")
if option == "Filter Data":

    roa = st.number_input('Exclude all stocks with an ROA [%] lower than:', value=0.0, format="%.1f", step=1.0)/100
    pe = st.number_input('Exclude all stocks with a P/E lower than:', value=0.0, format="%.1f", step=0.1)


    query = \
    f"""
    WITH name_screening AS
    (
    SELECT * 
    FROM company_data
    WHERE LOWER(company_name) LIKE LOWER('%{company_name}%')
    ),
    roa_screening AS 
    (
    SELECT * 
    FROM name_screening 
    WHERE return_on_assets >= {roa}
    )
    SELECT company_name Name, company_symbol Symbol, sector Sector, ROUND(return_on_assets*100,1) ROA, ROUND(current_pe,1) PE, market_cap 'Market Cap'
    FROM roa_screening
    WHERE current_pe >= {pe}
    ORDER BY current_pe;
    """

    result = ps.sqldf(query, locals())

    st.dataframe(result)
else:
    query = \
    f"""
    SELECT company_name Name, company_symbol Symbol, sector Sector, ROUND(return_on_assets*100,1) ROA, ROUND(current_pe,1) PE, market_cap 'Market Cap'
    FROM company_data
    WHERE LOWER(company_name) LIKE LOWER('%{company_name}%')
    ORDER BY company_name;
    """

    result = ps.sqldf(query, locals())

    st.dataframe(result)