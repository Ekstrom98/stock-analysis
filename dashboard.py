# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from utilities.db_utils import connect_to_database

# Connect to the PostgreSQL database
db_connection = connect_to_database('olap')

# Query the database to fetch the data
df = pd.read_sql_query("""SELECT name, symbol, industry, sector,
                       fetched_at, price, ema_34, ema_200, return_on_assets,
                       return_on_equity, trailing_earnings_per_share, price_earnings_ratio,
                       market_capitalization
                        FROM stock_analytics;""", db_connection)
db_connection.close()

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = dbc.Container([
    dcc.Markdown("# Magic Stock Analysis", style={'textAlign':'center'}),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            for i in df.columns
        ],
        data=df.to_dict('records'),  # the contents of the table
        editable=False,              # allow editing of data inside all cells
        filter_action="none",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=False,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=5,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['name', 'symbol', 'sector']
        ],
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto',
            'width': 'auto'
        }
    )
])



# Run the app
if __name__ == '__main__':
    app.run(debug=True)