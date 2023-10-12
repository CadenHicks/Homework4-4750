import numpy as np

ROWS = 5
COLS = 6
EMPTY = 0
X = 1
O = 2

# setup the starting board state
def initialize_board():
    board = np.full((ROWS, COLS), EMPTY)
    board[2][3] = X # FIRST MOVE
    board[2][2] = O # FIRST MOVE
    
    # example configuration for HW4 doc
    # (X h-value should be 84, O h-value should be 160)
    '''board[1][3] = X
    board[1][2] = O
    board[2][2] = O
    board[2][3] = O
    board[2][4] = X
    board[3][1] = O
    board[3][2] = X
    board[3][3] = X
    board[3][4] = O
    board[4][2] = X'''
    
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
                        if 0 <= i - di < ROWS and 0 <= j - dj < COLS and board[i - di][j - dj] == 0:
                            sides_open += 1
                        if 0 <= i + 3*di < ROWS and 0 <= j + 3*dj < COLS and board[i + 3*di][j + 3*dj] == 0:
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
                        if 0 <= i - di < ROWS and 0 <= j - dj < COLS and board[i - di][j - dj] == 0:
                            sides_open += 1
                        if 0 <= i + 2*di < ROWS and 0 <= j + 2*dj < COLS and board[i + 2*di][j + 2*dj] == 0:
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
    if player == 1:
        opponent = 2
    else:
        opponent = 1
        
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

'''
# driver - just testing the heuristic
def main():
    print("Board:")
    board = initialize_board() 
    display_board(board)
    print_heuristic(board, X, O)

if __name__ == "__main__":
    main()
'''