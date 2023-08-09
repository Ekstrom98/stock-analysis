import psycopg2, configparser

config = configparser.ConfigParser()
config.read('.cfg')

# Connect to the PostgreSQL database
connection = psycopg2.connect(
    dbname=config['POSTGRES']['POSTGRES_DB'],
    user=config['POSTGRES']['POSTGRES_USER'],
    password=config['POSTGRES']['POSTGRES_PASSWORD'],
    host=config['POSTGRES']['HOST']
)

# Create a cursor object
cursor = connection.cursor()

def check_if_value_exists(company_symbol):
    query = f"SELECT COUNT(*) FROM companies WHERE company_symbol = '{company_symbol.upper()}'"
    cursor.execute(query)
    results = bool(cursor.fetchone()[0])
    return results


if __name__=='__main__':
    try:
        while True:
            # Define the insert query with placeholders
            company_name = input("Company name: ")
            company_symbol = input("Company symbol: ")
            query = f"INSERT INTO companies (company_name, company_symbol) VALUES ('{company_name}', '{company_symbol.upper()}');"
            
            # Values to be inserted
            values = (f'{company_name}', f'{company_symbol.upper()}')
            
            value_already_exists = check_if_value_exists(company_symbol=company_symbol)
            if value_already_exists:
                print("The company symbol you've entered already exists in the database.")
            else:
                print("Values to be inserted: ", values)

                proceed = input("Do you wish to proceed (y/n)? ").strip().lower()
                if proceed == 'y':
                    # Execute the query
                    cursor.execute(query)

                    # Commit the transaction
                    connection.commit()
                    print("Values inserted successfully.")

                elif proceed == 'n':
                    print("Insertion skipped.")
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

    except KeyboardInterrupt:
        print("\nExiting the application...")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("Application closed.")


