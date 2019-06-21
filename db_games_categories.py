
import sqlite3 as sql
import logging
speedrunner_log = logging.getLogger(__name__)

def get_categories_by_game_id(con, game_id):
        cur = con.cursor()
        rows = cur.execute("SELECT category_id FROM GamesCategories WHERE game_id = '" + str(game_id) + "' ORDER BY category_id DESC").fetchall()
        return [category_id[0] for category_id in rows]

def add_game_category_by_id(con, game_id, category_id):
        cur = con.cursor()
        cur.execute("INSERT OR IGNORE INTO GamesCategories VALUES (?, ?, ?)", (None, game_id, category_id) )
        con.commit()
        return cur.lastrowid

def add_game_categories_by_id(con, game_id, category_ids):
        speedrunner_log.info('Adding categories for game_id ' + str(game_id) + ': ' + str(category_ids))

        entries = []
        for id in category_ids:
                entries.append((None, game_id, id))

        cur = con.cursor()
        cur.executemany("INSERT OR IGNORE INTO GamesCategories VALUES (?, ?, ?)", entries )
        con.commit()