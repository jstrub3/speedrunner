import flask
from flask import jsonify, request, Response
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
    response_content = open('home.html').read()
    return Response(response_content, mimetype='text/html')

@app.route('/games/titles/all', methods=['GET'])
def game_titles_all():    
    return jsonify(games_helper.get_titles(databases['games']))

@app.route('/games/categories/all', methods=['GET'])
def game_categories_all():
    return jsonify(games_helper.get_categories(databases['games']))

@app.route('/games/categories/<string:game_title>', methods=['GET'])
def game_categories(game_title):
    return jsonify(games_helper.get_game_categories(databases['games'], game_title))

@app.route('/games/add/', methods=['POST'])
@app.route('/categories/add/', methods=['POST'])
def add_or_update_game():
    request_categories = []
    if 'game_title' in request.json:
        if 'categories' in request.json:
            request_categories = request.json['categories']
        games_helper.add_or_update_game(databases['games'], request.json['game_title'], request_categories)

        return '<p>Successfully added game </p>'
    else:
        return '<p>Unable to add game</p>'

@app.route('/speedruns/<string:game_title>/<string:category>', methods=['GET'])
def get_top_speedrun(game_title, category):
    print('game_title: ', game_title, ' category: ', category)

    speedruns = speedrun_helper.get_speedruns_by_game_and_category(databases['speedruns'], game_title, category)
    sorted_speedruns = sorted(speedruns, key=lambda x: x['duration'])
    
    #only return player name and duration
    for speedrun in sorted_speedruns: 
        speedrun.pop('game_title', None)
        speedrun.pop('category', None)
        speedrun.pop('id', None)

    return jsonify(sorted_speedruns)
    
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