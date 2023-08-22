import pandas as pd
import pandasql as ps
def compute_ema(data, smoothing_factor, days_back):
    alpha = smoothing_factor/ (days_back + 1)
    ema = [round(data[0], 6)]
    for i in range(1, len(data)):
        current_ema = round(((1 - alpha) * ema[-1] + alpha * data[i]), 2)
        ema.append(current_ema)
    return ema

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

def filter_dataframe_based_on_selections(df: pd.DataFrame, magic_option: str, company_name: str) -> pd.DataFrame:
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