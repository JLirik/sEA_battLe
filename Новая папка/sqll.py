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
                   prizes TEXT DEFAULT ', ',
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
    cur.execute("""CREATE TABLE IF NOT EXISTS prizes(
                       prize_id INTEGER PRIMARY KEY,
                       name TEXT UNIQUE,
                       symbol TEXT UNIQUE,
                       about TEXT);
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
        return False
    return True


def add_prize(name, smb, about):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    try:
        cur.execute("""INSERT INTO prizes (name, symbol, about) VALUES (?, ?, ?)""", (name, smb, about,))
        con.commit()
    except Exception as e:
        return str(e)[26:]
    return 0


def add_prizes_to_user(login, prizes):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    prs = cur.execute("""SELECT prizes FROM users
                               WHERE login=?""", (login,)).fetchone()[0]
    prs = prs.split(', ')
    prs.extend(prizes)
    cur.execute("""UPDATE users SET prizes = ? WHERE login=? """, (', '.join(prs), login,))
    con.commit()
    return True


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
    a[login] = int(shots)
    cur.execute("""UPDATE fields SET field_users = ? WHERE field_id=?
                        """, (json.dumps(a), field_id,))
    con.commit()
    return True
    
def add_user_to_field_2(login, field_id, shots):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    users = cur.execute("""SELECT field_users FROM fields
                               WHERE field_id=?""", (field_id,)).fetchone()[0]
    a = json.loads(users)
    a[login] = int(shots)
    cur.execute("""UPDATE fields SET field_users = ? WHERE field_id=?
                        """, (json.dumps(a), field_id,))
    con.commit()
    return True

def redact_prize(pr_id, name, smb, about):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    cur.execute("""UPDATE prizes SET name = ?, symbol = ?, about=? WHERE prize_id=?
                                """, (name, smb, about, pr_id,))
    con.commit()
    return True


def get_prize_by_smb(smb):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    prz = cur.execute("""SELECT * FROM prizes WHERE symbol = ?""", (smb,)).fetchall()[0]
    return prz

def get_fields():
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    fields = cur.execute("""SELECT * FROM fields""").fetchall()
    return fields


def get_prizes():
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    pr = cur.execute("""SELECT * FROM prizes""").fetchall()
    return pr


def get_prize(smb):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    pr = cur.execute("""SELECT * FROM prizes WHERE symbol=?""", (smb,)).fetchall()[0]
    return pr


def get_user_prizes(login):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    pr = cur.execute("""SELECT prizes FROM users WHERE login=?""", (login,)).fetchall()
    return pr


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


def save_map_ch(field_id, new_map, new_users):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    cur.execute("""UPDATE fields SET field_info = ?, field_users = ? WHERE field_id=?
                            """, (new_map, json.dumps(new_users), field_id,))
    con.commit()
    return True


def redact_fields(field_id, field_info, name):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    try:
        cur.execute("""UPDATE fields SET field_name = ?, field_info = ? WHERE field_id=? """, (name, field_info, field_id,))
        con.commit()
    except Exception as e:
        return False
    return True


def delete_map(field_id):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    field = get_field(field_id)
    if '#' in field[1]:
        return False
    cur.execute("""DELETE FROM fields WHERE field_id=? 
                            """, (field_id,))
    a = get_users()
    for j in a:
        if str(field_id) in j[7]:
            c = j[7][2:].split(', ')
            d = ''
            for i in c:
                if i != str(field_id):
                    d += ', ' + i
            j2 = j
            j = tuple(
                item for item in j if item != j[1]
            )
            j = list(j)
            j.insert(7, d)
            j1 = tuple(j)
            a.insert(a.index(j2), j1)
            a.remove(j2)
    for i in a:
        cur.execute("""UPDATE users SET avaliable_fields = ? WHERE userid=?
                                    """, (i[7], i[0],))
    con.commit()
    return True

def delete_user_from_field(login, field_id):
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    print(login)
    print(field_id)
    fields = cur.execute("""SELECT avaliable_fields FROM users WHERE login=?""", (login,)).fetchone()
    res = []
    print(fields)
    # for el in fields.split(', '):
    #     if el != str(field_id):
    #         res.append(el)
    print(res)
    cur.execute("""UPDATE users SET avaliable_fields = ? WHERE login=? """, (', '.join(res), login,))
    con.commit()
    users = cur.execute("""SELECT field_users FROM fields WHERE field_id=?""", (field_id,)).fetchone()[0]
    a = json.loads(users)
    res = {}
    for el in a:
        if el != login:
            res[el] = a[el]
    cur.execute("""UPDATE fields SET field_users = ? WHERE field_id=?""", (json.dumps(res), field_id,))
    con.commit()
    return True


def get_users():
    con = sqlite3.connect('predprof.db')
    cur = con.cursor()
    users = cur.execute("""SELECT * FROM users""").fetchall()
    return users


# add_user_to_field('89685433354', 1, 105)
# add_field('----k---', {1: 'govna', 2: 'bullshit'}, 'suka')
# /user/maps?login=SeliverstovDm.
