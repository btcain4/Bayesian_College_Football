#
# Script Name: data_joins.py
# Author: Brian Cain

# The purpose of this script is to define functions that will
# join the multiple CFB datasets together. Any additional joins
# needed for data cleaning purposes are housed in the
# data_cleaning.py file.

##Import necessary packages
import pandas as pd
import numpy as np

##Define function that will join all necessary data into a single dataframe
def join_data(statsDf,gameDf,metricsDf,teamDf):

    ##Join school id onto statsDf
    joinedDf = (pd.merge(statsDf,teamDf[['school','id']],
                         how='left',
                         left_on=['school'],
                         right_on=['school']))

    ##Join game dataframe onto the statsDf
    joinedDf = (pd.merge(joinedDf,gameDf,
                         how='left',
                         left_on=['gameId','id'],
                         right_on=['gameId','team_id']))

    ##Join the metricsDf onto the joined dataframe
    metricsDf = (pd.merge(metricsDf,teamDf[['school','id']],
                          how='left',
                          left_on=['school'],
                          right_on=['school']))
    joinedDf = (pd.merge(joinedDf,metricsDf,
                         how='left',
                         left_on=['gameId','id'],
                         right_on=['gameId','id']))

    ##Remove duplicated columns
    joinedDf = joinedDf.drop(columns=['homeBool_y','week_num_y','gameSeason','id','school_y'])
    joinedDf = joinedDf.rename(columns={'homeBool_x': 'homeBool', 'week_num_x': 'week_num',
                                        'school_x': 'school'})

    return joinedDf

##Invole commands to join initial raw data
if __name__ == '__main__':

    ##Import all our initial dataframes
    gameDf = pd.read_csv('D:\\College_Football_Model_Data\\gameDf.csv')
    statsDf = pd.read_csv('D:\\College_Football_Model_Data\\statsDf.csv')
    teamDf = pd.read_csv('D:\\College_Football_Model_Data\\teamDf.csv') ##Some teams aren't in here if they are not FBS
    metricsDf = pd.read_csv('D:\\College_Football_Model_Data\\metricsDf.csv')

    ##Join all the data into a single dataframe and save to storage location
    joinedDf = join_data(statsDf,gameDf,metricsDf,teamDf)
    joinedDf.to_csv('D:\College_Football_Model_Data\\joinedDf.csv', index = False)
    
    
