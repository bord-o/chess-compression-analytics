import chess
import chess.engine

# uses uci interface with stockfish through python chess library. has problem matching legal move sometimes, work
# is continued with python stockfish module

# open stockfish with single threading
sf = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
sf.configure({"threads":1})

# initialize board with starting position
board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")




def eval_move_freq(uci_game):
    dyn_board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # uci_game is an array of uci encoded chess moves constituting a legal game
    encoded_game = ""
    encoded_arr = []
    # print(len(uci_game))
    for move in uci_game:
        move_indexes = sort_legals(dyn_board)

        for i in range(len(move_indexes)):
            # print(move_indexes[i], move)
            if move_indexes[i] == move:
                encoded_game += str(i) +","
                encoded_arr.append(i)
                print(encoded_game)
                #print(len(encoded_arr))
                break
        dyn_board.push_uci(move)

    return encoded_game






def sort_legals(board):

    legal_moves = board.legal_moves
    legals = []
    for m in legal_moves:
        legals.append(m)

    scores_test = []
    for x in range(len(legals)):

        board.push(legals[x])
        info = sf.analyse(board, chess.engine.Limit(nodes=1, depth=1))

        scores_test.append(info)
        board.pop()

    res_moves = {}

    for s in range(len(scores_test)):
        res_moves[legals[s].uci()] = scores_test[s]["score"].relative.score()

    res_moves_s = dict(sorted(res_moves.items(), key=lambda item: item[1], reverse=0))
    # this print gives the sorted legal moves in dict with each moves evaluation
    # print(res_moves_s)

    return list(res_moves_s.keys())


with open("./test.uci", "r") as uci_file:
    uci_moves = uci_file.read()
    uci_moves = uci_moves.split()
    # print(uci_moves[125])
    indexed_game = eval_move_freq(uci_moves)
    print(indexed_game)

sf.quit()
