"""
File: nationality_decade.py
Description: Description: Create a sankey diagram with the artists' nationality
as the source and their decade of birth as the target
"""
import pandas as pd
import sankey_multilayer as sk
import hw2_functions as fn


def main():
    # read the json file into a pandas dataframe and get Nationality, Gender, and Begin Date
    artists_df = pd.read_json('artists.json')

    # drop missing data
    artists_df = fn.drop_data(artists_df)

    # get the decade of birth for each artist then group by nationality and decade
    artists_df = fn.get_decade(artists_df, 'BeginDate')
    artists_agg = fn.aggregate(artists_df, 'Nationality', 'Decade', 20)

    sk.make_sankey(artists_agg, 'Nationality', 'Decade', vals='Count')


if __name__ == '__main__':
    main()
