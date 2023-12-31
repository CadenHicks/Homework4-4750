import numpy as np
import time

ROWS = 5
COLS = 6
EMPTY = '.'
X = 'x'
O = 'o'

# setup the starting board state
def initialize_board():
    board = np.full((ROWS, COLS), EMPTY)
    board[2][3] = X # FIRST MOVE
    board[2][2] = O # FIRST MOVE
    
    # example configuration for HW4 doc
    # (X h-value should be 84, O h-value should be 160)
    # board[1][3] = X
    # board[1][2] = O
    # board[2][2] = O
    # board[2][3] = O
    # board[2][4] = X
    # board[3][1] = O
    # board[3][2] = X
    # board[3][3] = X
    # board[3][4] = O
    # board[4][2] = X
    
    return board

# Display the board
def display_board(board):
    print("  1 2 3 4 5 6")
    for i, row in enumerate(board, 1):
        print(i, ' '.join(row))
       
# worker function for the heuristic
# counts the number of occurrences of each 
# pattern for the player and returns a 
# dict of the counts
def count_rows(board, player):
    directions = [(0,1), (1,0), (1,1), (1,-1)] # horizontal, vertical, diagonals
    mask = [[set() for _ in range(COLS)] for _ in range(ROWS)] # tracks patterns
    counts = {
        '4-in-a-row': 0,
        'two-side-open-3-in-a-row': 0,
        'one-side-open-3-in-a-row': 0,
        'two-side-open-2-in-a-row': 0,
        'one-side-open-2-in-a-row': 0,
    }
    
    # helper function to mark a pattern as counted
    def mark_mask(i, j, di, dj, length):
        for k in range(length):
            mask[i + k*di][j + k*dj].add((di, dj)) # direction specific

    # checks if a pattern exists for a given direction
    def check_pattern(i, j, di, dj, l):
        for k in range(l):
            if not (0 <= i + k*di < ROWS and 0 <= j + k*dj < COLS) or board[i + k*di][j + k*dj] != player:
                return False
        return True
    
    # Check for 4-in-a-row (wincon)
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == player:
                for di, dj in directions:
                    if check_pattern(i, j, di, dj, 4):
                        counts['4-in-a-row'] += 1
                        return counts # player has won

    # Check for 3-in-a-row occurrences
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == player:
                for di, dj in directions:
                    # makes sure pattern hasn't been counted yet
                    if (di, dj) not in mask[i][j] and check_pattern(i, j, di, dj, 3):
                        sides_open = 0 # to distinguish
                        if 0 <= i - di < ROWS and 0 <= j - dj < COLS and board[i - di][j - dj] == ".":
                            sides_open += 1
                        if 0 <= i + 3*di < ROWS and 0 <= j + 3*dj < COLS and board[i + 3*di][j + 3*dj] == ".":
                            sides_open += 1
                        if sides_open == 2:
                            counts['two-side-open-3-in-a-row'] += 1
                            mark_mask(i, j, di, dj, 3)
                        elif sides_open == 1:
                            counts['one-side-open-3-in-a-row'] += 1
                            mark_mask(i, j, di, dj, 3)

    # Check for 2-in-a-row - utilize mark_mask to avoid double counting
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == player:
                for di, dj in directions:
                    if (di, dj) not in mask[i][j] and check_pattern(i, j, di, dj, 2):
                        sides_open = 0
                        if 0 <= i - di < ROWS and 0 <= j - dj < COLS and board[i - di][j - dj] == ".":
                            sides_open += 1
                        if 0 <= i + 2*di < ROWS and 0 <= j + 2*dj < COLS and board[i + 2*di][j + 2*dj] == ".":
                            sides_open += 1
                        if sides_open == 2:
                            counts['two-side-open-2-in-a-row'] += 1
                            mark_mask(i, j, di, dj, 2)
                        elif sides_open == 1:
                            counts['one-side-open-2-in-a-row'] += 1
                            mark_mask(i, j, di, dj, 2)

    return counts

# calls count_rows to determine heuristic value
def heuristic(board, player, opponent):

    if player == X:
        opponent = O
    else:
        opponent = X
        
    # retrieve heuristic results for current board state
    counts = count_rows(board, player)
    opp_counts = count_rows(board, opponent)
        
    # checking for terminal states
    if counts['4-in-a-row'] > 0:
        return 1000
    if opp_counts['4-in-a-row'] > 0 and player == O:
        return -1000

    # calculate heuristic value
    h= 200*counts['two-side-open-3-in-a-row'] - 80*opp_counts['two-side-open-3-in-a-row'] + \
        150*counts['one-side-open-3-in-a-row'] - 40*opp_counts['one-side-open-3-in-a-row'] + \
        20*counts['two-side-open-2-in-a-row'] - 15*opp_counts['two-side-open-2-in-a-row'] + \
        5*counts['one-side-open-2-in-a-row'] - 2*opp_counts['one-side-open-2-in-a-row']
    return h

# helper - print heuristic values for a given board in detail
def print_heuristic(board, player, opponent):
    counts = count_rows(board, player)
    print("\nPlayer: ", player)
    print("4-in-a-row: ", counts['4-in-a-row'])
    print("two-side-open-3-in-a-row: ", counts['two-side-open-3-in-a-row'])
    print("one-side-open-3-in-a-row: ", counts['one-side-open-3-in-a-row'])
    print("two-side-open-2-in-a-row: ", counts['two-side-open-2-in-a-row'])
    print("one-side-open-2-in-a-row: ", counts['one-side-open-2-in-a-row'])
    print("Heuristic value: ", heuristic(board, player, opponent))
    counts = count_rows(board, opponent)
    print("\nOpponent: ", opponent)
    print("4-in-a-row: ", counts['4-in-a-row'])
    print("two-side-open-3-in-a-row: ", counts['two-side-open-3-in-a-row'])
    print("one-side-open-3-in-a-row: ", counts['one-side-open-3-in-a-row'])
    print("two-side-open-2-in-a-row: ", counts['two-side-open-2-in-a-row'])
    print("one-side-open-2-in-a-row: ", counts['one-side-open-2-in-a-row'])
    print("Heuristic value: ", heuristic(board, opponent, player))

def movesLeft(board) :
    
    for i in range(5) :
        for j in range(6) :
            if(board[i][j] == EMPTY) :
                return True
            
    return False

def minimax(board,depth,isPlayer,player,opponet) :

    h = heuristic(board,player,opponet)

    if (depth == 0) :
        return h
    
    if(h == 1000) :
        return h
    
    if(h == -1000) :
        return h

    if(movesLeft(board) == False) :
        return h
        
    if(isPlayer) :
        best = -1000000

        for i in range(5) :
            for j in range(6) :

                if(board[i][j] == EMPTY) :

                    board[i][j] = player

                    best = max(best,minimax(board, depth - 1, False, player, opponet))

                    board[i][j] = EMPTY

        return best    
    else :
        best = 1000000

        for i in range(5) :
            for j in range(6) :

                if(board[i][j] == EMPTY) :

                    board[i][j] = opponet

                    best = min(best,minimax(board, depth - 1, True, player,opponet))
                    
                    #high = 0

                    # if(best[0] != value[0]) :
                    #     high = min(best[0],value[0])
                    # elif(best[0] == value[0] and best[1] == value[1] and best[2] == value[2]):
                    #     high = value[0]
                    # else :
                    #     if(j < value[2] or value[2] == -1) :
                    #         high = best[0]
                    #     elif(value[2] < j) :
                    #         high = value[0]
                    #     elif(j == value[2]) :
                    #         if(i < value[1] or value[1] == -1) :
                    #             high = best[0]
                    #         elif(value[2] < j) :
                    #             high = value[0]   

                    # if(high == value[0] and value[1] != -1) :
                    #     best[1] = value[1]
                    #     best[2] = value[2]
                    # else :
                    #     best[1] = i 
                    #     best[2] = j

                    board[i][j] = EMPTY
        
        return best

def getBestMove(board,depth,player,opponet):
    score = -1000000
    bestMove = None
    for row in range(5) :
        for col in range(6) :
            if(board[row][col] == EMPTY) :
                board[row][col] = player
                s = minimax(board,depth,False,player,opponet)
                # if(player == O) :
                #     print("Heuristic for P2 Move (",row+1,col+1,"):",s)
                board[row][col] = EMPTY
                if(s > score) :
                    score = s
                    bestMove = [row,col]
    return bestMove

# driver - just testing the heuristic
def main():
    print("Board:")
    board = initialize_board() 
    display_board(board)
    #print_heuristic(board, X, O)

    
    # for i in range(5) :
    #     for j in range(6) :
    #         if(board[i][j] == EMPTY) :
    #             board[i][j] = O
    #             h = heuristic(board,O, X)
    #             print("Heuristic for P2 Move (",i+1,j+1,"):",h)
    #             board[i][j] = EMPTY

    while(movesLeft != False) :
        
        isOver = 0
        bestMove = None

        bestMove = getBestMove(board,1,X,O)

        if(bestMove == None) :
            print("Tie Game")
            break

        board[bestMove[0],bestMove[1]] = X
        print("Player 1 Move: (",bestMove[0]+1,",",bestMove[1]+1,")")
        print("Board:")
        display_board(board)

        isOver = heuristic(board,X,O)
        
        if(isOver == 1000) :
            print("Player 1 wins")
            break

        bestMove = getBestMove(board,3,O,X)

        if(bestMove == None) :
            print("Tie Game")
            break

        board[bestMove[0],bestMove[1]] = O
        print("Player 2 Move: (",bestMove[0]+1,",",bestMove[1]+1,")")
        print("Board:")
        display_board(board)

        isOver = heuristic(board,O,X)
        
        if(isOver == 1000) :
            print("Player 2 wins")
            break

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Execution time: ",(end-start)/60)