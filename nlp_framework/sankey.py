"""
File: sankey.py
Description: Provide a wrapper that maps a dataframe to a sankey diagram
"""

import plotly.graph_objects as go


def _code_mapping(df, src, targ):
    """Map labels in src and targ to integers"""

    # get distinct labels
    labels = sorted(set(list(df[src])+list(df[targ])))

    # get integer codes
    codes = list(range(len(labels)))

    # create label to code mapping
    lc_map = dict(zip(labels, codes))

    # substitute names for codes in the dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels


def make_sankey(df, src, targ, vals=None, **kwargs):
    """

    :param df: Input dataframe
    :param src: Source column of labels
    :param targ: Target column of labels
    :param vals: Thickness of link for each row
    :return:
    """

    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)  # all 1's

    df, labels = _code_mapping(df, src, targ)
    # underscore signals that code mapping is helping implementation

    line_color = kwargs.get('line_color', 'black')
    width = kwargs.get('width', 2)
    # look up key and return default value if key doesn't exist

    link = {'source': df[src], 'target': df[targ], 'value': values,
            'line': {'color': line_color, 'width': width}}
    node = {'label': labels}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()

