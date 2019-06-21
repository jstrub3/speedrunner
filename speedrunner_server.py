import flask
from flask import jsonify, request, Response

from datetime import datetime
import logging as speedrunner_log
import sqlite3 as sql

import speedrunner_consts as consts
import speedrunner_db as db
import db_games as Games
import db_categories as Categories
import db_games_categories as Games_Categories
import db_players as Players
import db_speedruns as Speedruns

app = flask.Flask(__name__)
app.config["DEBUG"] = consts.IS_DEBUG

database_path = consts.DATABASE_PATH

#Home page
@app.route('/', methods=['GET'])
def home():
    response_content = open('home.html').read()
    return Response(response_content, mimetype='text/html')

#Get all players
@app.route('/players/all', methods=['GET'])
def players_all():
    with sql.connect(database_path) as con:
        players = Players.get_players(con)
        return jsonify(players)

#Get all games
@app.route('/games/titles/all', methods=['GET'])
def game_titles_all():    
    with sql.connect(database_path) as con:
        games = Games.get_games(con)
        return jsonify(games)

#Get all categories
@app.route('/games/categories/all', methods=['GET'])
def game_categories_all():
    with sql.connect(database_path) as con:
        categories = Categories.get_categories(con)
        return jsonify(categories)

#Get all categories for a game
@app.route('/games/categories/<string:game_title>', methods=['GET'])
def game_categories(game_title):
    with sql.connect(database_path) as con:
        game_id = Games.get_game_id(con, game_title)
        category_ids = Games_Categories.get_categories_by_game_id(con, game_id)

        categories = []
        for category_id in category_ids:
            categories.append(Categories.get_category(con, category_id))

        return jsonify(categories)

#Add game title
#Add category(ies) to a game
@app.route('/games/add/', methods=['POST'])
@app.route('/games/categories/add/', methods=['POST'])
def add_or_update_game():
    with sql.connect(database_path) as con:
        if 'game_title' in request.json:
            game_id = Games.add_game(con, request.json['game_title'])
            if 'categories' in request.json:
                category_ids = Categories.add_categories(con, request.json['categories'])
                category_ids = [id[1] for id in category_ids]
                Games_Categories.add_game_categories_by_id(con, game_id, category_ids)
            return '<p>Successfully added game </p>'
    return '<p>Unable to add game</p>'

#Add speedrun
@app.route('/speedruns/add/', methods=['POST'])
def add_speedrun():
    if 'game_title' in request.json:
        if 'category' in request.json:
            if 'duration' in request.json:
                if 'player_name' in request.json:
                    with sql.connect(database_path) as con:
                        game_id = Games.add_game(con, request.json['game_title'])
                        category_id = Categories.add_category(con, request.json['category'])
                        player_id = Players.add_player(con, request.json['player_name'])
                        
                        #add or confirm the game-category mapping table entry
                        Games_Categories.add_game_category_by_id(con, game_id, category_id)
                        
                        #add the actual speedrun
                        Speedruns.add_speedrun_by_id(con, player_id, game_id, category_id, request.json['duration'])

                        return '<p>Successfully added speedrun </p>'
    return '<p>Unable to add speedrun</p>'

#Get the top <count> speedruns for a game, arranged by category
@app.route('/speedruns/games/<string:game_title>/', defaults={'count': -1}, methods=['GET'])
@app.route('/speedruns/games/<string:game_title>/<int:count>', methods=['GET'])
def get_top_speedruns_by_game_by_category(game_title, count):

    with sql.connect(database_path) as con:
        game_id = Games.get_game_id(con, game_title)
        speedruns_tuple = Speedruns.get_speedruns_by_game_id(con, game_id)

        speedruns = {}
        for speedrun_tuple in speedruns_tuple:
            speedrun_category = Categories.get_category(con, speedrun_tuple[0])
            
            speedrun = {}
            speedrun['player'] = Players.get_player(con, speedrun_tuple[1])
            speedrun['duration'] = speedrun_tuple[2]

            if speedrun_category not in speedruns:
                speedruns[speedrun_category] = []

            #This is hacky
            if count >= 0:
                if len(speedruns[speedrun_category]) < count:
                    speedruns[speedrun_category].append(speedrun)
            else:
                speedruns[speedrun_category].append(speedrun)
        
        return jsonify(speedruns)   

#Get top <count> speedruns by game and category
@app.route('/speedruns/games/<string:game_title>/<string:category>/', defaults={'count': -1}, methods=['GET'])
@app.route('/speedruns/games/<string:game_title>/<string:category>/<int:count>', methods=['GET'])
def get_top_speedruns_by_game_and_category(game_title, category, count):

    with sql.connect(database_path) as con:
        game_id = Games.get_game_id(con, game_title)
        category_id = Categories.get_category_id(con, category)

        speedruns_tuple = Speedruns.get_speedruns_by_game_id_and_category_id(con, game_id, category_id)

        speedruns = []
        for speedrun_tuple in speedruns_tuple:
            speedrun = {}
            speedrun['player'] = Players.get_player(con, speedrun_tuple[0])
            speedrun['duration'] = speedrun_tuple[1]
            speedruns.append(speedrun)
            
            count = count - 1
            if count == 0:
                break
        
        return jsonify(speedruns)    

#Get top <count> speedruns by player name
@app.route('/speedruns/players/<string:player_name>/', defaults={'count': -1}, methods=['GET'])
@app.route('/speedruns/players/<string:player_name>/<int:count>', methods=['GET'])
def get_speedruns_by_player(player_name, count):
    with sql.connect(database_path) as con:
        player_id = Players.get_player_id(con, player_name)
        speedruns_tuple = Speedruns.get_speedruns_by_player_id(con, player_id)

        speedruns = []
        for speedrun_tuple in speedruns_tuple:
            speedrun = {}
            speedrun['game_title'] = Games.get_game(con, speedrun_tuple[0])
            speedrun['category'] = Categories.get_category(con, speedrun_tuple[1])
            speedrun['duration'] = speedrun_tuple[2]
            speedruns.append(speedrun)
            
            count = count - 1
            if count == 0:
                break
        
        return jsonify(speedruns)    

def init_logging(log, datetime):
    log_file_name = './log/speedrunner_' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.log'
    speedrunner_log.basicConfig(filename=log_file_name, level=speedrunner_log.DEBUG, format = '%(asctime)s:%(levelname)s:%(message)s')
    speedrunner_log.getLogger().addHandler(speedrunner_log.StreamHandler())

if __name__ == '__main__':
    init_logging(speedrunner_log, datetime)

    speedrunner_log.info('Starting speedrunner_api server...')

    db.create_tables(database_path)
    db.init_from_csv(consts.SEED_DATA_PATH, database_path)

    app.run(port='5002', use_reloader=False)
    speedrunner_log.info('Closing speedrunner_server...')