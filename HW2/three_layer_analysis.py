"""
File: three_layer_analysis.py
Description: Create a sankey diagram using artists.json to visualize connections between the Nationality, Gender,
and Decade of birth of artists
"""
import pandas as pd
import hw2_functions as fn
import sankey_multilayer as sk


def main():
    artists_df = pd.read_json('artists.json')

    # drop missing data
    artists_df = fn.drop_data(artists_df)

    # get the decade of birth and then group artists by Nationality, Gender, and Decade of Birth
    artists_df = fn.get_decade(artists_df, 'BeginDate')
    df_agg = fn.aggregate(artists_df, 'Nationality', 'Gender', 25, 'Decade')

    # make the sankey diagram
    sk.make_sankey(df_agg, 'Nationality', 'Gender', 'Decade', vals='Count')


if __name__ == '__main__':
    main()
