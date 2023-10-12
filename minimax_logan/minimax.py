import numpy as np
from scipy.signal import convolve2d
from copy import copy
import time
from heuristic import *

nodes_generated = 0

def bestMove(state, player):

    global nodes_generated
    nodes_generated = 0
    # Max utility variable to store the utility of the best move
    max_utility = float('-inf')
    # Array to store the coordinates of the best move
    best_move = np.zeros(2)
    # Get all possible actions for Player1
    actions = get_actions(state)
    # Find the maximum utility of all the possible actions
    for action in actions:
        # Update the state
        state_post_action = update_state(state, action, player)
        # Run minimax for 1 more level starting with Player2's move
        if (player == 1):
            utility = minimax(state_post_action, 1, 2, True)
        else:
            utility = minimax(state_post_action, 3, 1, False)

        # Update the best move
        if (utility > max_utility):
            max_utility = utility
            best_move = action
        # Tie breaking
        elif (utility == max_utility):
            # First, tie break by row
            if (action[0] < best_move[0]):
                max_utility = utility
                best_move = action
            # If rows are equal, tie break by column
            elif (action[0] == best_move[0]):
                # Tie break by column
                if (action[1] < best_move[1]):
                    max_utility = utility
                    best_move = action
    
    return best_move

'''
Performs minimax algorithm (2-ply for P1, 4-ply for P2)
Returns updated state, move taken, and clock time

p1_max: Boolean stating if P1 is max
'''
def minimax(state, depth, player, p1_max):
    global nodes_generated
    # If at the leaf nodes, return their heuristic
    if (depth == 0):
        if (player == 1):
            return heuristic(state, player, 2)
        else:
            return heuristic(state, player, 1)
    
    # If Player1's move, maximize their move's utility
    if (player == 1):
        # Max utility variable to determine the most rewarding move
        if (p1_max == True):
            optimal_utility = float('-inf')
        else:
            optimal_utility = float('inf')

        # Get all possible actions for player 1
        actions = get_actions(state)

        for action in actions:
            # Update state for each action
            state_post_action = update_state(state, action, 1)
            # Find utility of child node, one level deeper
            utility = minimax(state_post_action, depth-1, 2, p1_max)
            # Find maximum utility of all child nodes
            if (p1_max == True):
                optimal_utility = max(optimal_utility, utility)
            else:
                optimal_utility = min(optimal_utility, utility)

        nodes_generated += len(actions)

        return optimal_utility
    # If Player2's move, minimize their move's utility
    else:
        # If P1 is maximizing, then P2 should be minimizing
        if (p1_max == True):
            optimal_utility = float('inf')
        else:
            optimal_utility = float('-inf')

        # Get all possible actions for player 2
        actions = get_actions(state)

        for action in actions:
            # Update state for each action
            state_post_action = update_state(state, action, 2)
            # Find utility of child node, one level deeper
            utility = minimax(state_post_action, depth-1, 1, p1_max)
            # Find maximum utility of all child nodes
            if (p1_max == True):
                optimal_utility = min(optimal_utility, utility)
            else:
                optimal_utility = max(optimal_utility, utility)

        nodes_generated += len(actions)

        return optimal_utility
    


def get_actions(state):
    '''
    Returns the indices of points that are available to play (== 0)

    Parameters:
    - state ((5,6) numpy array): empty (0), P1 (1), P2 (2)

    Returns:
    - (n, 2) numpy array: List of available indices
    '''
    filter = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])
    
    # Perform 2D convolution (count # of neighbors)
    neighbors_count = convolve2d(state, filter, mode='same')
    # Return points that are empty and contain at least one neighbor
    indices = np.where((state == 0) & (neighbors_count > 0))
    # Return a list of coordinates
    return np.array(indices).T

def update_state(state, action, player):
    '''
    Given a new action [x, y], return an updated state

    Parameters:
    - state ((5,6) numpy array)
    - action ([x, y]): Index of new move
    - player (int {1, 2}): Number of the player whose move it is

    Returns:
    - state with the value updated at [x, y]
    '''
    new_state = state.copy()
    new_state[*action] = player
    return new_state



def main():
    global nodes_generated
    # Create blank 5x6 board for state
    # 0: empty
    # 1: P1
    # 2: P2
    state = np.zeros((5,6))

    '''
    # o
    state[1][2] = 2
    state[2][2] = 2
    state[2][3] = 2
    state[3][1] = 2
    state[3][4] = 2

    # x
    state[1][3] = 1
    state[2][4] = 1
    state[3][2] = 1
    state[3][3] = 1
    state[4][2] = 1
    '''

    state[2][3] = 1
    state[2][2] = 2

    # Count 0's as empty squares
    empty_squares = len(np.array(np.where(state==0)).T)

    print("Initial state:")
    display_board(state)

    while (True):
        # Player 1 Move
        start_time = time.process_time()
        best_move = bestMove(state, 1)
        end_time = time.process_time()

        # Update state with player1's move
        state = update_state(state, best_move, 1)

        print(f"Player1 Move: [{best_move[0]+1}, {best_move[1]+1}]")
        print(f"Nodes generated: {nodes_generated}")
        print(f"CPU Time: {end_time - start_time} (s)")
        nodes_generated = 0
        display_board(state)
        #print(f"{state}\n")

        if (heuristic(state, 1, 2) == 1000):
            print("Player 1 Wins!")
            break

        if ((empty_squares - 1) == 0):
            print("It's a Draw!")
            break
        else:
            empty_squares -= 1

        # Player 2 Move
        start_time = time.process_time()
        best_move = bestMove(state, 2)
        end_time = time.process_time()

        # Update state with player2's move
        state = update_state(state, best_move, 2)

        print(f"Player2 Move: [{best_move[0]+1}, {best_move[1]+1}]")
        print(f"Nodes generated: {nodes_generated}")
        print(f"CPU Time: {end_time - start_time} (s)")
        nodes_generated = 0
        display_board(state)
        #print(f"{state}\n")

        if (heuristic(state, 2, 1) == 1000):
            print("Player 2 Wins!")
            break

        # If no one has one but the board is full, it's a draw
        if ((empty_squares - 1) == 0):
            print("It's a Draw!")
            break
        else:
            empty_squares -= 1

main()