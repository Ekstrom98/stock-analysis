import yfinance as yf
import pandas as pd 
import numpy as np
from utilities.db_utils import connect_to_database, look_up_dimension_keys_for_stock_data
from utilities.stock_utils import compute_ema

connection = connect_to_database()
cursor = connection.cursor()

# Execute a SELECT query on the desired column
cursor.execute("SELECT symbol FROM companies;")

# Fetch all rows from the result
symbols = cursor.fetchall()

for symbol in symbols:
    symbol = symbol[0]
    try:
        stock = yf.Ticker(symbol).info
        stock_history = yf.Ticker(symbol).history(period='max')
        historical_data = np.array(stock_history.Close)
        print("Looking at " + symbol)

        company_id, industry_id, sector_id = look_up_dimension_keys_for_stock_data(cursor, stock_info=stock)

        try:
            return_on_assets = stock['returnOnAssets']
        except:
            return_on_assets = None
        
        try:
            return_on_equity = stock['returnOnEquity']
        except:
            return_on_equity = None
        
        try:
            market_capitalization = stock['marketCap']
        except:
            market_capitalization = None
        
        try:
            price = stock['currentPrice']
        except:
            price = None
        
        try:
            ema_34 = compute_ema(data=historical_data, smoothing_factor=2, days_back=34)[-1]
        except:
            ema_34 = None

        try:
            ema_200 = compute_ema(data=historical_data, smoothing_factor=2, days_back=200)[-1]
        except:
            ema_200 = None

        try:
            trailing_earnings_per_share = stock['trailingEps']
        except:
            trailing_earnings_per_share = None
        
        try:
            price_earnings_ratio = round(price/trailing_earnings_per_share, 2)
        except:
            price_earnings_ratio = None

        
        query = """
                INSERT INTO stock_data 
                (price, ema_34, ema_200, return_on_assets, 
                return_on_equity, trailing_earnings_per_share,
                price_earnings_ratio, market_capitalization,
                company_id, industry_id, sector_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

        cursor.execute(query, (price, ema_34, ema_200, return_on_assets, return_on_equity, 
                               trailing_earnings_per_share, price_earnings_ratio, 
                               market_capitalization, company_id, industry_id, sector_id))
        
        print(f"Insertion of data from stock {symbol} completed.")
    except Exception as e:
        print("Error inserting data.")
        raise e

connection.commit()

cursor.close()
connection.close()
print("Insertion complete.")