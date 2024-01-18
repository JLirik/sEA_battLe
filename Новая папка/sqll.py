import sqlite3


def init_database():
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                   userid INTEGER PRIMARY KEY,
                   login TEXT UNIQUE,
                   password TEXT,
                   mail TEXT UNIQUE,
                   is_admin INTEGER DEFAULT 0,
                   avaliable_fields TEXT DEFAULT '');
                """)
    cur.execute("""CREATE TABLE IF NOT EXISTS fields(
                   field_id INTEGER PRIMARY KEY,
                   field_info TEXT,
                   field_users TEXT DEFAULT '');
                    """)
    con.commit()
    return True


def add_user(login, password, mail, is_admin):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    cur.execute("""INSERT INTO accounts (login, password, mail, is_admin) 
                       VALUES (?, ?, ?, ?)
                    """, (login, password, mail, is_admin))
    con.commit()
    return True


def add_field(field):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    cur.execute("""INSERT INTO fields (field_info) 
                       VALUES (?)
                    """, (field,))
    con.commit()
    return True


def add_user_to_field(login, field_id):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    fields = cur.execute("""SELECT avaliable_fields FROM accounts
                           WHERE login=?""", (login,)).fetchone()[0]
    fields += f', {field_id}'
    cur.execute("""INSERT INTO accounts (avaliable_fields) 
                       VALUES (?) WHERE login=?
                    """, (fields, login,))
    con.commit()
    users = cur.execute("""SELECT field_users FROM fields
                               WHERE field_id=?""", (field_id,)).fetchone()[0]
    users += f', {login}'
    cur.execute("""INSERT INTO fields (field_users) 
                           VALUES (?) WHERE field_id=?
                        """, (users, field_id,))
    con.commit()
    return True