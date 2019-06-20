
import sqlite3 as sql
import logging
speedrunner_log = logging.getLogger(__name__)


def get_game_id(con, game):
    cur = con.cursor()
    return cur.execute("SELECT id FROM Games WHERE game = '" + game + "'").fetchone()[0]

def get_game(con, id):
    cur = con.cursor()
    return cur.execute("SELECT game FROM Games WHERE id = '" + str(id) + "'").fetchone()[0]

def get_games(con):
    cur = con.cursor()
    return [game[0] for game in cur.execute("SELECT game FROM Games").fetchall()]

def add_game(con, game):
    cur = con.cursor()

    #check for existing game
    result = cur.execute("SELECT id FROM Games WHERE game = '" + game + "'").fetchone()

    if result == None:
        speedrunner_log.info('Adding game:' + game)
        
        cur.execute("INSERT INTO Games VALUES (?, ?)", (None, game) )
        con.commit()
        return cur.lastrowid
    else:
        return result[0]

def add_games(con, games):
    speedrunner_log.info('Adding games:' + str(games))

    entries = []
    for game in games:
        entries.append((None, game))

    cur = con.cursor()
    cur.executemany("INSERT OR IGNORE INTO Games VALUES (?, ?)", entries )
    con.commit()

    return cur.execute("SELECT game, id FROM Games WHERE game IN ({0})"
        .format(', '.join('?' for _ in games)), games).fetchall()
