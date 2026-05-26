from main.main import Game
import flask
import json
from main.communication.action_message import ActionMessage

app = flask.Flask(__name__)

@app.route("/api/neuroshima", methods=["POST"])
@app.route('/api/neuroshima/', methods=['POST'])
def new_game():
    data = flask.request.get_json()
    data = flask.request.get_json(silent=True)
    # if data is None:
    #     return flask.jsonify({
    #         "error": "Invalid JSON body"
    #     }), 400W
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
    data = flask.request.get_json()
    try:
        data = ActionMessage(**data)
        game = Game(data.gameState)
        game.handle_action(data.userAction)
        return json.dumps(game.export())
    except Exception as e:
        return flask.jsonify({
            "error": str(e)
        }), 400

@app.route('/api/neuroshima/view', methods=['POST'])
def view():
    data = flask.request.get_json()
    try:
        return json.dumps(Game(data).build_user_view())
    except Exception as e:
        return flask.jsonify({
                "error": str(e)
            }), 400

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()