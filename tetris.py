#!/usr/bin/env python3
import sys
import numpy as np
from typing import List, Tuple, Dict


WIDTH = 10
HEIGHT = 100
Piece  = Tuple[str, int]
Block  = Tuple[int, int]
Shape  = List[Block]

BLOCKS: Dict[str, Shape] = {
    'Q': [(0,0), (0,1), (1,0), (1,1)],        
    'I': [(0,0), (0,1), (0,2), (0,3)],       
    'T': [(0,1), (1,1), (1,0), (1,2)],    
    'S': [(0,0), (0,1), (1,1), (1,2)],       
    'Z': [(1,0), (1,1), (0,1), (0,2)],        
    'L': [(0,0), (1,0), (2,0), (0,1)],        
    'J': [(0,0), (0,1), (1,1), (2,1)]        
}

class Grid:
    def __init__(self, width: int = WIDTH, height: int = HEIGHT) -> None:
        self.width = width
        self.height = height
        self.values = np.zeros((height, width), dtype=bool)

    def clear_rows(self) -> int:
        filled_rows = np.all(self.values, axis=1)
        rows_keep = self.values[~filled_rows]
        new_grid = np.zeros_like(self.values)
        new_grid[:len(rows_keep)] = rows_keep #keeps non-filled rows at lowest indices
        self.values = new_grid


        return np.count_nonzero(filled_rows) #num of cleared rows
    
    def max_height(self) -> int:
        for r in range(self.height-1, -1, -1): #starts at top-most row
            if np.any(self.values[r]):
                return r+1
        return 0

def check_placement(grid, shape: str, row: int, col: int) -> bool:
    for r, c in BLOCKS[shape]:
        r = row + r
        c = col + c
        if grid.values[r, c]:
            return False
    return True
    
def find_row(grid, shape: str, col: int) -> int:
    max_r = max(r for r, _ in BLOCKS[shape]) #height of shape
    r = grid.height - 1 - max_r
    if not check_placement(grid, shape, r, col):
        return -1
    while r > 0 and check_placement(grid, shape, r-1, col):
        r -=1
    return r

def place_block(grid, shape: str, col: int) -> None:
    row = find_row(grid, shape, col)
    for r, c in BLOCKS[shape]:
        grid.values[row + r, col + c] = True

def parse_pieces(line: str) -> List[Piece]:
    pieces: List[Piece] = []
    for t in line.split(','):
        t = t.strip()
        if not t:
            continue
        shape, col = t[0], t[1:]
        pieces.append((shape, int(col)))
    return pieces

def tetris(pieces: List[Piece]) -> int:
    grid = Grid()
    for shape, col, in pieces:
        place_block(grid, shape, col)
        while grid.clear_rows() > 0:
            continue
    return grid.max_height()

def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        pieces = parse_pieces(line)
        final_height = tetris(pieces)
        print(final_height)

if __name__ == "__main__":
    main()