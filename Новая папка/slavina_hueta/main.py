from flask import Flask, url_for, request, render_template, send_from_directory, send_file, redirect
from sqll import *



app = Flask(__name__)
app.config['SECRET_KEY'] = 'predpof_code_crusaders'
init_database('predprof_db')


@app.route('/', methods=['GET'])
def first():
    return render_template('first_page.html')


@app.route('/', methods=['POST'])
def upload_file():
    print(1)
    torrent_id = request.form["kek"]
    print(torrent_id)



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')