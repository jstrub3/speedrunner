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

def get_game_categories(games_database, title):
    for game in games_database['games']:
        if game['game_title'] == title:
            return game['categories']

def get_categories(games_database):
    return_categories = []
    for game in games_database['games']:
        for category in game['categories']:
            return_categories.append(category)
    return_categories = list(set(return_categories))
    return return_categories

def get_titles(games_database):
    return_game_titles = []
    for game in games_database['games']:
        return_game_titles.append(game['game_title'])
    return return_game_titles

def add_or_update_game(games_database, title, category):
    for game in games_database['games']:
        if game['game_title'] == title:

            if isinstance(category, str):
                game['categories'].append(category)
            elif isinstance(category, list): 
                game['categories'].extend(category)

            #using list->set->list paradigm to remove duplicate categories
            game['categories'] = list(set(game['categories']))
            return

    #unable to find existing game with this title, create new
    new_game = {'game_title':title, 'categories':[]}
    
    if isinstance(category, str):
        new_game['categories'].append(category)
    elif isinstance(category, list): 
        new_game['categories'].extend(category)

    games_database['games'].append(new_game)
    
def delete_game(games_database, title):
    for game in games_database['games'][:]:
        if game['game_title'] == title:
            games_database.remove(game)