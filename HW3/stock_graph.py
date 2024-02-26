"""
File: stock_graph.py
Description: Provide a function to make the linegraph showing stock changes
"""

import plotly.graph_objs as go


def _create_trace(data, stock_info, stock_name):
    """
    Helper function to create the plotly trace object
    :param data: stock information dataframe
    :param stock_info: info to display
    :param stock_name: name of the stock
    :return trace: plotly trace object
    """
    trace = go.Scatter(x=data['Date'], y=data[stock_info], mode='lines', name=f'{stock_name} - {stock_info}')

    return trace


def generate_stock_line_graph(stock_data, stock_name, stock_info):
    """
    Generate line graph showing stock changes based on API data and Dash inputs
    :param stock_data: DataFrame containing stock data
    :param stock_name: Name of the stock
    :param stock_info: Type of stock information to display (Open, Close, Adj Close, Volume)
    :return: Plotly figure object
    """

    fig = go.Figure()

    # Iterate over each selected stock name
    for name in stock_name:
        # Filter the stock data for the current stock name
        filtered_data = stock_data[stock_data['Stock_Name'] == name]

        # Create a trace for the current stock data
        trace = _create_trace(filtered_data, stock_info, name)

        # Add the trace to the figure
        fig.add_trace(trace)

    # Create layout for the graph
    layout = go.Layout(title=f'Stock Price ({stock_info})',
                       xaxis=dict(title='Date'),
                       yaxis=dict(title=f'{stock_info}'))

    # Update the layout of the figure
    fig.update_layout(layout)

    return fig


def show_plot(stock_data, stock_name, stock_info, date_range):
    fig = generate_stock_line_graph(stock_data, stock_name, stock_info)
    fig.show()
