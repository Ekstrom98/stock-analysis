import psycopg2, configparser, csv

def connect_to_database():
    config = configparser.ConfigParser()
    config.read('/Users/viktorekstrom/Desktop/Desktop/Projekt/stock-analysis/.cfg')
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=config['POSTGRES']['POSTGRES_DB'],
            user=config['POSTGRES']['POSTGRES_USER'],
            password=config['POSTGRES']['POSTGRES_PASSWORD'],
            host=config['POSTGRES']['HOST']
        )
        print("Connection successful.")
        return connection
    except Exception as e:
        print("Connection unsuccessful. Error: " + str(e))
        return e 
    
def check_if_symbol_exists_in_companies_table(symbol):
    query = """SELECT COUNT(*) FROM companies WHERE company_symbol = %s"""
    cursor.execute(query, (symbol))
    results = bool(cursor.fetchone()[0])
    return results

def look_up_dimension_keys_for_stock_data(cursor, stock_info: dict):
    symbol = stock_info['symbol']
    company_id_query = f"SELECT company_id FROM companies WHERE symbol = '{symbol}'"
    cursor.execute(company_id_query)
    company_id = cursor.fetchall()[0]

    try:
        industry = stock_info['industry']
        industry_id_query = f"SELECT industry_id FROM industries WHERE industry = '{industry}'"
        cursor.execute(industry_id_query)
        industry_id = cursor.fetchall()[0]
    except:
        industry_id = [None]
    
    try:
        sector = stock_info['sector']
        sector_id_query = f"SELECT sector_id FROM sectors WHERE sector = '{sector}'"
        cursor.execute(sector_id_query)
        sector_id = cursor.fetchall()[0]
    except:
        sector_id = [None]

    return company_id[0], industry_id[0], sector_id[0]

def write_all_tables_to_csv():
    connection = connect_to_database()
    cursor = connection.cursor()
    config = configparser.ConfigParser()
    config.read('/Users/viktorekstrom/Desktop/Desktop/Projekt/stock-analysis/.cfg')
    tables = ['stock_data', 'companies', 'industries', 'sectors']
    
    for table in tables:
        try:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            path = config['BACKUP'][f'{table.upper()}']
            with open(path, 'w', newline='') as csvfile:

                csv_writer = csv.writer(csvfile)
            
                # Write header (column names) to CSV
                column_names = [desc[0] for desc in cursor.description]
                csv_writer.writerow(column_names)
                
                # Write rows to CSV
                csv_writer.writerows(rows)

        except Exception as e:
            raise e
        
    connection.commit()
    cursor.close()
    connection.close()