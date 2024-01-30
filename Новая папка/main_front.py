from flask import Flask, url_for, request, render_template, redirect, flash
from sqll import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'predpof_code_crusaders'
init_database()


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
        else:
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
        else:
            return redirect(url_for('usr_maps', login=request.form['login']))
    else:
        flash(f'Логин или пароль указаны неправильно')
        return render_template('log_in.html')


@app.route('/admin/main', methods=['GET'])
def admin_main():
    login = request.args.get('login')
    if not login:
        return redirect('/')
    return render_template('admin_main.html', style=url_for('static', filename='css/css_for_reg.css'))


@app.route('/admin/create_field', methods=['GET', 'POST'])
def admin_create_field():
    login = request.args.get('login')
    if not login:
        return redirect('/')
    form = None
    if request.method == 'POST':
        # add_field()
        pass
    else:
        return render_template('admin_create_field.html',
                               style=url_for('static', filename='css/css_for_reg.css'), form=form)


@app.route('/user/maps', methods=['GET'])
def usr_maps():
    login = request.args.get('login')
    if not login:
        return redirect('/')
    maps_lst = [(1, '1 карта', 6), (2, "2 карта", 3)]  # Потом будет получать из БД.
    # Формат: Номер карты(value), Название карты, Колличесво выстрелов
    return render_template('user_maps.html', data=maps_lst, style=url_for('static', filename='css/css_for_reg.css'))


@app.route('/user/maps', methods=['POST'])
def get_usr_maps():
    login = request.args.get('login')
    if not login:
        return redirect('/')
    map_id = request.form['map']
    return redirect('/user/playground')


@app.route('/user/playground', methods=['GET'])
def usr_playground():
    login = request.args.get('login')
    if not login:
        return redirect('/')
    global map_id
    local_map = [map_id, f'{map_id} карта', 6]  # Потом будет получать из БД.
    # Формат: Номер карты(айдишник в БД, равный map_id), Название карты, Колличесво выстрелов
    return render_template('user_playground.html', Field=local_map[1], style=url_for('static', filename='css/css_for_reg.css'))


if __name__ == '__main__':
    app.run(port=1024, host='127.0.0.1')
