import flask
from flask import jsonify, request
import speedrunner_consts as consts
import speedrunner_db_utilities as db_utils
import speedrunner_games_helper as games_helper
import speedrunner_speedrun_helper as speedrun_helper
import speedrunner_player_helper as player_helper

app = flask.Flask(__name__)
app.config["DEBUG"] = consts.IS_DEBUG

databases = {}


@app.route('/', methods=['GET'])
def home():
    return "<p>Speedrunner API initialized successfully</p>"

@app.route('/games/titles/all', methods=['GET'])
def game_titles_all():
    return_game_titles = []
    for game in databases['games']['games']:
        return_game_titles.append(game['game_title'])
    
    return jsonify(return_game_titles)

@app.route('/games/categories/', methods=['GET'])
def game_categories_all():
    return_categories = []
    for game in databases['games']['games']:
        for category in game['categories']:
            return_categories.append(category)
    return_categories = list(set(return_categories))
    return jsonify(return_categories)

@app.route('/games/categories/<string:game_title>', methods=['GET'])
def game_categories(game_title):
    for game in databases['games']['games']:
        if game['game_title'] == game_title:
            return jsonify(game['categories'])

    
def initialize_databases():
    for name in consts.REQUIRED_DATABASES:
        databases[name] = db_utils.load_database(name)

    #add any from the seed csv
    csv_list = db_utils.get_data_from_csv(consts.SEED_DATA_FILENAME)
    for entry in csv_list:
        games_helper.add_or_update_game(databases['games'], entry['Game'], entry['Categories'])
        speedrun_id = speedrun_helper.add_speedrun(databases['speedruns'], entry['Player'], entry['Game'], entry['Categories'], entry['Duration'])

        if speedrun_id:
            player_helper.add_or_update_player(databases['players'], entry['Player'], speedrun_id)

    #print('Updated games database:')
    #db_utils.print_database(databases['games'])
    print('Valid games database: ', db_utils.validate_database_uniqueness(databases['games'], 'games', 'game_title'))

    #print('Updated speedrun database:')
    #db_utils.print_database(databases['speedruns'])
    print('Valid speedruns database: ', db_utils.validate_database_uniqueness(databases['speedruns'], 'speedruns', 'id'))

    #print('Updated player database:')
    #db_utils.print_database(databases['players'])
    print('Valid players database: ', db_utils.validate_database_uniqueness(databases['players'], 'players', 'player_name'))

    if len(csv_list) > 0:
        print('Added or updated ', len(csv_list), ' speedruns from seed data, saving databases...')
        db_utils.save_database(databases['games'], 'games')
        db_utils.save_database(databases['players'], 'players')
        db_utils.save_database(databases['speedruns'], 'speedruns')

if __name__ == '__main__':
    print ('Starting speedrunner_server')

    initialize_databases()

    app.run(port='5002', use_reloader=False)
    print ('Closing speedrunner_server')