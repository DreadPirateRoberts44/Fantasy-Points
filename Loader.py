import csv
from time import time
import numpy as np
import pandas as pd
import warnings
warnings.simplefilter("ignore")


# Clean Missing data
def cleanMissingData(df):

     return

# Handle players who have a null value for their fantasy score
# TODO Evaluate with/without dropping these players, as null might be the representation of true 0
# currently this should not be run, difference in coefficient of determination when calling this is .39 vs .53 without
def handleMissingFantasyPoints(df):
     df.dropna(subset=["FantPt"], inplace=True)
     

# Replace values known by player that the dataset doesn't record for every row
# These values must be static (or relatively static)
def handleKnownMissingData(df):

     df["Bench Press"] = df["Bench Press"].fillna(df.groupby("Player")["Bench Press"].transform('median')) # There a lot of null/0 values for players with information. Either manually clean the data, or programmatically place these values
     df["40\xa0Yard"] = df["40\xa0Yard"].fillna(df.groupby("Player")["40\xa0Yard"].transform('median'))
     df["Vert Leap\xa0(in)"] = df["Vert Leap\xa0(in)"].fillna(df.groupby("Player")["Vert Leap\xa0(in)"].transform('median'))
     df["Shuttle"] = df["Shuttle"].fillna(df.groupby("Player")["Shuttle"].transform('median'))
     df["3Cone"] = df["3Cone"].fillna(df.groupby("Player")["3Cone"].transform('median'))
     df["Broad Jump\xa0(in)"] = df["Broad Jump\xa0(in)"].fillna(df.groupby("Player")["Broad Jump\xa0(in)"].transform('median'))
     df["Weight"] = df["Weight"].fillna(df.groupby("Player")["Weight"].transform('median'))
     df["Draft Round"] = df["Draft Round"].fillna(df.groupby("Player")["Draft Round"].transform('median'))
     #df["3Cone"] = df["3Cone"].fillna(df.groupby("Player")["3Cone"].transform('median'))
     #df["3Cone"] = df["3Cone"].fillna(df.groupby("Player")["3Cone"].transform('median'))
     #df["3Cone"] = df["3Cone"].fillna(df.groupby("Player")["3Cone"].transform('median'))
     #df["3Cone"] = df["3Cone"].fillna(df.groupby("Player")["3Cone"].transform('median'))
     
     return

# Replace or kill null values in the data set
def handleMissingData(df):
    #handleMissingFantasyPoints(df)

    # any 0 values should be treated as not a number TODO verify if/any exceptions
    df.replace(0,np.nan, inplace=True)
    handleKnownMissingData(df)
    # currently grouping by position, might not need to group here if we split the df into split the df into pieces
    # TODO this might be replacing ALL values, not just NAN, which is overstepping
    df["Bench Press"] = df["Bench Press"].fillna(df.groupby("FantPos")["Bench Press"].transform('median')) # There a lot of null/0 values for players with information. Either manually clean the data, or programmatically place these values
    df["40\xa0Yard"] = df["40\xa0Yard"].fillna(df.groupby("FantPos")["40\xa0Yard"].transform('median'))
    df["Vert Leap\xa0(in)"] = df["Vert Leap\xa0(in)"].fillna(df.groupby("FantPos")["Vert Leap\xa0(in)"].transform('median'))
    df["Shuttle"] = df["Shuttle"].fillna(df.groupby("FantPos")["Shuttle"].transform('median'))
    df["3Cone"] = df["3Cone"].fillna(df.groupby("FantPos")["3Cone"].transform('median'))
    df["Broad Jump\xa0(in)"] = df["Broad Jump\xa0(in)"].fillna(df.groupby("FantPos")["Broad Jump\xa0(in)"].transform('median'))

    df.replace(np.nan, 0, inplace=True) # categorical 0's break
    # TODO remove this once for sure not needed
    # Leaving this in to prevent crashes. I don't think it handles this data particularly well, so should make sure to fix at some point
    #df.interpolate(inplace=True)

    return


# This method handles data that isn't known prior to the season
# so shouldn't be used as is for making predictions
# TODO use previous years data per player to 
def handlePostSeasonData(df):
     df["PreviousSeasonsCount"] = 0
     df["PreviousScore"] = 0
     df["PreviousPlayed"] = 0
     df["PreviousStarts"] = 0
     identifyRookies(df)

     # TODO look to incorporate these into future stats
     df.drop(['G', 'GS', 'Cmp', 'Att', 'Yds', 'TD','Int','Att.1','Yds.1', 'Y/A', "TD.1", 'Rec', 'Yds.2', 'Y/R', 'TD.2'], axis=1, inplace=True) # We shouldn't explicitly need to drop these


# ML models can't handle nonnumeric data
# For now remove all non numeric columns 
# TODO convert to number as appropriate 
def handleNonNumericData(df):

     df['FantPos'] = df['FantPos'].astype('category')
     # Convert the categorical column to integer codes
     df['FantPos'] = df['FantPos'].cat.codes

     df['Home State'] = df['Home State'].astype('category')
     # Convert the categorical column to integer codes
     df['Home State'] = df['Home State'].cat.codes

     df['Tm'] = df['Tm'].astype('category')
     # Convert the categorical column to integer codes
     df['Tm'] = df['Tm'].cat.codes

     df['College'] = df['College'].astype('category')
     # Convert the categorical column to integer codes
     df['College'] = df['College'].cat.codes

     df = df.select_dtypes(include=['number'])

# TODO reevaluate how much this data might matter
# This doesn't get/need called. Leaving it in for reference
def dropIrrelevantData(df):
     df.drop(['Year', 'DOB', 'Wonderlic'], axis=1, inplace=True) 


def dropUnusedColumns(df):
     handleNonNumericData(df)
     handlePostSeasonData(df)
       

#TODO rename
# determine modularization
def identifyRookies(df):
     i = 0
     players = {}
     for index, row in df.iterrows():
          if row["Player"] in players: 
               df.at[index, "PreviousScore"]  = players[row["Player"]]["PreviousScore"] # currently just tracking one, could be more cumulative
               df.at[index, "PreviousPlayed"]  = players[row["Player"]]["PreviousPlayed"] # currently just tracking one, could be more cumulative
               df.at[index, "PreviousStarts"]  = players[row["Player"]]["PreviousStarts"] # currently just tracking one, could be more cumulative
               df.at[index, "PreviousSeasonsCount"] = players[row["Player"]]["PreviousSeasonsCount"]
               players[row["Player"]]["PreviousSeasonsCount"] += 1
          else:
               players[row["Player"]] = {}
               players[row["Player"]]["PreviousSeasonsCount"] = 1

          players[row["Player"]]["PreviousScore"] = row["FantPt"]
          players[row["Player"]]["PreviousPlayed"] = row["G"]
          players[row["Player"]]["PreviousStarts"] = row["GS"]


# filename - name of the file to open
# choice - 1 is use the original file, 2 is to use a modified version
def getPlayerData(filename, choice):
    if int(choice) < 3:
          df = pd.read_excel(filename, engine="openpyxl", sheet_name='1999-2013 data')
          handleMissingData(df)
          df.sort_values(by=["Hometown", "Player", "Year"], inplace=True) # sort so missing/new player information can be generated   
          dropUnusedColumns(df)
          if choice == 2:
               df.to_excel("modified.xlsx",sheet_name='1999-2013 data')
    else:
          df = pd.read_excel(filename, engine="openpyxl", sheet_name='1999-2013 data')
    return df


