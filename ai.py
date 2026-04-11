import logic
import copy

# Enhanced Snake Matrix: Encourages the AI to keep high values in the top-left
WEIGHT_MATRIX = [
    [1000, 100, 10, 1],
    [100, 10, 1, 0.1],
    [10, 1, 0.1, 0.01],
    [1, 0.1, 0.01, 0.001]
]

def calculate_heuristic(grid):
    score = 0
    empty_cells = 0
    for i in range(4):
        for j in range(4):
            # Multiply tile value by its position weight
            score += grid[i][j] * WEIGHT_MATRIX[i][j]
            if grid[i][j] == 0:
                empty_cells += 1
    
    # Adding a bonus for empty cells to keep the board open
    return score + (empty_cells * 100)

def expectimax(grid, depth, is_player):
    # Base case: reach depth limit
    if depth == 0:
        return calculate_heuristic(grid)

    if is_player:
        best_val = -float('inf')
        move_funcs = [logic.move_up, logic.move_down, logic.move_left, logic.move_right]
        for func in move_funcs:
            new_grid, changed, _ = func(copy.deepcopy(grid))
            if changed:
                best_val = max(best_val, expectimax(new_grid, depth - 1, False))
        return best_val if best_val != -float('inf') else calculate_heuristic(grid)
    else:
        # Chance node: The game spawns a 2 (90%) or 4 (10%)
        empty_cells = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
        if not empty_cells:
            return calculate_heuristic(grid)
        
        expected_val = 0
        # To keep it fast, we only sample a few empty cells if there are too many
        sample_cells = empty_cells[:4] if len(empty_cells) > 4 else empty_cells
        
        for r, c in sample_cells:
            # Case for spawning a '2'
            grid_2 = copy.deepcopy(grid)
            grid_2[r][c] = 2
            expected_val += 0.9 * expectimax(grid_2, depth - 1, True)
            
            # Case for spawning a '4'
            grid_4 = copy.deepcopy(grid)
            grid_4[r][c] = 4
            expected_val += 0.1 * expectimax(grid_4, depth - 1, True)
            
        return expected_val / len(sample_cells)

def get_best_move(grid):
    best_score = -1
    best_move = None
    move_funcs = {
        'Up': logic.move_up, 
        'Down': logic.move_down, 
        'Left': logic.move_left, 
        'Right': logic.move_right
    }

    for move, func in move_funcs.items():
        # Use deepcopy to avoid modifying the actual game state during simulation
        temp_grid = copy.deepcopy(grid)
        new_grid, changed, _ = func(temp_grid)
        if changed:
            # Depth 3 provides a great mix of speed and strategy
            score = expectimax(new_grid, 3, False) 
            if score > best_score:
                best_score = score
                best_move = move
    return best_move