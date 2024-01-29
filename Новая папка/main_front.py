from flask import Flask, url_for, request, render_template, redirect, flash
from sqll import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'predpof_code_crusaders'
init_database()


@app.route('/', methods=['GET'])
def first():
    return render_template('first_page.html', style=url_for('static', filename='css/css_for_reg.css'))


@app.route('/', methods=['POST'])
def first_post():
    button_pressed = request.form["but"]
    if button_pressed == 'Регистрация':
        return redirect('/reg')
    else:
        pass


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
            return redirect('/admin/main')
        else:
            return redirect('/user/main')
    else:
        if sql_ret == 'users.mail':
            msg = 'ая почта'
        else:
            msg = 'ый логин'
        flash(f'Указанн{msg} уже существует')
        return render_template('registration_unit.html')


@app.route('/admin/main', methods=['GET'])
def admin_main():
    return render_template('admin_main.html', style=url_for('static', filename='css/css_for_reg.css'))


@app.route('/admin/create_field', methods=['GET', 'POST'])
def admin_create_field():
    form = None
    if request.method == 'POST':
        # add_field()
        pass
    else:
        return render_template('admin_create_field.html',
                               style=url_for('static', filename='css/css_for_reg.css'), form=form)


@app.route('/user/maps', methods=['GET'])
def usr_maps():
    maps_lst = [(1, '1 карта', 6), (2, "2 карта", 3)]  # Потом будет получать из БД.
    # Формат: Номер карты(value), Название карты, Колличесво выстрелов
    return render_template('user_maps.html', data=maps_lst, style=url_for('static', filename='css/css_for_reg.css'))


if __name__ == '__main__':
    app.run(port=1024, host='127.0.0.1')
