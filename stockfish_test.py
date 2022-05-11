#!/usr/home/bordo/chess-compression-analytics/bin/python3.8

import numpy as np
import chess.engine
from stockfish import Stockfish

engine = Stockfish("/usr/local/bin/stockfish", depth=1, parameters={"Threads": 1, "Minimum Thinking Time": 0, "Slow Mover": 0})

# initialize board with starting position
board = chess.Board()

def test_encode(uci_game_arr):
    board.reset()
    move_counter = 0
    game_length = len(uci_game_arr) - 1
    encoded_game = ""

    for i in range(len(uci_game_arr) - 1):
        # print(move_counter)
        sorted_evals = np.array(list(sort_legals(board, board.turn)))
        # print(sorted_evals)
        movel = uci_game_arr[i].lower()

        try:
            index = np.where(sorted_evals == movel)[0][0]
        except IndexError:
            print("move not found in legals: end of game? Encoded " + str(move_counter) + "/" +  str(game_length) +" moves.")
            print(sorted_evals, movel)
            break
        except FutureWarning:
            print("failed elementwise comp")
            break

        # print(index)
        encoded_game += str(index) + ","

        board.push_uci(movel)
        move_counter += 1

    print()
    return encoded_game


def sort_legals(board, side):

    legal_moves = board.legal_moves
    legals = []
    for m in legal_moves:
        legals.append(m)

    move_evals = {}
    for x in range(len(legals)):

        board.push(legals[x])
        fen_board = board.fen()
        engine.set_fen_position(fen_board)
        move_eval = engine.get_evaluation()

        # print(legals[x].uci(), move_eval)
        move_evals[legals[x].uci()] = move_eval["value"]
        # print(board.turn)
        board.pop()

    # print(move_evals)

    sorted_eval = dict(sorted(move_evals.items(), key=lambda x: x[1], reverse=side))
    return sorted_eval.keys()

encoded_games = []

test_db = "./modern35.uci"
write_file = "./modern35.csv"
try:
    with open(test_db, "r") as game:
        g = game.read()
        game_arr = g.split("\n\n")
        games = len(game_arr)
        game_counter = 1


        for game in game_arr:
            move_arr = game.split()
            print(move_arr)
            encoded_games.append(test_encode(move_arr))
            print(str(game_counter) + "/" + str(games) + " games encoded")
            game_counter += 1

except KeyboardInterrupt:
    print(encoded_games)
    stats = ''.join(encoded_games)
    with open(write_file, "w+") as statfile:
        statfile.write(stats)

else:
    print(encoded_games)
    stats = ''.join(encoded_games)
    with open(write_file, "w+") as statfile:
        statfile.write(stats)
'''
with open("./promote.txt", "r") as prom:
    g = prom.read()
    moves = g.split()
    print(moves)
    en = test_encode(moves)
    print(en)
'''