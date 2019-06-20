
import sqlite3 as sql

def get_category_id(con, category):
    cur = con.cursor()
    return cur.execute("SELECT id FROM Categories WHERE category = '" + category + "'").fetchone()[0]

def get_category(con, id):
    cur = con.cursor()
    return cur.execute("SELECT category FROM Categories WHERE id = '" + str(id) + "'").fetchone()[0]

def get_categories(con):
    cur = con.cursor()
    return [category[0] for category in cur.execute("SELECT category FROM Categories").fetchall()]

def add_category(con, category):
    cur = con.cursor()

    #check for existing category
    result = cur.execute("SELECT id FROM Categories WHERE category = '" + category + "'").fetchone()

    if result == None:
        cur.execute("INSERT INTO Categories VALUES (?, ?)", (None, category) )
        con.commit()
        return cur.lastrowid
    else:
        return result[0]

def add_categories(con, categories):
    entries = []
    for category in categories:
        entries.append((None, category))

    cur = con.cursor()
    cur.executemany("INSERT OR IGNORE INTO Categories VALUES (?, ?)", entries )
    con.commit()

    return cur.execute("SELECT category, id FROM Categories WHERE category IN ({0})"
        .format(', '.join('?' for _ in categories)), categories).fetchall()
