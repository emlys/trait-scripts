import math
import numpy as np
import pandas as pd


# Processing script I used to generate the files binomial_to_symbol.csv and symbol_to_data.csv
# Not very efficient, but it shouldn't need to be run ever again


# This CSV has one row corresponding to each species synonym symbol (with a few duplicates)
# Some rows have the official latin binomial name for a species. Other rows have synonyms for official names.
# Rows that represent the same species have the same value in the 'Accepted Symbol' column.
data = pd.read_csv('usda_plants_complete.csv', dtype=object)


def merge(df: pd.DataFrame) -> pd.Series:
    """Merge data from all rows of df into one series"""

    merged = df.loc[0].copy()

    for i, row in df.loc[1:].iterrows():
        for column in df.columns:
            if pd.isnull(merged[column]) and pd.notnull(row[column]):
                merged[column] = row[column]
    return merged



in_progress = pd.DataFrame(columns=data.columns)
group = pd.DataFrame(columns=data.columns)
complete = pd.DataFrame(columns=data.columns)

# Map scientific names to symbols representing a species
binomial_to_symbol = pd.DataFrame(columns=['Scientific Name', 'Accepted Symbol'])

# Map symbols representing a species to all the data about that species
symbol_to_data = pd.DataFrame(columns=data.columns.drop(['Synonym Symbol', 'Scientific Name']))

def pop(df: pd.DataFrame) -> pd.Series:
    """Implement pop for a DataFrame: remove and return the first row"""
    first = df.iloc[0].copy()
    df.drop(0, inplace=True)
    return first


# Considering the dataframe as a graph:
#   rows are nodes, 
#   edge between nodes means they represent the same species
# do DFS to find all the connected components (groups of rows representing the same species)
# and merge all the data in each connected component into one row

while len(data.index) > 0:
    print(len(data.index))

    # Pop the first row off the dataframe and put it into in-progress
    in_progress = in_progress.append(pop(data))

    while len(in_progress.index) > 0:
  
        current = pop(in_progress)     # Pop the first row off the in-progress stack
        group = group.append(current)  # Move it to the current group

        # Find all rows connected to it
        name_match = data['Scientific Name'] == current['Scientific Name']
        accepted_symbol_match = data['Accepted Symbol'] == current['Accepted Symbol']
        synonym_symbol_match = data['Synonym Symbol'] == current['Accepted Symbol']

        # Boolean series: for each row in data, True if it represents the same species as `current`, False otherwise
        if pd.notnull(current['Synonym Symbol']):
            match_bools = name_match | accepted_symbol_match | synonym_symbol_match | (data['Accepted Symbol'] == current['Synonym Symbol'])
        else:
            match_bools = name_match | accepted_symbol_match | synonym_symbol_match

        # Push the new-found rows onto the in-progress stack 
        matches = data.loc[match_bools]
        in_progress = in_progress.append(matches).reset_index(drop=True)

        # Delete the accessed rows from the dataset
        data = data.loc[~match_bools].reset_index(drop=True)
        

    # get the accepted symbol for all rows of the group
    # if there are multiple accepted symbols in the group, list them all
    merged_symbol = ','.join(group['Accepted Symbol'].unique().tolist())

    # all rows in this connected component are in `group` now
    merged_data = merge(group.reset_index(drop=True)).drop(labels=['Synonym Symbol', 'Scientific Name'])
    merged_data['Accepted Symbol'] = merged_symbol
    
    binomial_rows = [{'Scientific Name': binomial, 'Accepted Symbol': merged_symbol} for binomial in group['Scientific Name']]
    binomial_to_symbol = binomial_to_symbol.append(binomial_rows)

    symbol_to_data = symbol_to_data.append(merged_data, ignore_index=True)

    group = pd.DataFrame(columns=data.columns)


binomial_to_symbol.to_csv('binomial_to_symbol.csv', index=False)
symbol_to_data.to_csv('symbol_to_data.csv', index=False)



