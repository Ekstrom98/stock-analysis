import configparser, requests
from bs4 import BeautifulSoup
from utilities.db_utils import connect_to_database, check_if_symbol_exists_in_companies_table

connection = connect_to_database()

sp_500 = config['STOCK INDICES']['SP500']

response = requests.get(sp_500).content
soup = BeautifulSoup(response,'html.parser')

cursor = connection.cursor()

for i in range(503):
    row = soup.find('table', id='constituents').find_all('tr')[i+1]
    symbol = row.find_all('td')[0].get_text(strip=True)
    name = row.find_all('td')[1].get_text(strip=True)
    values = (name, company_symbol)

    value_already_exists = check_if_symbol_exists_in_companies_table(symbol=symbol)

    if value_already_exists:
        print("The company symbol you've entered already exists in the database.")
    else:
        print("Values to be inserted: ", values)
        query = """INSERT INTO companies (name, symbol) VALUES (%s, %s);"""
   
        try:
            # Execute the query
            cursor.execute(query, (name, symbol))

            # Commit the transaction
            connection.commit()
            print("Values inserted successfully.")
        except Exception as e:
            print("Couldn't insert values. Error: " + str(e))