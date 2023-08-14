import psycopg2, configparser
import yfinance as yf
import pandas as pd
import numpy as np
import subprocess

config = configparser.ConfigParser()
config.read('.cfg')
try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        dbname=config['POSTGRES']['POSTGRES_DB'],
        user=config['POSTGRES']['POSTGRES_USER'],
        password=config['POSTGRES']['POSTGRES_PASSWORD'],
        host=config['POSTGRES']['HOST']
    )
    print("Connection successful.")
except Exception as e:
    print("Connection unsuccessful. Error: " + str(e))

cursor = connection.cursor()

df = pd.read_csv("backups/companies.csv",usecols=[0, 1, 2], header=None)
df.columns = ['ID', 'Company Name', 'Symbol']

def check_if_value_exists(company_symbol):
    query = """SELECT COUNT(*) FROM companies WHERE company_symbol = %s"""
    cursor.execute(query, (company_symbol))
    results = bool(cursor.fetchone()[0])
    return results

truncate_query = """TRUNCATE TABLE company_data"""
cursor.execute(truncate_query)
connection.commit()
symbol_errors = []
for symbol in df.Symbol:
    try:
        stock = yf.Ticker(symbol)
        print("Looking at " + symbol)
        try:
            company_name = stock.info['shortName']
        except:
            company_name = None
        
        try:
            symbol = stock.info['symbol']
        except:
            symbol = None

        try:
            industry = stock.info['industry']
        except:
            industry = None
        
        try:
            sector = stock.info['sector']
        except:
            sector = None
        
        try:
            fte = stock.info['fullTimeEmployees']
        except:
            fte = None

        try:
            return_on_assets = stock.info['returnOnAssets']
        except:
            return_on_assets = None
        
        try:
            return_on_equity = stock.info['returnOnEquity']
        except:
            return_on_equity = None
        
        try:
            market_cap = stock.info['marketCap']
        except:
            market_cap = None
        
        try:
            current_price = stock.info['currentPrice']
        except:
            current_price = None
        
        try:
            trailing_earnings_per_share = stock.info['trailingEps']
        except:
            trailing_earnings_per_share = None
        
        try:
            current_pe = current_price/trailing_earnings_per_share
        except:
            current_pe = None
        
        try:
            business_summary = stock.info['longBusinessSummary']
        except:
            business_summary = None
        
        query = """
                INSERT INTO company_data 
                (company_name, company_symbol, industry, sector, full_time_employees, return_on_assets, 
                return_on_equity, market_cap, current_price, trailing_eps, current_pe, business_summary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

        cursor.execute(query, (company_name, symbol, industry, sector, fte, return_on_assets, return_on_equity, market_cap, current_price, trailing_earnings_per_share, current_pe, business_summary))
        
        print("Insertion of data from stock " + company_name + " completed.")
    except Exception as e:
        symbol_errors.append(symbol)
        print("Error: " + str(e))

connection.commit()
cursor.close()
connection.close()

subprocess.run(['python3', 'backup_data.py'], check=True)

print("Finished.")