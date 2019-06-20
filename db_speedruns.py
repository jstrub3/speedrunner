
import sqlite3 as sql
import logging
speedrunner_log = logging.getLogger(__name__)

def get_speedrun_id(con, player_id, game_id, category_id, duration):
    cur = con.cursor()
    return cur.execute("SELECT id FROM Speedruns WHERE player_id = '" + str(player_id) + "' AND \
        WHERE category_id = '" + str(category_id) + "' AND \
            game_id = '" + str(game_id) + "' AND \
                duration = '" + duration + "'").fetchone()[0]

def get_speedrun(con, id):
    cur = con.cursor()
    cur.execute("SELECT player_id, game_id, category_id, duration FROM \
        Speedruns WHERE id = '" + str(id) + "'").fetchone()[0]

def get_speedruns_by_player_id(con, player_id):
    cur = con.cursor()
    return cur.execute("SELECT game_id, category_id, duration \
        FROM Speedruns WHERE player_id = '" + str(player_id) + "' ORDER BY duration ASC").fetchall()

def get_speedruns_by_game_id(con, game_id):
    cur = con.cursor()
    return cur.execute("SELECT category_id, player_id, duration \
        FROM Speedruns WHERE game_id = '" + str(game_id) + "' ORDER BY duration ASC").fetchall()

def get_speedruns_by_game_id_and_category_id(con, game_id, category_id):
    cur = con.cursor()
    print('looking up speedruns for: ', game_id, category_id)
    return cur.execute("SELECT player_id, duration \
        FROM Speedruns WHERE game_id = '" + str(game_id) + "' AND category_id = '" + str(category_id) + "' ORDER BY duration ASC").fetchall()

def add_speedrun_by_id(con, player_id, game_id, category_id, duration):
        cur = con.cursor()
        speedrunner_log.info('Adding speedrun: playerid = ' + str(player_id) + 
        ', game_id = ' + str(game_id) + 
        ', category_id = ' + str(category_id) + 
        ', duration = ' + duration)
        cur.execute("INSERT OR IGNORE INTO Speedruns VALUES (?, ?, ?, ?, ?)", (None, player_id, game_id, category_id, duration) )
        con.commit()
        return cur.lastrowid

def add_speedruns(con, speedruns):
    speedrunner_log.info('Adding speedruns:' + str(speedruns))

    entries = []
    for speedrun in speedruns:
        entry = (None, speedrun['player_id'], speedrun['game_id'], speedrun['category_id'], speedrun['duration'])
        entries.append(entry)
        
    cur = con.cursor()
    cur.executemany("INSERT OR IGNORE INTO Speedruns VALUES (?, ?, ?, ?, ?)", entries )
    con.commit()

