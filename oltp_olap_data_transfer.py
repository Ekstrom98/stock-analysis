from utilities.db_utils import connect_to_database, write_all_oltp_tables_to_csv

oltp_connection = connect_to_database('oltp')
olap_connection = connect_to_database('olap')

oltp_cursor = oltp_connection.cursor()

with open('sql/get_latest_data.sql', 'r') as query:
    query = query.read()


oltp_cursor.execute(f'{query}')

rows = oltp_cursor.fetchall()

oltp_cursor.close()
oltp_connection.close()


# Connect to target database (OLAP) and insert data
olap_cursor = olap_connection.cursor()
olap_cursor.execute("""TRUNCATE TABLE stock_analytics;""")
olap_cursor.executemany("""INSERT INTO stock_analytics (fetched_at, price, ema_34, ema_200, return_on_assets, return_on_equity,
                        trailing_earnings_per_share, price_earnings_ratio, market_capitalization, name, symbol,
                        industry, sector, description) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", rows)
olap_connection.commit()

olap_cursor.close()
olap_connection.close()
print("Data has been transferred to the table 'stock_analytics'.")