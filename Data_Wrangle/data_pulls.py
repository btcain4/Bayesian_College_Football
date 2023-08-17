#
# Script Name: data_pulls.py
# Author: Brian Cain

# The purpose of this script is to define functions that handle
# all pulls from the API datasource https://collegefootballdata.com/.
# This includes api authentication/requests, dataframe creation,
# datafile creation, and data specification (selecting what raw data is needed).

##Import packages necessary for pulling in data and data storage creation
import requests
import pandas as pd


##Define function to grab api data from CollegeFootballData.com and authenticate
def getData(url,access_token):

    resp = requests.get(url,
                        headers={'Authorization':'Bearer {}'.format(access_token)})

    ##Assess if the data pull worked correctly (if not trigger API error code)
    if resp.status_code == 200:
        apiData = resp.json()
        return apiData
    else:
        raise NameError('API Error, Reponse:' + str(resp.status_code))

##FUNCTIONS CREATING/EDITING DATAFRAMES----------

##Define function that creates a dataframe for raw data to be entered into (Applies to first API pull for a dataset)
def createRaw_df(data,colNames,dataTypes):

    ##Assemble data types and corresponding columns
    if dataTypes != False:
        dataTypes_input = [(x,y) for x in colNames for y in dataTypes]
    else:
        dataTypes_input = None

    ##Create dataframe
    df = pd.DataFrame(data,columns=colNames,
                           dtype=dataTypes_input)

    return df

##Define function that appends raw data to existing dataframe (Applies to all succeeding API pulls for a dataset)
def appendRaw_df(originalDf,data,colNames):

    ##Create new dataframe with new data and stack it onto original ddataframe
    additionalDf = pd.DataFrame(data,columns=colNames)
    newDf = originalDf.append(additionalDf, ignore_index=False)

    return newDf

##FUNCTIONS PULLING IN VARIOUS DATAPOINTS FOR DATASET CREATION----------


##Define function that pulls in data on individual FBS teams
def obtainTeam_data(url,access_token):

    jsonData_team = getData(url,access_token)

    teamData = []
    for i in jsonData_team:
        dataEntry = []
        i.pop('location')
        colNames = list(i.keys())
        for j in colNames:
            dataEntry.append(i[j])
        teamData.append(dataEntry)

    colNames_team = list(jsonData_team[0].keys())
    
    return teamData, colNames_team


##Define function that pulls in game data
def obtainGame_data(url,access_token,week_num):

    jsonGame_data = getData(url,access_token)

    gameData = []
    for i in jsonGame_data:

        gameId = i['id']
        gameWeek = int(week_num)
        gameSeason = i['season']
        gameDate = i['start_date']
        homeTeam_id = i['home_id']
        awayTeam_id = i['away_id']
        homePoints = i['home_points']
        awayPoints = i['away_points']
        homeQuarterly_points = i['home_line_scores'] 
        awayQuarterly_points = i['away_line_scores']
        home_elo = i['home_pregame_elo']
        away_elo = i['away_pregame_elo']
        home_homeBool, away_homeBool = 1, 0
        
        homeData = [gameId,gameWeek,gameSeason,homeTeam_id,homePoints,homeQuarterly_points,home_elo,home_homeBool]
        awayData = [gameId,gameWeek,gameSeason,awayTeam_id,awayPoints,awayQuarterly_points,away_elo,away_homeBool]
        gameData.append(homeData)
        gameData.append(awayData)

    colNames_game = ['gameId','week_num','gameSeason','team_id','points','Quarterly_points','elo','homeBool']
    
    return gameData, colNames_game


##Define function that gets individual game detailed stats
def obtainStats_data(url,access_token,week_num):

    ##Define a function to extract specified stat from API data
    def extractStat(gameData,homeStatus,statName):

        try:
        
            statValue = next(stat for stat in gameData['teams'][homeStatus]['stats'] if stat['category'] == statName)['stat'] ##returns 0 if stat is not available, indicating stat is 0

        except:

            statValue = 0

        return statValue

    jsonStats_data = getData(url,access_token)

    statsData = []
    for i in jsonStats_data:
        
        gameId = i['id']
        homeSchool = i['teams'][0]['school']
        awaySchool = i['teams'][1]['school']
        home_rush_td, away_rush_td = extractStat(i, 0,'rushingTDs'), extractStat(i, 1,'rushingTDs')
        home_pass_td, away_pass_td = extractStat(i, 0,'passingTDs'), extractStat(i, 1,'passingTDs')
        home_rush_attempt, away_rush_attempt = extractStat(i, 0,'rushingAttempts'), extractStat(i, 1,'rushingAttempts')
        home_yp_rush, away_yp_rush = extractStat(i, 0,'yardsPerRushAttempt'), extractStat(i, 1,'yardsPerRushAttempt')
        home_yp_pass, away_yp_pass = extractStat(i, 0,'yardsPerPass'), extractStat(i, 1,'yardsPerPass')
        home_rush_yards, away_rush_yards = extractStat(i, 0,'rushingYards'), extractStat(i, 1,'rushingYards')
        home_completion_attempts, away_completion_attempts = str(extractStat(i, 0,'completionAttempts')), str(extractStat(i, 1,'completionAttempts'))
        home_pass_yards, away_pass_yards = extractStat(i, 0,'netPassingYards'), extractStat(i, 1,'netPassingYards')
        home_total_yards, away_total_yards = extractStat(i, 0,'totalYards'), extractStat(i, 1,'totalYards')
        home_turnovers, away_turnovers = extractStat(i, 0,'turnovers'), extractStat(i, 1,'turnovers')
        home_tfl, away_tfl = extractStat(i, 0,'tacklesForLoss'), extractStat(i, 1,'tacklesForLoss')
        home_sacks, away_sacks = extractStat(i, 0,'sacks'), extractStat(i, 1,'sacks')
        home_qb_hurries, away_qb_hurries = extractStat(i, 0,'qbHurries'), extractStat(i, 1,'qbHurries')
        home_fumbles_lost, away_fumbles_lost = extractStat(i, 0,'fumblesLost'), extractStat(i, 1,'fumblesLost')
        home_interceptions, away_interceptions = extractStat(i, 0,'interceptions'), extractStat(i, 1,'interceptions')
        home_possessionTime, away_possessionTime = str(extractStat(i, 0,'possessionTime')), str(extractStat(i, 1,'possessionTime'))
        home_penalty_yards, away_penalty_yards = str(extractStat(i, 0,'totalPenaltiesYards')), str(extractStat(i, 1,'totalPenaltiesYards'))
        home_fourthDown_eff, away_fourthDown_eff = str(extractStat(i, 0,'fourthDownEff')), str(extractStat(i, 1,'fourthDownEff'))
        home_thirdDown_eff, away_thirdDown_eff = str(extractStat(i, 0,'thirdDownEff')), str(extractStat(i, 1,'thirdDownEff'))
        home_firstDowns, away_firstDowns = extractStat(i, 0,'firstDowns'), extractStat(i, 1,'firstDowns')
        home_defensive_td, away_defensive_td = extractStat(i, 0,'defensiveTDs'), extractStat(i, 1,'defensiveTDs')
        home_homeBool, away_homeBool = 1, 0

        homeData = [gameId,week_num,homeSchool,home_rush_td,home_pass_td,home_rush_attempt,
                    home_yp_rush,home_rush_yards,home_yp_pass,home_completion_attempts,
                    home_pass_yards,home_total_yards,home_turnovers,
                    home_tfl,home_sacks,home_qb_hurries,home_fumbles_lost,
                    home_interceptions,home_possessionTime,home_penalty_yards,home_fourthDown_eff,
                    home_thirdDown_eff,home_firstDowns,home_defensive_td,home_homeBool]
        awayData = [gameId,week_num,awaySchool,away_rush_td,away_pass_td,away_rush_attempt,
                    away_yp_rush,away_rush_yards,away_yp_pass,away_completion_attempts,
                    away_pass_yards,away_total_yards,away_turnovers,
                    away_tfl,away_sacks,away_qb_hurries,away_fumbles_lost,
                    away_interceptions,away_possessionTime,away_penalty_yards,away_fourthDown_eff,
                    away_thirdDown_eff,away_firstDowns,away_defensive_td,away_homeBool]

        if len([float(i) for i in homeData[3:9]+homeData[10:18]+homeData[22:24] if float(i) == 0]) == 17 or len([float(i) for i in awayData[3:9]+awayData[10:18]+awayData[22:24] if float(i) == 0]) == 17:
            continue ##Skips to next iteration because game stats were not available

        statsData.append(homeData)
        statsData.append(awayData)

    colNames_stats = ['gameId','week_num','school','rush_td','pass_td','rush_attempt','yp_rush','rush_yards',
                      'yp_pass','completion_attempts','pass_yards','total_yards','turnovers','tfl','sacks',
                      'qb_hurries','fumbles_lost','interceptions','possession_time','penalty_yards',
                      'fourthDown_eff','thirdDown_eff','firstDowns','defensive_td','homeBool']

    return statsData, colNames_stats


##Function that gets individual game advanced metrics
def obtainMetrics_data(url,access_token,week_num):

    jsonMetrics_data = getData(url,access_token)

    metricsData = []
    for i in jsonMetrics_data:

        gameId = i['gameId']
        school = i['team']

        ##NOTE: all defensive metrics are just the opposing teams offensive metrics
        offensive_plays = i['offense']['plays']
        offensive_drives = i['offense']['drives']
        offensive_ppa = i['offense']['ppa']
        offensive_successRate = i['offense']['successRate']
        offensive_explosiveness = i['offense']['explosiveness']
        offensive_powerSuccess = i['offense']['powerSuccess']
        offensive_stuffRate = i['offense']['stuffRate']
        offensive_lineYards = i['offense']['lineYards']
        offensive_secondLevelYards = i['offense']['secondLevelYards']
        offensive_openFieldYards = i['offense']['openFieldYards']

        data = [gameId,week_num,school,offensive_plays,offensive_drives,offensive_ppa,offensive_successRate,offensive_explosiveness,
                offensive_powerSuccess,offensive_stuffRate,offensive_lineYards,offensive_secondLevelYards,offensive_openFieldYards]
        metricsData.append(data)

    colNames_metrics = ['gameId','week_num','school','offensive_plays','offensive_drives','offensive_ppa','offensive_successRate','offensive_explosiveness',
                'offensive_powerSuccess','offensive_stuffRate','offensive_lineYards','offensive_secondLevelYards','offensive_openFieldYards']
    
    return metricsData, colNames_metrics

##RUN INITIAL DATAPULLS TO CREATE MODELING DATASETS USING FUNCTIONALITY ABOVE------------------------

##Invoke Commands to be run for initial setup of first dataframe dating from 2015-2021 (excludes 2020 for covid uncertainty)
if __name__ == '__main__':

    ##Define desired game seasons for data
    seasons = ['2015','2016','2017','2018','2019','2021']

    ##Define college football API access token
    access_token = '' ## Left blank for security purposes.
    
    ##Loop through desired seasons for game data
    ct = 0
    for i in seasons:
        for j in range(15): ##15 weeks in regular season

            j = str(j+1)
            
            url_game = 'https://api.collegefootballdata.com/games?year='+i+'&week='+j+'&seasonType=regular'
        
            if ct == 0: ##Create initial dataframes
                gameData, colNames_game = obtainGame_data(url_game,access_token,j)
                gameDf = createRaw_df(gameData,colNames_game,False)
            else:
                gameData, colNames_game = obtainGame_data(url_game,access_token,j)
                gameDf = appendRaw_df(gameDf,gameData,colNames_game)

            ct += 1
    
    gameDf.to_csv('D:\College_Football_Model_Data\\gameDf.csv', index = False)

    ##Loop through desired seasons to obtain stats for each game
    ct = 0
    for i in seasons:
        for j in range(15):

            j = str(j+1)

            if ct == 0: ##Create initial dataframe (createRaw_df function)
                url_stats = 'https://api.collegefootballdata.com/games/teams?year='+i+'&week='+j+'&seasonType=regular'
                statsData, colNames_stats = obtainStats_data(url_stats,access_token,j)
                statsDf = createRaw_df(statsData,colNames_stats,False)
                ct += 1
            else: ##(appendRaw_df function)
                url_stats = 'https://api.collegefootballdata.com/games/teams?year='+i+'&week='+j+'&seasonType=regular'
                statsData, colNames_stats = obtainStats_data(url_stats,access_token,j)
                statsDf = appendRaw_df(statsDf,statsData,colNames_stats)

    statsDf['completion_attempts'] = statsDf['completion_attempts'].astype(str) ##Column displayed unique date behavior (should be string)
    statsDf['penalty_yards'] = statsDf['penalty_yards'].astype(str)
    statsDf['fourthDown_eff'] = statsDf['fourthDown_eff'].astype(str)
    statsDf['thirdDown_eff'] = statsDf['thirdDown_eff'].astype(str)

    statsDf.to_csv('D:\College_Football_Model_Data\\statsDf.csv', index = False)

    ##Loop through desired seasons to obtain metrics for each game
    ct = 0
    for i in seasons:
        for j in range(15):

            j = str(j+1)

            if ct == 0: ##Create initial dataframe (createRaw_df function)
                url_metrics = 'https://api.collegefootballdata.com/stats/game/advanced?year='+i+'&week='+j
                metricsData, colNames_metrics = obtainMetrics_data(url_metrics,access_token,j)
                metricsDf = createRaw_df(metricsData,colNames_metrics,False)
                ct += 1
            else: ##(appendRaw_df function)
                url_metrics = 'https://api.collegefootballdata.com/stats/game/advanced?year='+i+'&week='+j
                metricsData, colNames_metrics = obtainMetrics_data(url_metrics,access_token,j)
                metricsDf = appendRaw_df(metricsDf,metricsData,colNames_metrics)

    metricsDf.to_csv('D:\College_Football_Model_Data\\metricsDf.csv', index = False)

    ##Create dataframe housing all FBS team information
    url_team = 'https://api.collegefootballdata.com/teams/fbs'
    teamData, colNames_team = obtainTeam_data(url_team,access_token)
    teamDf = createRaw_df(teamData,colNames_team,False)
    teamDf.to_csv('D:\College_Football_Model_Data\\teamDf.csv', index = False)


