"""
File: stock_dash.py
Description: A dashboard that visualizes changes in stocks
"""

from stocks_api import StocksAPI
import stock_graph as sg
from dash import Dash, dcc, html, Input, Output


def main():
    api = StocksAPI('MAANG-data')
    min_date = api.get_extreme_date(earliest=True)
    max_date = api.get_extreme_date(earliest=False)

    # create the dash app
    app = Dash(__name__)

    # create the layout
    app.layout = html.Div([
        html.H4('Stock Data Interactive Dashboard'),
        dcc.Graph(id="graph", style={'width': '100vw', 'height': '90vh'}),

        html.P("Select Stock:"),
        dcc.Checklist(id='stock_name', options=api.get_stock_list(), value=[api.get_stock_list()[0]], inline=True),

        html.P("Select Information to Display:"),
        dcc.RadioItems(id='stock_info', options=[
            {'label': 'Open Price', 'value': 'Open'},
            {'label': 'Close Price', 'value': 'Close'},
            {'label': 'Adjusted Close', 'value': 'Adj Close'},
            {'label': 'Volume Traded', 'value': 'Volume'}
        ], value='Close', inline=True),

        html.P("Select Date Range"),
        dcc.DatePickerRange(id='date_range', min_date_allowed=min_date, max_date_allowed=max_date, start_date=min_date,
                            end_date=max_date)
    ])

    @app.callback(
        Output("graph", "figure"),
        Input("stock_name", "value"),
        Input("stock_info", "value"),
        Input('date_range', 'start_date'),
        Input('date_range', 'end_date')
    )
    def display_stock_graph(stock_name, stock_info, start_date, end_date):
        # get only YYYY-MM-DD from date
        start_date = start_date[0:10]
        end_date = end_date[0:10]

        # get dataframe and then trim data
        stocks_df = api.total_stocks_df
        stock_data = StocksAPI.trim_data(df=stocks_df, stock_name=stock_name, start_date=start_date, end_date=end_date)

        fig = sg.generate_stock_line_graph(stock_data=stock_data, stock_info=stock_info,
                                           stock_name=stock_name)
        return fig

    app.run_server(debug=True)


main()
