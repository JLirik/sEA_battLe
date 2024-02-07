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
        print(1)
        print(data)
        with open('map.txt', 'w') as f:
            a = ''
            tmp = int(len(data) ** 0.5)
            for i in range(0, len(data), tmp):
                a += data[i:i + tmp] + '\n'
            f.write(a.strip())
        print(1)
        print(a)
        return True

    print(555)
    data = request.args.get('data')
    login = request.args.get('login')
    if not login:
        return redirect('/')
    if data:
        data = request.args.get('data')
        print(data)
        post_game(data)
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
        return render_template('admin_main.html', style=url_for('static', filename='css/css_for_reg.css'), login=login, data=map_lst, popitki=popitki, users=users_list)


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
    users_list = get_users()
    for i in users_list:
        if i[1] != login:
            users_list.remove(i)
    # Формат: Номер карты(value), Название карты, Колличесво выстрелов
    return render_template('user_maps.html', data=maps_lst, style=url_for('static', filename='css/css_for_reg.css'), login=login, users=users_list)


@app.route('/user/maps', methods=['POST'])
def get_usr_maps():
    map_id = request.form['map']
    login = request.form['login']
    return redirect(url_for('usr_playground', login=login, map_id=map_id))


@app.route('/user/playground', methods=['GET'])
def usr_playground():
    login = request.args.get('login')
    map_id = request.args.get('map_id')
    if not login:
        return redirect('/')
    local_map = get_field(map_id)
    # Формат: Номер карты, Расстановка на поле, словарь с кол-вом выстрелов по логину, имя карты, словарь призов
    return render_template('user_playground.html', Field=local_map[1], style=url_for('static', filename='css/css_for_reg.css'))


if __name__ == '__main__':
    app.run(port=1024, host='127.0.0.1')
