from main import Game
import flask
import json

app = flask.Flask(__name__)

@app.route('/api/neuroshima/', methods=['POST'])
def new_game():
    pass

@app.route('/api/neuroshima/action', methods=['POST'])
def action():
    pass
    # data = flask.request.get_json()
    # # print(data)
    # game = Game(data)
    # return json.dumps(game.export_game_state())

@app.route('/api/neuroshima/view', methods=['POST'])
def view():
    pass
    # data = flask.request.get_json()
    # game = Game(data)
    # return json.dumps(game.export_game_state())

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()