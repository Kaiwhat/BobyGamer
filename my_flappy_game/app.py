from flask import Flask, render_template

app = Flask(__name__, static_folder='static',static_url_path='/')

@app.route('/')
def flappy():
    return render_template('game.html') 

if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=5000)