import sqlite3 as sql
import os
import csv
import logging
speedrunner_log = logging.getLogger(__name__)

import speedrunner_consts as consts

import db_games as Games
import db_categories as Categories
import db_games_categories as Games_Categories
import db_players as Players
import db_speedruns as Speedruns

def create_tables():
    with sql.connect(consts.DATABASE_PATH) as con:
        speedrunner_log.info('Creating tables...')

        con.execute('CREATE TABLE IF NOT EXISTS Games(id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT, CONSTRAINT game_unique UNIQUE (game))')
        con.execute('CREATE TABLE IF NOT EXISTS Categories(id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, CONSTRAINT category_unique UNIQUE (category))')
        con.execute('CREATE TABLE IF NOT EXISTS Players(id INTEGER PRIMARY KEY AUTOINCREMENT, player TEXT, CONSTRAINT player_unique UNIQUE (player))')
        con.execute('CREATE TABLE IF NOT EXISTS Speedruns(id INTEGER PRIMARY KEY AUTOINCREMENT, player_id INTEGER, game_id INTEGER, category_id INTEGER, duration TEXT, CONSTRAINT gamecategory_unique UNIQUE (game_id, category_id, duration, player_id))')
        con.execute('CREATE TABLE IF NOT EXISTS GamesCategories(id INTEGER PRIMARY KEY AUTOINCREMENT, game_id INTEGER, category_id INTEGER, CONSTRAINT gamecategory_unique UNIQUE (game_id, category_id))')
        con.commit()
    speedrunner_log.info('Tables created successfully')


def create_csv_entries(reader):
    keys = []
    for key in next(reader, None):
        keys.append(key)

    entries = []
    entry = []
    for line in reader:
        entry = {}
        for idx in range(len(line)):
            entry[keys[idx]] = line[idx]
        entries.append(entry)
    return entries

def init_from_csv(csv_name):
    with open(csv_name, mode='r') as csv_file:
        speedrunner_log.info('Parsing speedrun data from '+ csv_name)

        reader = csv.reader(csv_file)
        entries = create_csv_entries(reader)

        #Parse entries and add to the database
        with sql.connect(consts.DATABASE_PATH) as con:
            games = set()
            categories = set()
            players = set()

            for entry in entries:
                games.add(entry['Game'])
                categories.add(entry['Categories'])
                players.add(entry['Player'])

            #Bulk add games
            game_ids = Games.add_games(con, list(games))

            #Bulk add categories
            category_ids = Categories.add_categories(con, list(categories))
            
            #Bulk add players
            player_ids = Players.add_players(con, list(players))
            
            #Add table entries that rely on ids
            game_ids_dict = dict(game_ids)
            category_ids_dict = dict(category_ids)
            player_ids_dict = dict(player_ids)

            
            #This assigns a set of categories for a game_id
            # resulting in the format:
            # game_id:  3  categories:  [5]
            # game_id:  1  categories:  [1, 5]
            # game_id:  7  categories:  [4, 5, 6]
            game_categories_dict = {}
            for entry in entries:
                game = entry['Game']
                category = entry['Categories']
                
                game_id = game_ids_dict[game]
                category_id = category_ids_dict[category]

                if game_id not in game_categories_dict:
                    game_categories_dict[game_id] = set()

                game_categories_dict[game_id].add(category_id)

            #Bulk assign game category mapping table entries
            for game_id, category_ids in game_categories_dict.items():
                Games_Categories.add_game_categories_by_id(con, game_id, list(category_ids))

            
            #creates speedruns in the following format
            # {'player_id': 25, 'game_id': 9, 'category_id': 10, 'duration': '3:53:33'}
            # {'player_id': 14, 'game_id': 9, 'category_id': 10, 'duration': '4:20:00'}
            # {'player_id': 26, 'game_id': 9, 'category_id': 10, 'duration': '3:53:34'}
            # {'player_id': 34, 'game_id': 9, 'category_id': 10, 'duration': '3:58:22'}
            # {'player_id': 19, 'game_id': 9, 'category_id': 10, 'duration': '4:11:34'}
            speedruns = []
            for entry in entries:
                game = entry['Game']
                category = entry['Categories']
                player = entry['Player']
                duration = entry['Duration']
                
                game_id = game_ids_dict[game]
                category_id = category_ids_dict[category]
                player_id = player_ids_dict[player]
                
                speedrun = {}
                speedrun['player_id'] = player_id
                speedrun['game_id'] = game_id
                speedrun['category_id'] = category_id
                speedrun['duration'] = duration

                speedruns.append(speedrun)

            #Bulk add Speedruns
            Speedruns.add_speedruns(con, speedruns)