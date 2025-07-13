import sys
import numpy as np

"""
========== GRID ==========
"""
class Grid:
    def __init__(self, width=10, height=100):
        self.width = width
        self.height = height
        self.ocupied = np.zeros((height, width), dtype=bool)

    def is_occupied(self, row, col):
        return self.is_occupied[row, col]
    
    def clear_filled_rows(self):
        filled_rows = np.all(self.ocupied, axis=1)
        rows_to_keep = self.ocupied[~filled_rows]
        num_cleared = np.count_nonzero(filled_rows)
        new_grid = np.zeros_like(self.ocupied)
        new_grid[:len(rows_to_keep)] = rows_to_keep

        self.ocupied = new_grid
        return num_cleared


    
    def max_height(self):
        for row in range(self.height - 1, -1, -1):
            if np.any(self.ocupied[row]):
                return row + 1
        return 0

"""
========== BLOCKS ==========
"""
BLOCKS = {
    'Q': [(0,0), (0,1), (1,0), (1,1)],        
    'I': [(0,0), (0,1), (0,2), (0,3)],       
    'T': [(0,0), (0,1), (0,2), (1,1)],    
    'S': [(0,1), (0,2), (1,0), (1,1)],       
    'Z': [(0,0), (0,1), (1,1), (1,2)],        
    'L': [(0,0), (1,0), (2,0), (2,1)],        
    'J': [(0,1), (1,1), (2,1), (2,0)]        
}

"""
Returns True if the piece can be placed at the given position, False otherwise.
"""
def check_placement(grid, shape, row, col):
    
    for r, c in BLOCKS[shape]:
        r = row + r
        c = col + c
        if r < 0 or r >= grid.height or c < 0 or c >= grid.width or grid.ocupied[r, c]:
            return False
    return True

"""
Find the lowest row where the piece can be placed. Returns the row index or -1 if it cannot be placed.
"""
def find_row(grid, shape, col):
    max_r = max(r for r, _ in BLOCKS[shape])
    row = grid.height - 1 - max_r
    if not check_placement(grid, shape, row, col):
        return -1
    while row > 0 and check_placement(grid, shape, row - 1, col):
        row -= 1

    return row


def place_block(grid, shape, col):
    row = find_row(grid, shape, col)
    for r, c in BLOCKS[shape]:
        grid.ocupied[row + r, col + c] = True
    return True



def parse_piece(str): 
    "Convert something like 'Q0' to ('Q', 0)"
    return (str[0], int(str[1:]))

"""
Given a list of (piece_type, column), simulate dropping them into the grid,
apply row clears, and return final height.

@param pieces: List of tuples (piece_type, column)
@return: Final height of the grid after all pieces are placed
"""
def tetris(pieces):
    grid = Grid()
    for shape, col in pieces:
        place_block(grid, shape, col)
        while grid.clear_filled_rows() > 0:
            continue
    return grid.max_height()


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        piece_strs = line.split(",")
        pieces = [parse_piece(p) for p in piece_strs]
        final_height = tetris(pieces)
        print(final_height)

if __name__ == "__main__":
    main()