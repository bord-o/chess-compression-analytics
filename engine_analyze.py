#!/usr/bin/python3

import chess
import chess.engine
import time 

leela = chess.engine.SimpleEngine.popen_uci(["/home/bordo/chessdb/lc0/build/release/lc0", "--threads=1", "--score-type=Q"])

fishy = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

fishy.configure({"threads":1})

board = chess.Board("8/5kp1/8/5R2/1p3B1P/5PK1/2r3P1/3r4 b - - 5 63")

legals = board.legal_moves
static_legals = []

for m in legals:
    static_legals.append(m)


scores_test = []
for x in range(len(static_legals)):
    board.push(static_legals[x])
    info = fishy.analyse(board, chess.engine.Limit(nodes=1, depth=1))

    scores_test.append(info)
    board.pop()

res_moves = {}

for s in range(len(scores_test)):
    # print(static_legals[s], scores_test[s]["score"].relative)
    res_moves[static_legals[s].uci()] = scores_test[s]["score"].relative.score()

# print(res_moves)
res_moves_s = dict(sorted(res_moves.items(), key=lambda item: item[1], reverse=0))
print(res_moves_s)

print(list(res_moves_s.keys()))


leela.quit()
fishy.quit()
