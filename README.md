# trait-scripts
assorted scripts related to species trait data

All data is from the USDA PLANTS database accessed through the [advanced search](https://plants.sc.egov.usda.gov/adv_search.html). `usda_plants_detailed_with_synonyms.csv` is the original data. Many species are represented by multiple rows in that file because they have multiple synonymous scientific names or symbols, and there are also duplicates. In `binomial_to_symbol.csv` and `symbol_to_data.csv`, the data is combined into a relational format. 

Rows were grouped into connected components by depth-first search, where rows A and B are connected if any of the following is true
- A['Accepted Symbol'] == B['Accepted Symbol']
- A['Synonym Symbol'] == B['Accepted Symbol']
- A['Scientific Name'] == B['Scientific Name'],

meaning that A and B represent the same species. For each species, data from all rows was merged to fill in as many columns as possible, and a symbol assigned to that species.

`binomial_to_symbol.csv` maps Latin binomials to species symbols. `symbol_to_data.csv` maps species symbols to the merged data for that species.
