"""
File: stocks_api.py
Description: Provide an API for accessing stocks data in a directory
"""
import os
import pandas as pd


class StocksAPI:

    def __init__(self, path=None):
        """
        Constructor for the API
        :param path: path to the directory where the stocks data is stored
        """
        self.path = path
        self.total_stocks_df = self.get_combined_df()

    @staticmethod
    def _get_stock_name(csv):
        """
        Helper function to get the name of the stock based on the CSV file
        :param csv: the csv that contains the stock data
        :return stock_name: the name of the stock
        """
        stock_name = str(csv.name)
        stock_name = stock_name.replace('.csv', '')

        return stock_name

    def get_stock_list(self):
        """
        Return the stock names that are in the data directory
        :return stock_names: list of stock names
        """
        stock_names = list()

        for filename in os.scandir(self.path):
            if filename.is_file():
                stock_name = StocksAPI._get_stock_name(filename)
                stock_names.append(stock_name)

        return stock_names

    def get_combined_df(self):
        """
        Access different stock csv files in a directory and combined them
        :return total_stocks_df: Combined dataframe with stock data
        """
        total_stocks_df = pd.DataFrame()  # intialize the combined stock dataframe as en emtpy dataframe

        for filename in os.scandir(self.path):
            if filename.is_file() and filename.name.endswith('.csv'):
                if self.path:
                    csv_path = self.path + "/" + str(filename.name)
                else:
                    csv_path = str(filename.name)

                stock_df = pd.read_csv(csv_path)
                stock_df['Date'] = pd.to_datetime(stock_df['Date'])

                stock_name = StocksAPI._get_stock_name(filename)

                stock_df['Stock_Name'] = stock_name  # add a stock name column so stocks can be identified

                # concat the dataframe for each stock to the combined dataframe
                total_stocks_df = pd.concat([total_stocks_df, stock_df])

        return total_stocks_df

    @staticmethod
    def _get_date(df):
        """
        Helper function to get either the earliest or latest date
        :param df: dataframe that has dates
        :return:
        """
        date = df['Date'].iloc[0]  # get the earliest date

        return date

    def get_extreme_date(self, earliest):
        """
        Get the earliest date for the stock data
        :param earliest: true/false value to get either earliest or latest date
        :return first_date_list: list in [yyyy, mm, dd]
        """
        if earliest:
            df = self.total_stocks_df.sort_values(by='Date')  # sort by the date, ascending
            date = self._get_date(df)

        else:
            df = self.total_stocks_df.sort_values(by='Date', ascending=False)  # sort by the date, descending
            date = self._get_date(df)

        return date

    @staticmethod
    def trim_data(df, stock_name, start_date, end_date):
        """
        Get dataframe with stock data that matches the criteria
        :param df: dataframe to trim
        :param stock_name: Name(s) of stocks select
        :param start_date: start date of range
        :param end_date: end date of range
        :return: trimmed dataframe
        """
        trimmed_df = df[df['Stock_Name'].isin(stock_name) & (df['Date'] >= start_date)
                        & (df['Date'] <= end_date)]

        return trimmed_df




