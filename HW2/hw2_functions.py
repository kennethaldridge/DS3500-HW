"""
File: hw2_functions.py
Description: file containing get_decade and aggregate functions
"""


def drop_data(df):
    # drop missing data and where nationality is unknown
    df.dropna(inplace=True)

    df.drop(df[df['BeginDate'] == 0].index, inplace=True)

    df.drop(df[df['Nationality'] == 'Nationality unknown'].index, inplace=True)

    return df

def get_decade(df, col):
    """
    :param df: Input dataframe
    :param col: Input column
    :return df: Output dataframe
    """
    # change column type to a string and replace last digit of birth year with 0 then change datatype to int
    df[col] = df[col].astype(str)
    df[col] = df[col].apply(lambda x: x[:-1] + '0')
    df[col] = df[col].astype(int)

    df = df.rename(columns={col: 'Decade'})

    return df


def aggregate(df, group_col1, group_col2, count_min=25, *cols):
    """
       :param df: Input dataframe
       :param group_col1: group by column 1
       :param group_col2: group by column 2
       :param count_min: minimum count of artists to be included in the dataframe
       :param cols: additional columns to be grouped by
       :return df_agg: Output aggregated dataframe
       """

    # get a full list of the grouping columns and group by them and get a count column for each group
    col_list = [group_col1, group_col2] + list(cols)
    df_agg = df.groupby(col_list).size().reset_index()
    df_agg = df_agg.rename(columns={0: 'Count'})

    # only include groups with artist count >= the minimum
    df_agg = df_agg.loc[df_agg['Count'] >= count_min]

    return df_agg
