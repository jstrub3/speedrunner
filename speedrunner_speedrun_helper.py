import json
import uuid

def get_speedrun_by_id(speedruns_database, id):
    for speedrun in speedruns_database['speedruns']:
        if speedrun['id'] == id:
            return speedrun

def get_speedruns_by_player_name(speedruns_database, player_name):
    return_speedruns = []
    for speedrun in speedruns_database['speedruns']:
        if speedrun['player_name'] == player_name:
            return_speedruns.append(speedrun)
    return return_speedruns

def get_speedruns_by_game(speedruns_database, game_title):
    return_speedruns = []
    for speedrun in speedruns_database['speedruns']:
        if speedrun['game_title'] == game_title:
            return_speedruns.append(speedrun)
    return return_speedruns

def get_speedruns_by_game_and_category(speedruns_database, game_title, category):
    return_speedruns = []
    for speedrun in speedruns_database['speedruns']:
        if (speedrun['game_title'] == game_title
        and speedrun['category'] == category):
            return_speedruns.append(speedrun)
    return return_speedruns

def add_speedrun(speedruns_database, player_name, game_title, category, duration):
    for speedrun in speedruns_database['speedruns']:
        if (speedrun['player_name'] == player_name 
        and speedrun['game_title'] == game_title 
        and speedrun['category'] == category
        and speedrun['duration'] == duration):
            return None
    
    speedrun_id = str(uuid.uuid1())
    new_speedrun = {'id':speedrun_id, 'game_title':game_title, 'player_name':player_name, 'category':category, 'duration': duration}
    speedruns_database['speedruns'].append(new_speedrun)
    return speedrun_id
    
def delete_speedrun(speedruns_database, id):
    for speedrun in speedruns_database['speedruns'][:]:
        if speedrun['id'] == id:
            speedruns_database.remove(speedrun)