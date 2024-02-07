import json

from flask import Flask, url_for, request, render_template, redirect, flash
from sqll import *
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'predpof_code_crusaders'
init_database()

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
        print(a)
        add_field(a.strip(), {}, 'gg')
        print(123)
        return True

    def add_user(name, field, number):
        add_user_to_field(name, field, number)

    print(555)
    name = request.args.get('name')
    field = request.args.get('field')
    data = request.args.get('data')
    login = request.args.get('login')
    number = request.args.get('tentacles')
    print(name, 234578)
    print(data, 456787656789)
    print(number, 'wqewqe')
    if not login:
        return redirect('/')
    if data:
        data = request.args.get('data')
        post_game(data)
        return redirect(url_for('admin_main', login=login))
    if name and field:
        name = request.args.get('name')
        field = request.args.get('field')
        number = request.args.get('tentacles')
        add_user(name, field, number)
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


@app.route('/admin/create_field', methods=['POST'])
def get_index():
    form = SizeForm()
    login = request.args.get('login')
    print(login, 2)
    if form.validate_on_submit():
        size = form.size.data
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
    return render_template('index.html', style=url_for('static', filename='css/css_for_reg.css'), size=size, login=login)



@app.route('/user/maps', methods=['GET'])
def usr_maps():
    login = request.args.get('login')
    if not login:
        return redirect('/')
    maps_lst = get_user_fields(login)  # Потом будет получать из БД.
    # Формат: Номер карты(value), Название карты, Колличесво выстрелов
    return render_template('user_maps.html', data=maps_lst, style=url_for('static', filename='css/css_for_reg.css'), login=login)


@app.route('/user/maps', methods=['POST'])
def get_usr_maps():
    map_id = request.form['map']
    login = request.form['login']
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
                aa += i[::-1] + "\n"
            new_map = aa.split('\n')[:-1]
            print(new_map)

            local_map = get_field(map_id)
            converted = local_map[1].split('\n')
            print(converted)

            for y in range(len(converted)):
                for x in range(len(converted)):
                    if converted[y][x] == 'k' and new_map[y][x] == '#':
                        print('Вы попали!')
                        row = list(converted[y])
                        row[x] = '#'
                        converted[y] = ''.join(row)
                    elif converted[y][x] == '-' and new_map[y][x] == '#':
                        row = list(converted[y])
                        row[x] = '#'
                        converted[y] = ''.join(row)
            to_bd = '\n'.join(converted)
            nothing = save_map_ch(map_id, to_bd, new_dict)
            return redirect(url_for('usr_maps', login=logn))


if __name__ == '__main__':
    app.run(port=1024, host='127.0.0.1')
