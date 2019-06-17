import json
import uuid

def get_player_by_name(players_database, name):
    for player in players_database['players']:
        if player['player_name'] == id:
            return player

def get_player_by_speedrun(players_database, speedrun_id):
    for player in players_database['players']:
        for speedrun_id in player['speedrun_ids']:
            if speedrun_id == speedrun_id:
                return player

def add_or_update_player(players_database, player_name, speedrun_id):
    for game in players_database['players']:
        if game['player_name'] == player_name:
            game['speedrun_ids'].append(speedrun_id)

            #using list->set->list paradigm to remove duplicate speedrun_ids
            game['speedrun_ids'] = list(set(game['speedrun_ids']))
            return  

    #unable to find existing player with this name, create new
    new_player = {'player_name':player_name, 'speedrun_ids':[]}
    new_player['speedrun_ids'].append(speedrun_id)  
    players_database['players'].append(new_player)
    
def delete_player(players_database, player_name):
    for player in players_database['players'][:]:
        if player['player_name'] == player_name:
            players_database.remove(player)