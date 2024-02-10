import json

from flask import Flask, url_for, request, render_template, redirect, flash
from sqll import *
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'predpof_code_crusaders'
init_database()
files = ['jpg', 'png', 'jpeg']

class SizeForm(FlaskForm):
    size = IntegerField('Размер', validators=[DataRequired()])
    submit = SubmitField('Создать')

@app.route('/', methods=['GET'])
def first():
    return render_template('first_page.html', style=url_for('static', filename='css/css_for_reg.css'))


# @app.route('/', methods=['POST'])
# def first_post():
#     button_pressed = request.form["but"]
#     if button_pressed == 'Регистрация':
#         return redirect('/reg')
#     else:
#         pass


@app.route('/reg', methods=['GET'])
def reg():
    return render_template('registration_unit.html')


@app.route('/reg', methods=['POST'])
def reg_post():
    is_admin = 1 if request.form['admin'] == 'AdmCd.exe' else 0
    sql_ret = add_user(request.form['login'], request.form['password'],
                       request.form['email'], f"{request.form['name']} {request.form['surname']}",
                       is_admin)
    if sql_ret == 0:
        if is_admin:
            return redirect(url_for('admin_main', login=request.form['login']))
        return redirect(url_for('usr_maps', login=request.form['login']))
    else:
        if sql_ret == 'users.mail':
            msg = 'ая почта'
        else:
            msg = 'ый логин'
        flash(f'Указанн{msg} уже существует')
        return render_template('registration_unit.html')


@app.route('/log_in', methods=['GET'])
def login():
    return render_template('log_in.html')


@app.route('/log_in', methods=['POST'])
def login_post():
    user, passw = request.form['login'], request.form['password']
    sql_ret = log_in(user, passw)
    if sql_ret:
        is_admin = adm_chck(user)
        if is_admin:
            return redirect(url_for('admin_main', login=request.form['login']))
        return redirect(url_for('usr_maps', login=request.form['login']))
    else:
        flash(f'Логин или пароль указаны неправильно')
        return render_template('log_in.html')


@app.route('/admin/main', methods=['GET'])
def admin_main():
    def post_game(data, name):
        a = ''
        tmp = int(len(data) ** 0.5)
        for i in range(0, len(data), tmp):
            a += data[i:i + tmp] + '\n'
        tupo = add_field(a.strip(), {}, name)
        if not tupo:
            flash('Карта с таким названием уже сущетсвует!')
            flash('Дайте карте уникальное имя.')
            return render_template('index.html', style=url_for('static', filename='css/css_for_reg.css'),
                                   gifts=gift_lst, size=size, login=login)

        return True

    def check(map_1):
        n = len(map_1)
        for y in range(n):
            for x in range(n):
                if map_1[y][x] not in ("-", '#'):
                    if x < n - 1:
                        if map_1[y][x + 1] not in ("-", '#'):
                            return True
                        if y < n - 1:
                            if map_1[y + 1][x] not in ("-", '#'):
                                return True
                            if map_1[y + 1][x + 1] not in ("-", '#'):
                                return True
                        if y > 0:
                            if map_1[y - 1][x] not in ("-", '#'):
                                return True
                            if map_1[y - 1][x + 1] not in ("-", '#'):
                                return True
                    elif y < n - 1 and map_1[y + 1][x] not in ("-", '#'):
                        return True
                    elif y > 0 and map_1[y - 1][x] not in ("-", '#'):
                        return True
        return False

    name = request.args.get('name')
    name1 = request.args.get('name1')
    field = request.args.get('field')
    data = request.args.get('data')
    login = request.args.get('login')
    number = request.args.get('tentacles')
    text = request.args.get('tentacles1')
    id_f = request.args.get('id_file')
    map_id = request.args.get('map')
    map_id_1 = request.args.get('map1')
    field_id = request.args.get('field_id')
    login_user = request.args.get('login_user')

    if not login:
        return redirect('/')
    if data:
        data = request.args.get('data').replace(' ', '-')

        gift_lst = get_prizes()
        b = ''
        tmp = int(len(data) ** 0.5)
        for i in range(0, len(data), tmp):
            b += data[i:i + tmp] + '\n'
        size = len(b.split('\n')[:-1])

        if check(b.split('\n')[:-1]):
            flash('Нельзя ставить два корабля рядом')
            if id_f:
                map_lst = get_field(id_f)
                karta = map_lst[1].split('\n')

                not_to_red = False
                if '#' in map_lst[1]:
                    not_to_red = True
                return render_template('redact_field.html', data=karta, red=not_to_red, f_name=map_lst[3],
                                       id_f=map_lst[0], login=login, size=len(karta), gifts=gift_lst)

            return render_template('index.html', style=url_for('static', filename='css/css_for_reg.css'),
                                   gifts=gift_lst, size=size, login=login)

        if text == '':
            flash('Назовите поле!')
            if id_f:
                map_lst = get_field(id_f)
                karta = map_lst[1].split('\n')

                not_to_red = False
                if '#' in map_lst[1]:
                    not_to_red = True
                return render_template('redact_field.html', data=karta, red=not_to_red, f_name=map_lst[3],
                                       id_f=map_lst[0], login=login, size=len(karta), gifts=gift_lst)
            return render_template('index.html', style=url_for('static', filename='css/css_for_reg.css'),
                                   gifts=gift_lst, size=size, login=login)

        if data.count('-') != len(data):
            are_gifts = [e[2] for e in get_prizes()]

            for e in data:
                if e not in are_gifts and e not in ('-', '#'):
                    flash(f'Не существует приза {e}')
                    if id_f:
                        map_lst = get_field(id_f)
                        karta = map_lst[1].split('\n')

                        not_to_red = False
                        if '#' in map_lst[1]:
                            not_to_red = True
                        return render_template('redact_field.html', data=karta, red=not_to_red, f_name=map_lst[3],
                                               id_f=map_lst[0], login=login, size=len(karta), gifts=gift_lst)
                    return render_template('index.html', style=url_for('static', filename='css/css_for_reg.css'),
                                           gifts=gift_lst, size=size, login=login)
            if id_f:
                a = ''
                tmp = int(len(data) ** 0.5)
                for i in range(0, len(data), tmp):
                    a += data[i:i + tmp] + '\n'
                par = redact_fields(id_f, a.strip(), text)
                if not par:
                    flash('Карта с таким названием уже сущетсвует!')
                    flash('Дайте карте уникальное имя.')
                    map_lst = get_field(id_f)
                    karta = map_lst[1].split('\n')

                    not_to_red = False
                    if '#' in map_lst[1]:
                        not_to_red = True
                    return render_template('redact_field.html', data=karta, red=not_to_red, f_name=map_lst[3],
                                           id_f=map_lst[0], login=login, size=len(karta), gifts=gift_lst)
            else:
                post_game(data, text)
            return redirect(url_for('admin_main', login=login))

        flash('Нельзя создать карту без кораблей!')
        if id_f:
            map_lst = get_field(id_f)
            karta = map_lst[1].split('\n')

            not_to_red = False
            if '#' in map_lst[1]:
                not_to_red = True
            return render_template('redact_field.html', data=karta, red=not_to_red, f_name=map_lst[3],
                                   id_f=map_lst[0], login=login, size=len(karta), gifts=gift_lst)
        return render_template('index.html', style=url_for('static', filename='css/css_for_reg.css'), gifts=gift_lst, size=size, login=login)
    if name and field:
        name = request.args.get('name')
        field = request.args.get('field')
        number = request.args.get('tentacles')
        add_user_to_field(name, field, number)
        return redirect(url_for('admin_main', login=login))
    if name1 and field:
        name1 = request.args.get('name1')
        field = request.args.get('field')
        number = request.args.get('tentacles')
        if number:
            add_user_to_field_2(name1, field, number)
            return redirect(url_for('admin_main', login=login))
        else:
            users_list = get_users()
            map_lst = get_fields()
            b = request.args.get('b')
            flash('Нужно ввести количество выстрелов, которое хотите добавить пользователю.')
            return render_template('add_users.html', data=users_list, maps=map_lst, name=b, login=login)
    if map_id_1:
        map_id_1 = request.args.get('map1')
        delete_map(map_id_1)
        return redirect(url_for('admin_main', login=login))
    if field_id and login:
        field_id = request.args.get('field_id')
        login_user = request.args.get('login_user')
        login = request.args.get('login')
        delete_user_from_field(login_user, field_id)
        return redirect(url_for('admin_main', login=login))
    else:
        map_lst = get_fields()
        users_list = get_users()
        abc1 = []
        abc2 = []
        popitki = []
        for i in map_lst:
            for log, attempts in eval(i[2]).items():
                abc1.append(log)
                abc1.append(attempts)
                x = tuple(abc1)
                for j in users_list:
                    if x[0] in j and j[5] != 1:
                        abc2.append(x)
                        abc2.insert(0, i[0])
                        abc2.insert(1, j[4])
                abc1 = []
                popitki.append(abc2)
                abc2 = []
        for i in users_list:
            if i[1] != login:
                users_list.remove(i)

        return render_template('admin_main.html', style=url_for('static', filename='css/css_for_reg.css'), login=login,
                               data=map_lst, popitki=popitki, users=users_list)


@app.route('/admin/add_users', methods=['GET', 'POST'])
def add_users():
    login = request.args.get('login')
    a = request.args.get('map')
    print(a)
    users_list = get_users()
    map_lst = get_fields()
    if not login:
        return redirect('/')
    else:
        return render_template('add_users.html', data=users_list, maps=map_lst, name=a, login=login)


@app.route('/admin/redact_field', methods=['GET', 'POST'])
def redactor():
    login = request.args.get('login')
    a = request.args.get('map')
    map_lst = get_field(a)
    karta = map_lst[1].split('\n')
    gift_lst = get_prizes()

    not_to_red = False
    if '#' in map_lst[1]:
        not_to_red = True

    if not login:
        return redirect('/')
    else:
        return render_template('redact_field.html', gifts=gift_lst, data=karta, red=not_to_red, f_name=map_lst[3], id_f=map_lst[0], login=login, size=len(karta))


@app.route('/admin/del_prize', methods=['GET'])
def del_prize_al():
    login = request.args.get('login')
    if not login:
        return redirect('/')
    else:
        symb = request.args.get('deleterer')
        b = delete_prize(symb)
        a = get_prizes()
        return render_template('prizes_view_admin.html', login=login, data=a, filter='')


@app.route('/admin/create_field', methods=['GET'])
def index():
    login = request.args.get('login')
    form = SizeForm()
    if not login:
        return redirect('/')
    else:
        return render_template('home.html', form=form, login=login)


@app.route('/admin/prize_corner', methods=['GET', 'POST'])
def prize():
    login = request.args.get('login')
    if not login:
        return redirect('/')
    else:
        if request.method == 'GET':
            return render_template('prize_create.html', login=login)
        name = request.form['name']
        smb = request.form['symbol']
        file = request.files['icon']
        about = request.form['about']
        if smb in ('-', '#'):
            flash('Нельзя обозначать призы символами «#» и «-»')
            return render_template('prize_create.html', login=login)

        if file.filename.split('.')[-1] not in files:
            flash('Недопустимый формат файла')
            return render_template('prize_create.html', login=login)
        sql_ret = add_prize(name, smb, about)
        if not sql_ret:
            file.save(f'.\\static\\media\\{smb}.{file.filename.split(".")[-1]}')
            # "C:\Users\peter\AppData\Roaming"
            return redirect(url_for('admin_main', login=login))
        else:
            if sql_ret.strip() == 'prizes.symbol':
                txt = 'Символ'
            else:
                txt = 'Имя'
            flash(f'{txt} уже существует')
            return render_template('prize_create.html', login=login)


@app.route('/admin/redact', methods=['GET', 'POST'])
def changer():
    login = request.args.get('login')
    if not login:
        return redirect('/')
    else:
        if request.method == 'GET':
            symb = request.args.get('qup')
            if symb:
                inf_prize = get_prize_by_smb(symb)
                id_f = inf_prize[0]
                name = inf_prize[1]
                symb = inf_prize[2]
                desc = inf_prize[3]
            else:
                name = ''
                desc = ''
            return render_template('prize_create.html', login=login, name=name, symb=symb, desc=desc, id_f=id_f)
        name = request.form['name']
        smb = request.form['symbol']
        file = request.files['icon']
        about = request.form['about']
        id_f = int(request.form['rrp'])

        if smb in ('-', '#'):
            flash('Нельзя обозначать призы символами «#» и «-»')
            return render_template('prize_create.html', login=login, name=name, symb=smb, desc=about, id_f=id_f)

        if file.filename.split('.')[-1] not in files:
            flash('Недопустимый формат файла')
            return render_template('prize_create.html', login=login, name=name, symb=smb, desc=about, id_f=id_f)
        sql_ret = redact_prize(id_f, name, smb, about)
        if not sql_ret:
            file.save(f'.\\static\\media\\{smb}.{file.filename.split(".")[-1]}')
            # "C:\Users\peter\AppData\Roaming"
            return redirect(url_for('admin_main', login=login))
        else:
            if sql_ret.strip() == 'prizes.symbol':
                txt = 'Символ'
            else:
                txt = 'Имя'
            flash(f'{txt} уже существует')
            return render_template('prize_create.html', login=login, name=name, symb=smb, desc=about, id_f=id_f)


@app.route('/admin/prizes_view', methods=['GET', 'POST'])
def prizes_view_admin():
    login = request.args.get('login')
    a = get_prizes()
    if not login:
        return redirect('/')
    else:
        if request.method == 'GET':
            return render_template('prizes_view_admin.html', login=login, data=a, filter='')
        else:
            fil = request.form['filter']
            return render_template('prizes_view_admin.html', login=login, data=a, filter=fil)


@app.route('/admin/create_field', methods=['POST'])
def get_index():
    form = SizeForm()
    login = request.args.get('login')

    if form.validate_on_submit():
        size = form.size.data
        if not (2 <= size <= 15):
            flash('Размер поля должен быть от 2 до 15 клеток!')
            return render_template('home.html', form=form, login=login)
        return redirect(url_for('game', size=size, login=login))


# @app.route('/game/<int:size>', methods=['GET'])
# def game(size):
#     login = request.args.get('login')
#     if not login:
#         return redirect('/')
#     return render_template('index.html',  style=url_for('static', filename='css/css_for_reg.css'), size=size)


@app.route('/game/<int:size>', methods=['POST', 'GET'])
def game(size):
    login = request.args.get('login')
    if not login:
        return redirect('/')
    gift_lst = get_prizes()
    return render_template('index.html', style=url_for('static', filename='css/css_for_reg.css'), gifts=gift_lst, size=size, login=login)


@app.route('/user/maps', methods=['GET'])
def usr_maps():
    login = request.args.get('login')
    if not login:
        return redirect('/')
    maps_lst = get_user_fields(login)  # Потом будет получать из БД.
    users_list = get_users()
    prizes = get_user_prizes(login)
    a = prizes[0][0].split(', ')
    q = []
    for i in a:
        if i != '':
            q.append(i)
    for i in users_list:
        if i[1] != login:
            users_list.remove(i)
    # Формат: Номер карты(value), Название карты, Колличесво выстрелов
    return render_template('user_maps.html', data=maps_lst, style=url_for('static', filename='css/css_for_reg.css'), login=login, users=users_list, prizes=q)


@app.route('/user/maps', methods=['POST'])
def get_usr_maps():
    map_id = request.form['map']
    login = request.form['login']
    map_lst = get_fields()
    return redirect(url_for('usr_playground', login=login, map_id=map_id))


@app.route('/user/playground', methods=['GET'])
def usr_playground():
    logn = request.args.get('login')
    map_id = request.args.get('map_id')
    try:
        data = request.args.get('data')
    except Exception as e:
        data = ''
    if not logn:
        return redirect('/')
    if not data:
        local_map = get_field(map_id)
        converted = local_map[1].split('\n')
        # Формат: Номер карты, Расстановка на поле, словарь с кол-вом выстрелов по логину, имя карты, словарь призов
        return render_template('user_playground.html', size=len(converted), shots=json.loads(local_map[2])[logn], map_id=map_id, login=logn, field=converted, style=url_for('static', filename='css/css_for_reg.css'))
    else:
        if data.count('#') > json.loads(get_field(map_id)[2])[logn]:
            flash(f'У вас недостаточно снарядов для выстрела по выбранному количеству клеток')
            flash('(Нехватка боеприпасов 70%!!!)')
            local_map = get_field(map_id)
            converted = local_map[1].split('\n')
            return render_template('user_playground.html', size=len(converted), shots=json.loads(local_map[2])[logn],
                                   map_id=map_id, login=logn, field=converted,
                                   style=url_for('static', filename='css/css_for_reg.css'))
        else:
            local_map = get_field(map_id)
            shots_left = json.loads(local_map[2])[logn] - data.count('#')
            new_dict = json.loads(local_map[2])
            new_dict[logn] = shots_left
            a = ''
            counter = 0
            for i in range(0, len(data)):
                a += data[i]
                if (len(a) - counter) % int(len(data) ** 0.5) == 0:
                    a += '\n'
                    counter += 1
            aa = ""
            for i in a.split("\n")[:-1]:
                aa += i + "\n"
            new_map = aa.split('\n')[:-1]

            local_map = get_field(map_id)
            converted = local_map[1].split('\n')
            f = 0
            counter = data.count('#')
            flash(f'Выстрелов вы совершили: {counter}')
            flash('Среди которых:')
            won_prizes = []
            for y in range(len(converted)):
                for x in range(len(converted)):
                    if converted[y][x] == '-' and new_map[y][x] == '#':
                        row = list(converted[y])
                        row[x] = '#'
                        converted[y] = ''.join(row)
                    elif converted[y][x] == '#':
                        pass
                    elif converted[y][x] not in ('#', '-') and new_map[y][x] == '#':
                        prize = get_prize(converted[y][x])
                        flash(f'Вы выиграли {prize[1]}')
                        won_prizes.append(prize[2])
                        f = 1
                        row = list(converted[y])
                        row[x] = '#'
                        converted[y] = ''.join(row)
            if f == 0:
                flash('Вы ни разу не попали')
            else:
                add_prizes_to_user(logn, won_prizes)
            to_bd = '\n'.join(converted)
            save_map_ch(map_id, to_bd, new_dict)
            return redirect(url_for('usr_maps', login=logn))


@app.route('/user/prizes_view', methods=['GET', 'POST'])
def prizes_view_user():
    login = request.args.get('login')
    prizes = request.args.get('prizes')
    a = get_prizes()
    if not login:
        return redirect('/')
    else:
        return render_template('prizes_view_user.html', login=login, prizes=prizes, data=a)


if __name__ == '__main__':
    app.run(port=1024, host='127.0.0.1')
