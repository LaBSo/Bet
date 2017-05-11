import pandas as pd
import numpy as np
import sqlite3
# from arb import replaceNull
# from datetime import timedelta
import warnings

warnings.filterwarnings("ignore")

# load data (make sure you have downloaded database.sqlite)
with sqlite3.connect('C:/Users/Omistaja/Dropbox/Betting/Soccer/database.sqlite') as con:
    countries = pd.read_sql_query("SELECT * from Country", con)
    matches = pd.read_sql_query("SELECT * from Match", con)
    leagues = pd.read_sql_query("SELECT * from League", con)
    teams = pd.read_sql_query("SELECT * from Team", con)

selected_countries = ['Scotland', 'France', 'Germany', 'Italy', 'Spain', 'Portugal', 'England']
countries = countries[countries.name.isin(selected_countries)]
leagues = countries.merge(leagues, on='id', suffixes=('', '_y'))

# There's a special character in the long name "Atlético Madrid".
# This can be a pain in the ass, so I'm gonna change it for simplicity.
# teams.loc[teams.team_api_id == 9906,"team_long_name"] = "Atletico Madrid"

matches = matches[matches.date >= '2011-08-01']
matches = matches[matches.league_id.isin(leagues.id)]
matches = matches[['id', 'country_id', 'league_id', 'season', 'stage', 'date', 'match_api_id', 'home_team_api_id',
                   'away_team_api_id', 'home_team_goal', 'away_team_goal', 'B365H', 'B365D', 'B365A', 'BWH', 'BWD',
                   'BWA', 'IWH', 'IWD', 'IWA',
                   'LBH', 'LBD', 'LBA', 'PSH', 'PSD', 'PSA', 'WHH', 'WHD', 'WHA', 'SJH', 'SJD', 'SJA',
                   'VCH', 'VCD', 'VCA', 'GBH', 'GBD', 'GBA', 'BSH', 'BSD', 'BSA']]

# matches.dropna(inplace=True)
matches = matches.merge(teams, left_on='home_team_api_id', right_on='team_api_id', suffixes=('', '_h'))
matches = matches.merge(teams, left_on='away_team_api_id', right_on='team_api_id', suffixes=('', '_a'))
matches = matches[['id', 'season', 'date', 'home_team_goal', 'away_team_goal', 'B365H', 'BWH', 'IWH', 'LBH', 'PSH',
                   'WHH', 'SJH', 'VCH', 'GBH', 'BSH','team_long_name', 'team_long_name_a']]


# Look the results
matches['result'] = 'H'
matches.loc[matches.home_team_goal == matches.away_team_goal, "result"] = 'D'
matches.loc[matches.home_team_goal < matches.away_team_goal, "result"] = 'A'

# Betting rule
matches['payout'] = matches[['B365H', 'BWH', 'IWH', 'LBH', 'PSH', 'WHH', 'SJH',
                 'VCH', 'GBH', 'BSH']].max(axis=1)

# our team either lost or drew. reset payout to 0
matches.loc[~(matches.result == 'H'), "payout"] = 0
matches.head()

# sort by date
matches = matches.sort_values(by='date')

print(matches.head())
