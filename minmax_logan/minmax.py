import numpy as np
from scipy.signal import convolve2d
from copy import copy

def minimax(state):

    # Get all available moves
    actions = get_actions(state)

    # Indices of best move
    best_action = np.zeros(2)

    # Indices of best counter move
    best_counter = np.zeros(2)

    # Max utility variable to determine the most rewarding move
    max_utility = float('-inf')

    # Explore each action
    for action in actions:

        # Update state for each action
        state_post_action = update_state(state, action, 1)

        # Get all possible counter moves from the new state
        successors = get_actions(state_post_action)

        # Min utility variable to determine the best counter move
        min_utility = float('inf')

        # Evaluate utility for each successor
        # Find the move with the lowest heuristic (best countermove)
        for successor in successors:

            # Update state for each successor action
            state_post_successor = update_state(state_post_action, successor, 2)

            # Calculate the heuristic of the state after the successor action
            utility = heuristic(state_post_successor)

            # If the utility is better than the current minimum, update it to the new move/utility
            if (utility < min_utility) or (utility == min_utility and successor[1] < best_counter[1]) or (utility == min_utility and successor[1] == best_counter[1] and successor[0] < best_counter[0]):
                best_counter = successor
                min_utility = utility

        # Once an optimal counter has been found, determine if it is preferable to the current best action's utility
        if (min_utility > max_utility) or (min_utility == max_utility and action[1] < best_action[1]) or (min_utility == max_utility and action[1] == best_action[1] and action[0] < best_action[0]):
            best_action = action
            max_utility = min_utility

    # Apply the best move to the current state
    state = update_state(state, best_action, 1)

    if (terminal(state)):
        return
    
    # Apply the best counter move, as well
    state = update_state(state, best_counter, 2)

    if (terminal(state)):
        return
    
    # Search for the next move from the updated state
    print(best_action)
    print(best_counter)
    print(state)
    minimax(state)

def terminal(state):
    if (heuristic(state) == 1000 or heuristic(state) == -1000):
        return True
    else:
        return False

import numpy as np

# not done
def heuristic(state):
    utility = 0
    for i in state:
        for j in i:
            # Horizontal check
            if (j < 2):
                if (state[i][j:j+5] == np.array([0,1,1,1,0])):
                    utility += 200
            if (j < 3):
                if (state[i][j:j+4] == np.array([0,1,1,1]) or state[i][j:j+4] == np.array([1,1,1,0])):
                    utility += 150


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
    # Create blank 5x6 board for state
    # 0: empty
    # 1: P1
    # 2: P2
    state = np.zeros((5,6))

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

    print(state)
    print(state[1][0:0+5])


    #minimax(state)

main()
