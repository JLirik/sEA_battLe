import sqlite3
import json


def init_database():
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                   userid INTEGER PRIMARY KEY,
                   login TEXT UNIQUE,
                   password TEXT,
                   mail TEXT UNIQUE,
                   name TEXT,
                   is_admin INTEGER DEFAULT 0,
                   avaliable_fields TEXT DEFAULT '');
                """)
    cur.execute("""CREATE TABLE IF NOT EXISTS fields(
                   field_id INTEGER PRIMARY KEY,
                   field_info TEXT,
                   field_users TEXT DEFAULT '{}',
                   field_name TEXT UNIQUE,
                   field_prizes TEXT DEFAULT '{}');
                    """)
    con.commit()
    return True


def add_user(login, password, mail, name, is_admin):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    try:
        cur.execute("""INSERT INTO users (login, password, mail, name, is_admin) 
                           VALUES (?, ?, ?, ?, ?)
                        """, (login, password, mail, name, is_admin,))
        con.commit()
    except Exception as e:
        return str(e)[26:]
    return 0


def log_in(login, passw):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    try:
        pwd = cur.execute("""SELECT password FROM users WHERE login=?""", (login,)).fetchone()[0]
    except TypeError:
        return False
    if passw == pwd:
        return True
    return False


def adm_chck(login):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    adm = cur.execute("""SELECT is_admin FROM users WHERE login=?""", (login,)).fetchone()[0]
    return adm


def add_field(field, prizes, name):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    try:
        cur.execute("""INSERT INTO fields (field_info, field_name, field_prizes) 
                           VALUES (?, ?, ?)
                        """, (field, name, json.dumps(prizes),))
        con.commit()
    except Exception as e:
        return str(e)[26:]
    return 0


def add_user_to_field(login, field_id, shots):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    fields = cur.execute("""SELECT avaliable_fields FROM users
                           WHERE login=?""", (login,)).fetchone()[0]
    fields += f', {field_id}'
    cur.execute("""UPDATE users SET avaliable_fields = ? WHERE login=? """, (fields, login,))
    con.commit()
    users = cur.execute("""SELECT field_users FROM fields
                               WHERE field_id=?""", (field_id,)).fetchone()[0]
    a = json.loads(users)
    a[login] = shots
    cur.execute("""UPDATE fields SET field_users = ? WHERE field_id=?
                        """, (json.dumps(a), field_id,))
    con.commit()
    return True


def get_fields():
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    fields = cur.execute("""SELECT * FROM fields""").fetchall()
    return fields


def get_field(field_id):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    fields = cur.execute("""SELECT * FROM fields WHERE field_id = ?""", (field_id,)).fetchall()[0]
    return fields


def get_user_fields(user):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    fields = cur.execute("""SELECT avaliable_fields FROM users WHERE login=?""", (user,)).fetchall()[0][0].split(', ')
    ret = []
    for el in fields:
        if el:
            tmp = get_field(el)
            changed = json.loads(tmp[2])[user]
            ret.append((tmp[0], tmp[1], changed, tmp[3], tmp[4]))
    return ret


def save_map_ch(field_id, new_map):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    cur.execute("""UPDATE fields SET field_info = ? WHERE field_id=?
                            """, (new_map, field_id,))
    con.commit()
    return True


# add_user_to_field('89685433354', 1, 105)
# add_field('----k---', {1: 'govna', 2: 'bullshit'}, 'suka')
# /user/maps?login=SeliverstovDm.
