from plansza import board_to_json, Zeton, board
import flask
import json

# ten program uodstepnia 2 funkcje - GET /api/neuroshima/get_board - zwraca aktualny stan planszy w formacie JSON
# POST /api/neuroshima/postaw - przyjmuje dane o żetonie i go stawia

app = flask.Flask(__name__)

@app.route('/api/neuroshima/get_board', methods=['GET'])
def get_board():
    return json.dumps(board_to_json());

@app.route('/api/neuroshima/postaw', methods=['POST'])
def postaw_zeton():
    data = flask.request.get_json()
    board[data['x']][data['y']] = Zeton(data['x'], data['y'], data['frakcja'], data['nazwa'], data['rotacja'])
    # return json.dumps(board_to_json());
    return json.dumps({'status': 'success'})

@app.route('/api/neuroshima/bitwa', methods=['POST'])
def bitwa():
    for inicjatywa in range(9, -1, -1):
        for i in range(5):
            for j in range(9):
                # print(inicjatywa, i, j)
                if board[i][j] is not None:
                    board[i][j].aktywuj(inicjatywa)

        for i in range(5):
            for j in range(9):
                if board[i][j] is not None:
                    board[i][j].koniec_inicjatywy()

    return json.dumps({'status': 'success'})

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()