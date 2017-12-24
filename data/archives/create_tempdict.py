import pandas as pd
import pickle as pk


raw_data = pd.read_csv("migration_data-2000-2015-cleaned.csv", sep="\t" )

all_countries = raw_data["Country of birth"].unique()
focus_countries = raw_data["Focus country"].unique()


### Type de dictionnaire final
# AUS : focus country
# AFG : other country
# 2000: date
# 887: number of people from AFG coming from AFG entering AUS
# -1: number of from AFG coming from AUS going back to AFG 
# (-1: unknown value)
#
# dic["AUS"] = {"AFG": {2000:[887, -1]}} 


### Initialisation
dic = {}
for i in focus_countries:
    current_dic = {}
    for j in all_countries:
        current_dic2 = {}
        for k in range(2000, 2016):
            current_dic2[k] = [-1, -1]
        current_dic[j] = current_dic2
    dic[i] = current_dic


### Parcours final pour récupérer les différences
# Et les mettre sous forme de dataFrames
for index in range(len(raw_data)):
    series = raw_data.iloc[index]
    
    if series.Direction == "INFLOW":
        dic[series["Focus country"]][series["Country of birth"]][series.Year][0] = series.Value
    elif series.Direction == "OUTFLOW":
        dic[series["Focus country"]][series["Country of birth"]][series.Year][1] = series.Value
    else:
        print("*** Dirty data at line {}.".format(index))
    
    if index%1000 == 0:
        print("{:.1f} %".format(index/len(raw_data)*100))
        

if input("Save dictionnary in \"tempdict.pk\"? (Type 1. Else type 0)") == 1:
    with open("tempdict.pk", 'wb') as f:
        pk.dump(dic, f)
