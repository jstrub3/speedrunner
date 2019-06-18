import copy
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

@app.route('/players/all', methods=['GET'])
def players_all():
    return jsonify(databases['players'])

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
@app.route('/games/categories/add/', methods=['POST'])
def add_or_update_game():
    request_categories = []
    if 'game_title' in request.json:
        if 'categories' in request.json:
            request_categories = request.json['categories']
        games_helper.add_or_update_game(databases['games'], request.json['game_title'], request_categories)

        db_utils.save_database(databases['games'], 'games')
        return '<p>Successfully added game </p>'
    else:
        return '<p>Unable to add game</p>'

@app.route('/speedruns/add/', methods=['POST'])
def add_speedrun():
    if 'game_title' in request.json:
        if 'category' in request.json:
            if 'duration' in request.json:
                if 'player_name' in request.json:
                    speedrun_id = speedrun_helper.add_speedrun(databases['speedruns'], 
                    request.json['player_name'], 
                    request.json['game_title'], 
                    request.json['category'], 
                    request.json['duration'])

                    #speedrun id needs to be stored on the player as well
                    player_helper.add_or_update_player(databases['players'], request.json['player_name'], speedrun_id)
                    db_utils.save_database(databases['players'], 'players')
                    db_utils.save_database(databases['speedruns'], 'speedruns')

                    return '<p>Successfully added speedrun </p>'
    else:
        return '<p>Unable to add speedrun</p>'

@app.route('/speedruns/games/<string:game_title>/', defaults={'count': 0}, methods=['GET'])
@app.route('/speedruns/games/<string:game_title>/<int:count>', methods=['GET'])
def get_top_speedruns_by_category(game_title, count):
    #Because we pop unwanted elements off the speedrun objects, we need to 
    # deep copy the list upon retrieval
    speedruns = copy.deepcopy(speedrun_helper.get_speedruns_by_game(databases['speedruns'], game_title))
    sorted_speedruns = sorted(speedruns, key=lambda x: x['duration'])
    
    speedruns_by_category = {}

    for speedrun in sorted_speedruns:
        if speedrun['category'] not in speedruns_by_category:
            speedruns_by_category[speedrun['category']] = []

        speedruns_by_category[speedrun['category']].append(speedrun)
        speedrun.pop('game_title', None)
        speedrun.pop('category', None)

    if count > 0:
        for category in speedruns_by_category:
            speedruns_by_category[category] = speedruns_by_category[category][0:count]

    return jsonify(speedruns_by_category)

@app.route('/speedruns/games/<string:game_title>/<string:category>/', defaults={'count': 0}, methods=['GET'])
@app.route('/speedruns/games/<string:game_title>/<string:category>/<int:count>', methods=['GET'])
def get_top_speedruns(game_title, category, count):
    #Because we pop unwanted elements off the speedrun objects, we need to 
    # deep copy the list upon retrieval
    speedruns = copy.deepcopy(speedrun_helper.get_speedruns_by_game_and_category(databases['speedruns'], game_title, category))
    sorted_speedruns = sorted(speedruns, key=lambda x: x['duration'])
    
    #only return player name and duration
    for speedrun in sorted_speedruns: 
        speedrun.pop('game_title', None)
        speedrun.pop('category', None)
        speedrun.pop('id', None)

    if ( count > 0):
        return jsonify(sorted_speedruns[0:count])
    else:
        return jsonify(sorted_speedruns)
    
@app.route('/speedruns/players/<string:player_name>/', defaults={'count': 0}, methods=['GET'])
@app.route('/speedruns/players/<string:player_name>/<int:count>', methods=['GET'])
def get_speedruns_by_player(player_name, count):
    #Because we pop unwanted elements off the speedrun objects, we need to 
    # deep copy the list upon retrieval
    speedruns = copy.deepcopy(speedrun_helper.get_speedruns_by_player_name(databases['speedruns'], player_name))
    sorted_speedruns = sorted(speedruns, key=lambda x: x['duration'])
    
    #only return player name and duration
    for speedrun in sorted_speedruns: 
        speedrun.pop('id', None)
        speedrun.pop('player_name', None)

    if ( count > 0):
        return jsonify(sorted_speedruns[0:count])
    else:
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

    print('Valid games database: ', db_utils.validate_database_uniqueness(databases['games'], 'games', 'game_title'))
    print('Valid speedruns database: ', db_utils.validate_database_uniqueness(databases['speedruns'], 'speedruns', 'id'))
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