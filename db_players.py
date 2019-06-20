
import sqlite3 as sql

def get_player_id(con, player):
    cur = con.cursor()
    return cur.execute("SELECT id FROM Players WHERE player = '" + player + "'").fetchone()[0]

def get_player(con, id):
    cur = con.cursor()
    return cur.execute("SELECT player FROM Players WHERE id = '" + str(id) + "'").fetchone()[0]

def get_players(con):
    cur = con.cursor()
    return [player[0] for player in cur.execute("SELECT player FROM Players").fetchall()]

def add_player(con, player):
    cur = con.cursor()

    #check for existing player
    result = cur.execute("SELECT id FROM Players WHERE player = ?", [player]).fetchone()

    if result == None:
        cur.execute("INSERT INTO Players VALUES (?, ?)", (None, player) )
        con.commit()
        return cur.lastrowid
    else:
        return result[0]

def add_players(con, players):
    entries = []
    for player in players:
        entries.append((None, player))

    cur = con.cursor()
    cur.executemany("INSERT OR IGNORE INTO Players VALUES (?, ?)", entries )
    con.commit()

    return cur.execute("SELECT player, id FROM Players WHERE player IN ({0})"
        .format(', '.join('?' for _ in players)), players).fetchall()

