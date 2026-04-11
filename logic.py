import random

def start_game():
    mat = [[0] * 4 for _ in range(4)]
    add_new_2(mat)
    add_new_2(mat)
    return mat

def add_new_2(mat):
    empty_cells = [(r, c) for r in range(4) for c in range(4) if mat[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        mat[r][c] = 2

def compress(mat):
    new_mat = [[0] * 4 for _ in range(4)]
    changed = False
    for i in range(4):
        pos = 0
        for j in range(4):
            if mat[i][j] != 0:
                new_mat[i][pos] = mat[i][j]
                if j != pos:
                    changed = True
                pos += 1
    return new_mat, changed

def merge(mat):
    changed = False
    score = 0
    for i in range(4):
        for j in range(3):
            if mat[i][j] != 0 and mat[i][j] == mat[i][j+1]:
                mat[i][j] *= 2
                score += mat[i][j]
                mat[i][j+1] = 0
                changed = True
    return mat, changed, score

def reverse(mat):
    return [row[::-1] for row in mat]

def transpose(mat):
    return [list(row) for row in zip(*mat)]

def move_left(grid):
    stage1, changed1 = compress(grid)
    stage2, changed2, score = merge(stage1)
    final_grid, changed3 = compress(stage2)
    return final_grid, (changed1 or changed2 or changed3), score

def move_right(grid):
    reversed_grid = reverse(grid)
    final_grid, changed, score = move_left(reversed_grid)
    return reverse(final_grid), changed, score

def move_up(grid):
    transposed_grid = transpose(grid)
    final_grid, changed, score = move_left(transposed_grid)
    return transpose(final_grid), changed, score

def move_down(grid):
    transposed_grid = transpose(grid)
    reversed_grid = reverse(transposed_grid)
    final_grid, changed, score = move_left(reversed_grid)
    res_reversed = reverse(final_grid)
    return transpose(res_reversed), changed, score