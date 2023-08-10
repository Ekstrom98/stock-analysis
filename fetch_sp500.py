import psycopg2, configparser, requests
from bs4 import BeautifulSoup

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

sp_500 = config['STOCK INDICES']['SP500']

response = requests.get(sp_500).content
soup = BeautifulSoup(response,'html.parser')

cursor = connection.cursor()
def check_if_value_exists(company_symbol):
    query = f"SELECT COUNT(*) FROM companies WHERE company_symbol = '{company_symbol.upper()}'"
    cursor.execute(query)
    results = bool(cursor.fetchone()[0])
    return results

for i in range(503):
    row = soup.find('table', id='constituents').find_all('tr')[i+1]
    company_symbol = row.find_all('td')[0].get_text(strip=True)
    company_name = row.find_all('td')[1].get_text(strip=True)
    values = (company_name, company_symbol)

    value_already_exists = check_if_value_exists(company_symbol=company_symbol)

    if value_already_exists:
        print("The company symbol you've entered already exists in the database.")
    else:
        print("Values to be inserted: ", values)
        query = """INSERT INTO companies (company_name, company_symbol) VALUES (%s, %s);"""
   
        try:
            # Execute the query
            cursor.execute(query, (company_name, company_symbol))

            # Commit the transaction
            connection.commit()
            print("Values inserted successfully.")
        except Exception as e:
            print("Couldn't insert values. Error: " + str(e))