
import time
import sys
import argparse
from io import StringIO

from utils.Go import *
from players import myPlayerUCTS, myPlayerBasic
def get_arguments():
    parser = argparse.ArgumentParser(description="AlphaENSCEIRB")
    parser.add_argument("--blackTile", type=str, default='UCTSearch',
                        help="AI used for the black tiles")
    parser.add_argument("--whiteTile", type=str, default='Basic',
                        help="AI used for the white tiles")
    return parser.parse_args()

args = get_arguments()

def args_to_object(arg):
    if arg == 'UCTSearch':
        return myPlayerUCTS
    # elif arg == 'AlphaBeta':
    #     return myPlayerAlphaBeta
    elif arg == 'Basic':
        return myPlayerBasic
    else:
        print("Invalid AI name")

def run_local_game(ai1, ai2, goban_size = 5):
    '''

    :param ai1: first AI type
    :param ai2: second AI type
    :param goban_size: Size of de board - Default is 9x9
    :return: Winner, number of white and black tiles
    '''
    b = Go(goban_size)

    players = []
    player1 = ai1.myPlayer(goban_size)
    print('Player 1 uses', player1._my_ai)
    # player1 = myPlayer.myPlayer()
    player1.newGame(b._BLACK)
    players.append(player1)
    player2 = ai2.myPlayer(goban_size)
    print('Player 2 uses', player2._my_ai)
    player2.newGame(b._WHITE)
    players.append(player2)

    totalTime = [0, 0] # total real time for each player
    nextplayer = 0
    nextplayercolor = b._BLACK

    outputs = ["", ""]
    sysstdout= sys.stdout
    stringio = StringIO()

    # print(b.get_legal_moves())
    while not b.is_game_over():
        print("Referee Board:")
        print(b)
        print("Before move", b._nb_move)
        # print("Legal Moves: ", b.get_legal_moves())
        b._nb_move += 1
        otherplayer = (nextplayer + 1) % 2
        othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE

        currentTime = time.time()
        #sys.stdout = stringio
        move = players[nextplayer].getPlayerMove()
        sys.stdout = sysstdout
        playeroutput = "\r" + stringio.getvalue()
        stringio.truncate(0)
        print(("[Player "+str(nextplayer) + "] ").join(playeroutput.splitlines(True)))
        outputs[nextplayer] += playeroutput
        totalTime[nextplayer] += time.time() - currentTime
        print("Player ", nextplayercolor, players[nextplayer].getPlayerName(), "plays" + str(move))
        (x,y) = move
        if not b.is_valid_move(nextplayercolor,[x,y]):
            print(otherplayer, nextplayer, nextplayercolor)
            print("Problem: illegal move")
            break
        b.push([nextplayercolor, x, y])
        players[otherplayer].playOpponentMove(x,y)

        nextplayer = otherplayer
        nextplayercolor = othercolor

        print(b)
        # print("*"*10)
        # (nbwhites, nbblacks) = b.get_nb_pieces()
        # print(nbblacks, nbwhites)
        # [nbwhites, nbblacks] = b.count_corner()
        # print(nbblacks, nbwhites)
        # print("*"*10)
    print("The game is over")
    print(b)

    (nbwhites, nbblacks) = b.get_nb_pieces()
    print(nbblacks, nbwhites)
    [nbwhites, nbblacks] = b.count_corner()
    print(nbblacks, nbwhites)
    print("Time:", totalTime)
    print("Winner: ", end="")
    if nbwhites > nbblacks:
        print("WHITE")
        winner = b._WHITE
    elif nbblacks > nbwhites:
        print("BLACK")
        winner = b._BLACK
    else:
        print("DEUCE")
        winner = 0
    player2.endGame(winner)

    return winner, nbwhites, nbblacks, totalTime

if __name__ == '__main__':
    run_local_game(args_to_object(args.blackTile), args_to_object(args.whiteTile))