import psycopg2, configparser
import yfinance as yf
import pandas as pd
import numpy as np

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

for symbol in df.Symbol:
    try:
        stock = yf.Ticker(symbol)
        print("Looking at " + symbol)
        try:
            company_name = stock.info['shortName']
            #if "'" in company_name:
                #company_name = company_name.replace("'","''")
                #print(company_name)
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
        
        query = """
                INSERT INTO company_data 
                (company_name, company_symbol, industry, sector, full_time_employees, return_on_assets, 
                return_on_equity, market_cap, current_price, trailing_eps, current_pe)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

        cursor.execute(query, (company_name, symbol, industry, sector, fte, return_on_assets, return_on_equity, market_cap, current_price, trailing_earnings_per_share, current_pe))
        #cursor.execute(query)
        print("Insertion of data from stock " + company_name + " completed.")
    except Exception as e:
        print("Error: " + str(e))

connection.commit()
cursor.close()
connection.close()

print("Finished.")