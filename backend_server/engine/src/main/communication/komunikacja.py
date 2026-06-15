from main.main import Game
import flask
import json
from main.communication.server_message import ServerMessage

app = flask.Flask(__name__)


@app.route("/api/neuroshima", methods=["POST"])
# @app.route('/api/neuroshima/', methods=['POST'])
def new_game():
    data = flask.request.get_json()
    # data = flask.request.get_json(silent=True)
    # if data is None:
    #     return flask.jsonify({
    #         "error": "Invalid JSON body"
    #     }), 400W
    try:
        game = Game()
        game.start_game(data)
        return flask.jsonify(game.export()), 200
    except Exception as e:
        return flask.jsonify({
            "error": str(e)
        }), 400

@app.route('/api/neuroshima/action', methods=['POST'])
def action():
    data = flask.request.get_json()
    try:
        data = ServerMessage(**data)
        game = Game()
        game.load(data.gameState)
        game.handle_action(data.userAction)
        return flask.jsonify({
            "messageType": "GAMESTATUSCHANGE_RESPONSE",
            "gameState": game.export()
        }), 200
    except Exception as e:
        return flask.jsonify({
            "error": str(e)
        }), 400

@app.route('/api/neuroshima/view', methods=['POST'])
def view():
    data = flask.request.get_json()
    try:
        # Java sends { "messageType": "GAMEVIEW_REQUEST", "gameState": {...} }.
        # Also accept raw game-state JSON for easier direct testing.
        # game_state = data.get("gameState", data) if isinstance(data, dict) else data
        # game = Game().load(game_state)
        data = ServerMessage(**data)
        game = Game()
        game.load(data.gameState)
        return flask.jsonify({
            "messageType": "GAMEVIEW_RESPONSE",
            "gameView": game.build_user_view()
        }), 200
    except Exception as e:
        return flask.jsonify({
                "error": str(e)
            }), 400

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()