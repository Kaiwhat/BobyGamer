from flask import Flask, render_template, request, url_for, redirect
from DB import show_table, insert_table  # 假設你有相應的資料庫操作模組

app = Flask(__name__, static_folder='static', static_url_path='/')

max_score = 0

@app.route('/')
def flappy():
    return render_template('game.html', max_score_back=max_score)

@app.route('/reload_max_score', methods=['POST'])
def reload():
    re_max = request.json['re_max']
    global max_score
    max_score = re_max
    return redirect(url_for('flappy'))

@app.route('/get_max_score', methods=['GET'])
def get_max_score():
    return {'max_score': max_score}

@app.route('/show_table')
def show():
    data = show_table()
    return render_template('game.html', max_score_back=max_score, table=data)

@app.route('/insert_table', methods=['POST'])
def insert():
    form = request.form
    name = form['player_name']
    insert_table(name, max_score)
    data = show_table()
    return render_template('game.html', max_score_back=max_score, table=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
