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
    def post_game(data):
        a = ''
        tmp = int(len(data) ** 0.5)
        for i in range(0, len(data), tmp):
            a += data[i:i + tmp] + '\n'
        add_field(a.strip(), {}, 'Карта 105')
        return True

    def check(map_1):
        n = len(map_1)
        for y in range(n):
            for x in range(n):
                if map_1[y][x] != "-":
                    if x < n - 1:
                        if map_1[y][x + 1] != "-":
                            return True
                        if y < n - 1:
                            if map_1[y + 1][x] != "-":
                                return True
                            if map_1[y + 1][x + 1] != "-":
                                return True
                        if y > 0:
                            if map_1[y - 1][x] != "-":
                                return True
                            if map_1[y - 1][x + 1] != "-":
                                return True
                    elif y < n - 1 and map_1[y + 1][x] != "-":
                        return True
                    elif y > 0 and map_1[y - 1][x] != "-":
                        return True
        return False


    name = request.args.get('name')
    field = request.args.get('field')
    data = request.args.get('data')
    login = request.args.get('login')
    number = request.args.get('tentacles')
    if not login:
        return redirect('/')
    if data:
        data = request.args.get('data').replace(' ', '-')

        gift_lst = []
        b = ''
        tmp = int(len(data) ** 0.5)
        for i in range(0, len(data), tmp):
            b += data[i:i + tmp] + '\n'
        size = len(b.split('\n')[:-1])

        if check(b.split('\n')[:-1]):
            flash('Нельзя ставить два корабля рядом')
            return render_template('index.html', style=url_for('static', filename='css/css_for_reg.css'),
                                   gifts=gift_lst, size=size, login=login)

        if data.count('-') != len(data):
            post_game(data)
            return redirect(url_for('admin_main', login=login))

        flash('Нельзя создать карту без кораблей!')

        return render_template('index.html', style=url_for('static', filename='css/css_for_reg.css'), gifts=gift_lst, size=size, login=login)
    if name and field:
        name = request.args.get('name')
        field = request.args.get('field')
        number = request.args.get('tentacles')
        add_user_to_field(name, field, number)
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
        print(map_lst)
        return render_template('admin_main.html', style=url_for('static', filename='css/css_for_reg.css'), login=login, data=map_lst, popitki=popitki, users=users_list)


@app.route('/admin/add_users', methods=['GET', 'POST'])
def add_users():
    login =  request.args.get('login')
    a = request.args.get('map')
    print(a)
    users_list = get_users()
    print(users_list)
    map_lst = get_fields()
    print(map_lst)
    if not login:
        return redirect('/')
    else:
        return render_template('add_users.html', data=users_list, maps=map_lst, name=a, login=login)

@app.route('/admin/create_field', methods=['GET'])
def index():
    login = request.args.get('login')
    print(login, 1)
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
        print(1)
        if request.method == 'GET':
            return render_template('prize_create.html', login=login)
        name = request.form['name']
        smb = request.form['symbol']
        file = request.files['icon']
        about = request.form['about']
        print(5, file)
        if file.filename.split('.')[-1] not in files:
            flash('Недопустимый формат файла')
            return render_template('prize_create.html', login=login)
        sql_ret = add_prize(name, smb, about)
        print(sql_ret, 1)
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


@app.route('/admin/create_field', methods=['POST'])
def get_index():
    form = SizeForm()
    login = request.args.get('login')
    print(login, 2)

    if form.validate_on_submit():
        size = form.size.data
        if not (2 <= size <= 15):
            flash('Размер поля должен быть от 2 до 15 клеток!')
            return render_template('home.html', form=form, login=login)
        return redirect(url_for('game', size=size, login=login))


# @app.route('/game/<int:size>', methods=['GET'])
# def game(size):
#     login = request.args.get('login')
#     print(login, 2)
#     if not login:
#         return redirect('/')
#     return render_template('index.html',  style=url_for('static', filename='css/css_for_reg.css'), size=size)


@app.route('/game/<int:size>', methods=['POST', 'GET'])
def game(size):
    login = request.args.get('login')
    print(login, 123)
    if not login:
        return redirect('/')
    gift_lst = []
    return render_template('index.html', style=url_for('static', filename='css/css_for_reg.css'), gifts=gift_lst, size=size, login=login)


@app.route('/admin/prizes_view', methods=['GET', 'POST'])
def prizes_view_admin():
    login = request.args.get('login')
    a = get_prizes()
    print(a)
    if not login:
        return redirect('/')
    else:
        return render_template('prizes_view_admin.html', login=login, data=a)


@app.route('/user/maps', methods=['GET'])
def usr_maps():
    login = request.args.get('login')
    if not login:
        return redirect('/')
    maps_lst = get_user_fields(login)  # Потом будет получать из БД.
    users_list = get_users()
    prizes = get_user_prizes(login)
    print(prizes)
    a = prizes[0][0].split(', ')
    print(a)
    q = []
    for i in a:
        if i != '':
           q.append(i)
    print(q)
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
    print(map_lst)
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
        print(data)
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
            # print(new_map)

            local_map = get_field(map_id)
            converted = local_map[1].split('\n')
            # print(converted)
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
                        # print(prize)
                        flash(f'Вы выиграли {prize[1]}')
                        # print('Вы попали!')
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
    print(1)
    print(prizes)
    a = get_prizes()
    print(a)
    if not login:
        return redirect('/')
    else:
        return render_template('prizes_view_user.html', login=login, prizes=prizes, data=a)


if __name__ == '__main__':
    app.run(port=1024, host='127.0.0.1')
