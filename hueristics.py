import numpy as np

def get_mse(arr):
    mean = np.mean(arr)
    sum_squared_error = 0
    for num in arr:
        sum_squared_error += (num - mean) ** 2
    return sum_squared_error / len(arr)

def get_squareness_and_holes(board_state):
    heights = [0] * len(board_state[0])
    holes = 0
    columns_found = set()
    for i in range(len(board_state)):
        for j in range(len(board_state[i])):
            if board_state[i][j] is not None and j not in columns_found:
                heights[j] = len(board_state) - i
                columns_found.add(j)
            elif board_state[i][j] is None and j in columns_found:
                holes += 1
    heights.remove(min(heights))

    return {"holes": holes, 'mse': get_mse(heights), 'heights': heights}
