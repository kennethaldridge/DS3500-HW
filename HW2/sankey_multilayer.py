"""
File: Sankey_multilayer.py
Description: Provide a wrapper that can map multiple columns of a dataframe to a sankey function
"""

import plotly.graph_objects as go
import pandas as pd


def _stacking(df, cols, vals):
    """created a stacked dataframe with a src, targ and potentially vals column"""
    # if there is a values column, carry over in stacking function, if not, then ignore
    if vals:
        # initialize empty dataframe
        stacked = pd.DataFrame(columns=['src', 'targ', 'vals'])

        # go through column list and stack adjacent columns
        for i in list(range(0, len(cols)-1)):
            other_df = df[[cols[i], cols[i + 1], vals]]
            other_df.columns = ['src', 'targ', 'vals']

            stacked = pd.concat([stacked, other_df], axis=0, ignore_index=True)
    else:
        # initialize empty dataframe
        stacked = pd.DataFrame(columns=['src', 'targ'])

        # go through column list and stack adjacent columns
        for i in list(range(0, len(cols) - 1)):
            other_df = df[[cols[i], cols[i + 1]]]
            other_df.columns = ['src', 'targ']

            stacked = pd.concat([stacked, other_df], axis=0, ignore_index=True)

    return stacked


def _code_mapping(df, src, targ):
    """ Map labels in src and targ to integers """
    # get distinct labels
    labels = sorted(set(list(df[src])+list(df[targ])))

    # get integer codes
    codes = list(range(len(labels)))

    # create label to code mapping
    lc_map = dict(zip(labels, codes))

    # substitute names for codes in the dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels


def make_sankey(df, col1, col2, *cols, vals=None, **kwargs):
    """
    :param df: Chosen dataframe
    :param col1: first chosen column
    :param col2: second chosen column
    :param cols: other columns
    :param vals: values to assign to sankey
    :return:
    """
    # change all column data types to string
    columns = [col1, col2] + list(cols)
    for col in columns:
        df[col] = df[col].astype(str)

    # create a stacked dataframe
    df = _stacking(df, columns, vals=vals)

    if vals:
        values = df['vals']
    else:
        values = [1] * len(df)  # all 1's

    # return data frame with codes and the labels
    df, labels = _code_mapping(df, 'src', 'targ')

    line_color = kwargs.get('line_color', 'gray')
    width = kwargs.get('width', 0)

    # define the links and the nodes for the sankey diagram
    link = {'source': df['src'], 'target': df['targ'], 'value': values,
            'line': {'color': line_color, 'width': width}}
    node = {'label': labels}

    # create the sankey diagram
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()


