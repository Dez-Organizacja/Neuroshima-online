from main.main import Game
import flask
import json

app = flask.Flask(__name__)

@app.route("/api/neuroshima", methods=["POST"])
@app.route('/api/neuroshima/', methods=['POST'])
def new_game():
    data = flask.request.get_json()
    with open ("odp.txt", "w") as f:
        print(data, file=f)
    data = flask.request.get_json(silent=True)
    if data is None:
        return flask.jsonify({
            "error": "Invalid JSON body"
        }), 400
    try:
        game = Game(data)
        game.start_game()
        return flask.jsonify(game.export()), 200
    except Exception as e:
        return flask.jsonify({
            "error": str(e)
        }), 400

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