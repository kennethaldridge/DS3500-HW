"""
File: gender_decade.py
Description: Create a sankey diagram with the artists' gender as the source and their
decade of birth as the target
"""

import pandas as pd
import sankey_multilayer as sk
import hw2_functions as fn


def main():
    artists_df = pd.read_json('artists.json')

    # drop missing data
    artists_df = fn.drop_data(artists_df)

    # get the decade of birth for each artist then group by nationality and decade
    artists_df = fn.get_decade(artists_df, 'BeginDate')
    artists_agg = fn.aggregate(artists_df, 'Gender', 'Decade', 35)

    sk.make_sankey(artists_agg, 'Gender', 'Decade', vals='Count')


if __name__ == '__main__':
    main()
