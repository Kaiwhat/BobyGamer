from flask import Flask, render_template,request,url_for,redirect#,jsonify
#from flask_socketio import SocketIO, emit #web
from DB import show_table, insert_table
app = Flask(__name__, static_folder='static',static_url_path='/')

max_score=0
#socketio = SocketIO(app) #web

@app.route('/')
def flappy():
    return render_template('game.html',max_score_back=max_score) 


@app.route('/reload_max_score', methods=['POST'])
def reload():
    re_max = request.json['re_max']
    global max_score
    max_score=re_max
    return redirect(url_for('flappy'))
    #socketio.emit('score_update', {'max_score': max_score})
    #return {'message': 'Score updated'}
    #print(max_score)
    #return redirect(url_for('flappy')) 
    #return jsonify({'max_score_back': max_score})
    #return render_template('game.html',max_score_back=max_score)  

@app.route('/get_max_score', methods=['GET'])
def get_max_score():
    return {'max_score': max_score}

@app.route('/show_table')
def show():
    data=show_table()
    return render_template('game.html',max_score_back=max_score, table=data) 

@app.route('/insert_table', methods=['POST'])
def insert():
    form =request.form
    name = form['player_name']
    #name = request.form.get('player_name')
    #name = request.json['name']
    insert_table(name, max_score)
    data=show_table()
    return render_template('game.html',max_score_back=max_score, table=data) 
    #return redirect(url_for('flappy')) 
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)