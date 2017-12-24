# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 16:09:44 2017

@author: Thomas
"""
import pandas as pd
import pickle as pk


# https://docs.python.org/3/library/pickle.html#examples
with open("tempdict.pk", "rb") as f:
    dictionnary = pk.load(f)


raw_data = pd.read_csv("migration_data-2000-2015-cleaned.csv", sep="\t" )
all_countries = raw_data["Country of birth"].unique()
focus_countries = raw_data["Focus country"].unique()

print(all_countries)
print(focus_countries)

### Type de dictionnaire final
# AUS : focus country (a)
# AFG : other country (b)
# 2000: date (c)
# 887: number of people from AFG coming from AFG entering AUS (d)
# -1: number of from AFG coming from AUS going back to AFG  (e)
# (-1: unknown value)
#
# dic["AUS"] = {"AFG": {2000:[887, -1]}} 


### Type de TSV final
# AUS\tAFG\t2000\t887
# (e) is ignored.
# If (d) is unknown, put 0.
with open("transformed_data.tsv", 'w') as f:
    f.write("focus\tcountry\tyear\tnbFromCountryToFocus\n")
    for focus in focus_countries:
        for other_country in all_countries:
            for year in range(2000, 2016):
                value = dictionnary[focus][other_country][year][0]
                if value == -1:
                    value = 0
               
                line = "{}\t{}\t{}\t{}\n".format(focus, other_country, year, value)
                f.write(line)

print("Data has been written in transformed_data.tsv.")