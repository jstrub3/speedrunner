import json

def get_game_by_name(games_database, title):
    for game in games_database['games']:
        if game['game_title'] == title:
            return game

def get_games_by_category(games_database, category):
    return_games = []
    for game in games_database['games']:
        if game['categories'] == category:
            return_games.append(game)
    return return_games

def add_or_update_game(games_database, title, category):
    for game in games_database['games']:
        if game['game_title'] == title:
            game['categories'].append(category)

            #using list->set->list paradigm to remove duplicate categories
            game['categories'] = list(set(game['categories']))
            return  

    #unable to find existing game with this title, create new
    new_game = {'game_title':title, 'categories':[]}
    new_game['categories'].append(category)  
    games_database['games'].append(new_game)
    
def delete_game(games_database, title):
    for game in games_database['games'][:]:
        if game['game_title'] == title:
            games_database.remove(game)