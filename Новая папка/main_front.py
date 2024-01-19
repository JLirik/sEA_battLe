from flask import Flask, url_for, request, render_template, send_from_directory, send_file, redirect
from sqll import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'predpof_code_crusaders'
init_database()


@app.route('/', methods=['GET'])
def first():
    return render_template('first_page.html', style=url_for('static', filename='css/css_for_reg.css'))


@app.route('/reg', methods=['GET'])
def reg():
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


@app.route('/user/main', methods=['GET, POST'])
def user_main():
    return render_template('user_main.html', style=url_for('static', filename='css/css_for_reg.css'))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
