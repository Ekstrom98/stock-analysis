import subprocess, configparser
def backup_data():
        config = configparser.ConfigParser()
        config.read('.cfg')
        POSTGRES_USER = config['POSTGRES']['POSTGRES_USER']
        POSTGRES_PASSWORD = config['POSTGRES']['POSTGRES_PASSWORD']
        HOST = config['POSTGRES']['HOST']
        PORT = config['POSTGRES']['PORT']
        POSTGRES_DB = config['POSTGRES']['POSTGRES_DB']
        connection_str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{POSTGRES_DB}"
        
        with open('./sql/backup_data.sql', 'r') as file:
            sql_commands = file.read().split(';')

        for command in sql_commands:
            
            try:
                if command.strip() != '':
                    table = command.split(' ')[1]
                    print(f"Copying table {table}...")
                    backup_path = config['BACKUP'][f'{table.upper()}']
                    command = command.format(path=backup_path)
                  
                    result = subprocess.run(['psql', connection_str], input=command.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    if result.returncode != 0:
                        print(f"Command failed: {result.stderr.decode()}")
                    else:
                        print(f"The table {table} has been successfully copied.")
                        print("Number of records copied:")
                        print(result.stdout.decode().split('COPY ')[1])

            except Exception as e:
                 print(f"Command skipped: {str(e)}")
backup_data()