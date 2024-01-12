import sqlite3


def init_database(root):
    print(1)
    con = sqlite3.connect(root)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                   userid INTEGER PRIMARY KEY,
                   login TEXT UNIQUE DEFAULT '',
                   password TEXT DEFAULT NULL,
                   mail TEXT UNIQUE,
                   is_admin INTEGER DEFAULT 0);
                """)
    con.commit()
    return True
