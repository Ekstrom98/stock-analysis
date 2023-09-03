# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
from utilities.db_utils import connect_to_database

# Incorporate data
#df = pd.read_csv('backups/stock_analytics.csv')

# Connect to the PostgreSQL database
db_connection = connect_to_database('olap')

# Query the database to fetch the data
df = pd.read_sql_query("SELECT * FROM stock_analytics LIMIT 10;", db_connection)
db_connection.close()

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)