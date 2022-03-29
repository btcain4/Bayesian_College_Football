#
# Script Name: data_pulls.py
# Author: Brian Cain

# The purpose of this script is to define functions that handle
# all pulls from the datasource https://collegefootballdata.com/.
# This includes api authorization/requests, dataframe creation,
# datafile creation, and data specification.

##Import packages necessary for pulling in data and data storage creation
import requests
import pandas as pd


##Define function to grab api data from CollegeFootballData.com
def getData(url,access_token):

    resp = requests.get(url,
                        headers={'Authorization':'Bearer {}'.format(access_token)})

    ##Assess if the data pull worked correcltly (if not trigger API error code)
    if resp.status_code == 200:
        apiData = resp.json()
        return apiData
    else:
        raise NameError('API Error, Reponse:' + str(resp.status_code))

##FUNCTIONS CREATING/EDITING DATAFRAMES----------

##Define function that creates a dataframe for raw data to be entered into (Applies to first API pull)
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

##Define function that appends raw data to existing dataframe (Applies to all succeeding API pulls)
def appendRaw_df(originalDf,data,colNames):

    ##Create new dataframe with new data and stack it onto original ddataframe
    additionalDf = pd.DataFrame(data,columns=colNames)
    newDf = originalDf.append(additionalDf, ignore_index=False)

    return newDf

##FUNCTIONS PULLING IN VARIOUS DATAPOINTS----------


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
        home_passes_deflected, away_passes_deflected = extractStat(i, 0,'passesDeflected'), extractStat(i, 1,'passesDeflected')
        home_fumbles_lost, away_fumbles_lost = extractStat(i, 0,'fumblesLost'), extractStat(i, 1,'fumblesLost')
        home_interceptions, away_interceptions = extractStat(i, 0,'interceptions'), extractStat(i, 1,'interceptions')
        home_possessionTime, away_possessionTime = extractStat(i, 0,'possessionTime'), extractStat(i, 1,'possessionTime')
        home_penalty_yards, away_penalty_yards = extractStat(i, 0,'totalPenaltiesYards'), extractStat(i, 1,'totalPenaltiesYards')
        home_fourthDown_eff, away_fourthDown_eff = extractStat(i, 0,'fourthDownEff'), extractStat(i, 1,'fourthDownEff')
        home_thirdDown_eff, away_thirdDown_eff = extractStat(i, 0,'thirdDownEff'), extractStat(i, 1,'thirdDownEff')
        home_firstDowns, away_firstDowns = extractStat(i, 0,'firstDowns'), extractStat(i, 1,'firstDowns')
        home_defensive_td, away_defensive_td = extractStat(i, 0,'defensiveTDs'), extractStat(i, 1,'defensiveTDs')
        home_homeBool, away_homeBool = 1, 0

        homeData = [gameId,week_num,homeSchool,home_rush_td,home_pass_td,home_rush_attempt,
                    home_yp_rush,home_rush_yards,home_yp_pass,home_completion_attempts,
                    home_pass_yards,home_total_yards,home_turnovers,
                    home_tfl,home_sacks,home_qb_hurries,home_passes_deflected,home_fumbles_lost,
                    home_interceptions,home_possession_time,home_penalty_yards,home_fourthDown_eff,
                    home_thirdDown_eff,home_firstDowns,home_defensive_td,home_homeBool]
        awayData = [gameId,week_num,awaySchool,away_rush_td,away_pass_td,away_rush_attempt,
                    away_yp_rush,away_rush_yards,away_yp_pass,away_completion_attempts,
                    away_pass_yards,away_total_yards,away_turnovers,
                    away_tfl,away_sacks,away_qb_hurries,away_passes_deflected,away_fumbles_lost,
                    away_interceptions,away_possession_time,away_penalty_yards,away_fourthDown_eff,
                    away_thirdDown_eff,away_firstDowns,away_defensive_td,away_homeBool]

        if len([float(i) for i in homeData[3:9]+homeData[10:19]+homeData[20:25] if float(i) == 0]) == 9 or len([float(i) for i in awayData[3:9]+awayData[10:13]+awayData[20:25] if float(i) == 0]) == 9:
            continue ##Skips to next iteration because game stats were not available

        statsData.append(homeData)
        statsData.append(awayData)

    colNames_stats = ['gameId','week_num','school','rush_td','pass_td','rush_attempt','yp_rush','rush_yards',
                      'yp_pass','completion_attempts','pass_yards','total_yards','turnovers','tfl','sacks',
                      'qb_hurries','passes_deflected','fumbles_lost','interceptions','possession_time','penalty_yards',
                      'fourthDown_eff','thirdDown_eff','firstDowns','defensive_td','homeBool']

    return statsData, colNames_stats


##Function that gets individual game advanced metrics
def obtainMetrics_data(url,access_token,week_num):

    jsonMetrics_data = getData(url,access_token)

    metricsData = []
    for i in jsonMetrics_data:

        gameId = i['gameId']
        school = i['team']

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
        
        defensive_plays = i['defensive']['plays']
        defensive_drives = i['defensive']['drives']
        defensive_ppa = i['defensive']['ppa']
        defensive_successRate = i['defensive']['successRate']
        defensive_explosiveness = i['defensive']['explosiveness']
        defensive_powerSuccess = i['defensive']['powerSuccess']
        defensive_stuffRate = i['defensive']['stuffRate']
        defensive_lineYards = i['defensive']['lineYards']
        defensive_secondLevelYards = i['defensive']['secondLevelYards']
        defensive_openFieldYards = i['defensive']['openFieldYards']

        data = [offensive_plays,offensive_drives,offensive_ppa,offensive_successRate,offensive_explosiveness,
                offensive_powerSuccess,offensive_stuffRate,offensive_lineYards,offensive_secondLevelYards,offensive_openFieldYards,
                defensive_plays,defensive_drives,defensive_ppa,defensive_successRate,defensive_explosiveness,
                defensive_powerSuccess,defensive_stuffRate,defensive_lineYards,defensive_secondLevelYards,defensive_openFieldYards]
        metricsData.append(data)

    colNames_metrics = ['offensive_plays','offensive_drives','offensive_ppa','offensive_successRate','offensive_explosiveness',
                'offensive_powerSuccess','offensive_stuffRate','offensive_lineYards','offensive_secondLevelYards','offensive_openFieldYards',
                'defensive_plays','defensive_drives','defensive_ppa','defensive_successRate','defensive_explosiveness',
                'defensive_powerSuccess','defensive_stuffRate','defensive_lineYards','defensive_secondLevelYards','defensive_openFieldYards']
    
    return metricsData, colNames_metrics


