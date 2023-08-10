import streamlit as st
import pandas as pd
import pandasql as ps
# python -m streamlit run streamlit_app.py

def magic_formula(df: pd.DataFrame, roa_col: str, pe_col: str) -> pd.DataFrame:
    df_roa_sorted = df.sort_values(by=roa_col, ascending=True)
    df_roa_sorted.reset_index(inplace=True, drop=True)

    df_pe_sorted = df_roa_sorted.sort_values(by=pe_col, ascending=False)

    df_pe_sorted.reset_index(inplace=True, drop=False)
    df_roa_score = df_pe_sorted.rename(columns={"index": "roa_score"})

    df_pe_sorted = df_roa_score.reset_index(drop=False)
    df_pe_sorted = df_pe_sorted.rename(columns={"index": "pe_score"})
    
    df_magic = df_pe_sorted.copy()
    df_magic['Magic Score'] = df_magic['pe_score'] + df_magic['roa_score']
    df_magic = df_magic.sort_values(by='Magic Score', ascending=False)
    df_magic.dropna(inplace=True, subset=[roa_col, pe_col])
    df_magic.drop(inplace=True, columns=['pe_score', 'roa_score'])
    df_magic.reset_index(inplace=True, drop=True)
    
    return df_magic

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
col1, col2 = st.columns(2)
with col1:
    selection_option = st.radio("Choose an option:", ["Show All", "Filter Data"], index=0)
with col2:
    magic_option = st.radio("Show magic score:", ["Yes", "No"], index=1)

company_name = st.text_input("Search for stock (leave it blank to view all available stocks)")

if selection_option == "Filter Data":

    roa = st.number_input('Exclude all stocks with an ROA [%] lower than:', value=0.0, format="%.1f", step=1.0)/100
    pe = st.number_input('Exclude all stocks with a P/E lower than:', value=0.0, format="%.1f", step=0.1)

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
    if magic_option == 'Yes':
        result = magic_formula(df = result, roa_col = 'ROA', pe_col = 'PE')

    if company_name != '':
        name_query = \
                f"""
                SELECT Name, Symbol, Sector, ROA, PE, "Magic Score"
                FROM result
                WHERE LOWER(Name) LIKE LOWER('%{company_name}%')
                ORDER BY "Magic Score" DESC;
                """
        result = ps.sqldf(name_query, locals())

    st.dataframe(result)
else:
    
    query = \
    f"""
    SELECT company_name Name, company_symbol Symbol, sector Sector, ROUND(return_on_assets*100,1) ROA, ROUND(current_pe,1) PE
    FROM company_data
    ORDER BY company_name;
    """

    result = ps.sqldf(query, locals())

    if magic_option == 'Yes':
        result = magic_formula(df = result, roa_col = 'ROA', pe_col = 'PE')
    if company_name != '':
        name_query = \
                f"""
                SELECT Name, Symbol, Sector, ROA, PE, "Magic Score"
                FROM result
                WHERE LOWER(Name) LIKE LOWER('%{company_name}%')
                ORDER BY "Magic Score" DESC;
                """
        result = ps.sqldf(name_query, locals())
    st.dataframe(result)

st.markdown("---")