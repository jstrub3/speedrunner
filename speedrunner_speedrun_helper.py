import json
import uuid

def get_speedrun_by_id(speedruns_database, id):
    for speedrun in speedruns_database['speedruns']:
        if speedrun['id'] == id:
            return speedrun

def get_speedruns_by_player_id(speedruns_database, player_id):
    return_speedruns = []
    for speedrun in speedruns_database['speedruns']:
        if speedrun['player_id'] == player_id:
            return_speedruns.append(speedrun)
    return return_speedruns

def add_speedrun(speedruns_database, player_id, game_title, category, duration):
    for speedrun in speedruns_database['speedruns']:
        if (speedrun['player_id'] == player_id 
        and speedrun['game_title'] == game_title 
        and speedrun['category'] == category
        and speedrun['duration'] == duration):
            #print('Duplicate speedrun detected for player ', player_id, ' on game ', game_title, ' ', category, ' for duration ', duration, '!')
            return None
    
    speedrun_id = str(uuid.uuid1())
    new_speedrun = {'id':speedrun_id, 'game_title':game_title, 'player_id':player_id, 'category':category, 'duration': duration}
    speedruns_database['speedruns'].append(new_speedrun)
    return speedrun_id
    
def delete_speedrun(speedruns_database, id):
    for speedrun in speedruns_database['speedruns'][:]:
        if speedrun['id'] == id:
            speedruns_database.remove(speedrun)