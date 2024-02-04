"""
File: nationality_gender.py
Description: Description: Create a sankey diagram with the artists' nationality
as the source and their gender as the target

"""
import pandas as pd
import sankey_multilayer as sk
import hw2_functions as fn


def main():
    # read the json file into a pandas dataframe and get Nationality, Gender, and Begin Date
    artists_df = pd.read_json('artists.json')

    # drop missing data
    artists_df = fn.drop_data(artists_df)

    # group by nationality and gender
    artists_agg = fn.aggregate(artists_df, 'Nationality', 'Gender', 30)

    sk.make_sankey(artists_agg, 'Nationality', 'Gender', vals='Count')


if __name__ == '__main__':
    main()
