# 6x6 Sudoku

from Base import *
import pygame
from random import shuffle


class Sudoku(template):
    __slots__ = ('arr', 'key', 'clues', 'notes', 'note_mode', 'solved')
    
    def __init__(self) -> None:
        self.arr, self.key = generate()
        self.clues = [(r, c) for r in range(6) for c in range(6) if self.arr[r][c] != 0]
        self.notes = [[[False] * 6 for _ in range(6)] for _ in range(6)]
        self.note_mode = False
        self.solved = False

    def init(self, width: int, height: int) -> tuple[int, int]:
        tile   = min(width*6/7 / 6 * SPACER, height / 6 * SPACER)
        buffer = min(width*6/7 - 6 * tile,   height - 6 * tile) / 2
        return int(tile), int(buffer)

    def render(self, dis, tile, buffer, _, clicked) -> None:
        dis.fill((125, 125, 125))
        
        # Draw grid lines
        end = tile * 6
        
        cx = (clicked[0] - buffer) // tile
        cy = (clicked[1] - buffer) // tile
        if 0 <= cx < 6 and 0 <= cy < 6:
            pygame.draw.rect(dis, BLUE if self.note_mode else GREEN, (cx * tile + buffer, cy * tile + buffer, tile, tile))
        if self.solved:
            pygame.draw.rect(dis, GREEN, (buffer, buffer, end, end))
        pygame.draw.rect(dis, BLACK, (buffer, buffer, end, end), THICK)
        
        for i in range(1, 6):
            pygame.draw.line(dis, BLACK,
                (0   + buffer, i * tile + buffer),
                (end + buffer, i * tile + buffer),
                width = THICK if i % 2 == 0 else THIN)
            pygame.draw.line(dis, BLACK,
                (i * tile + buffer, 0   + buffer),
                (i * tile + buffer, end + buffer),
                width = THICK if i % 3 == 0 else THIN)
        
        # Draw numbers
        bf = buffer + tile / 2
        for r in range(6):
            for c in range(6):
                col = BLACK if (r, c) in self.clues else GREY
                x = c * tile + buffer
                y = r * tile + buffer
                if self.arr[r][c] != 0:
                    text(dis, str(self.arr[r][c]), x + tile/2, y + tile/2, font_size=100, font_color=col)
                else:
                    for v in range(6):
                        if self.notes[r][c][v]:
                            xx = (tile / 6) * (2 * (v % 3) + 1) # [1, 3, 5][v % 3]
                            yy = (tile / 3) * (v // 3 + 1) # [1, 2][v // 3]
                            text(dis, str(v+1), x + xx, y + yy, font_size=50, font_color=col)
        #pygame.display.update()

    def mouse_down(self, dis, tile, buffer, is_dragged, clicked) -> None:
        return None
        #self.render(dis, tile, buffer, is_dragged, clicked)
    
    # [[maybe_unused]]
    def mouse_drag(self, dis, tile, buffer, is_dragged, clicked) -> None:
        return None
    
    def key_pressed(self, dis, tile, buffer, is_dragged, clicked, key) -> None:
        if self.solved:
            return
        
        # Arrow keys to move selected tile
        if pygame.K_RIGHT <= key <= pygame.K_UP:
            match key:
                case pygame.K_UP:
                    clicked[1] -= tile
                case pygame.K_DOWN:
                    clicked[1] += tile
                case pygame.K_LEFT:
                    clicked[0] -= tile
                case pygame.K_RIGHT:
                    clicked[0] += tile
            #self.render(dis, tile, buffer, is_dragged, clicked)
        
        #  Shift toggles hint mode
        elif key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
            self.note_mode = not self.note_mode
        
        # Number (or backspace) pressed to enter digit
        elif pygame.K_0 <= key <= pygame.K_9 or key == pygame.K_BACKSPACE:
            val = key - pygame.K_0 if key != pygame.K_BACKSPACE else 0
            col = (clicked[0] - buffer) // tile
            row = (clicked[1] - buffer) // tile
            
            if not self.solved and 0 <= row < 6 and 0 <= col < 6 and (row, col) not in self.clues:
                # Making note
                if self.note_mode:
                    # Deleting all notes
                    if val == 0:
                        for i in range(6):
                            self.notes[row][col][i] = False
                    # Take/Remove one value
                    else:
                        self.notes[row][col][val-1] = not self.notes[row][col][val-1]
                # Filling in answer
                else:
                    self.arr[row][col] = val
                    if self.arr == self.key:
                        self.solved = True
                        self.note_mode = False
        
        #self.render(dis, tile, buffer, is_dragged, clicked)


'''
    +------------------+
    | Helper functions |
    +------------------+
'''

def generate() -> tuple[Board, Board]:
    '''
    Return (sudoku, solution) 6x6 boards
    '''
    key = [[0] * 6 for _ in range(6)]
    
    fill(key)
    
    cells = [(r, c) for r in range(6) for c in range(6)]
    shuffle(cells)

    board = [row[:] for row in key]
    
    # Try removing each cell, see if there is still 1 solution
    for r, c in cells:
        v = board[r][c]
        board[r][c] = 0

        # If there are now >1 solutions, undo the cell's removal
        arr = [row[:] for row in board]
        if num_solutions(arr) > 1:
            board[r][c] = v
        
    return (board, key)

def valid(arr: Board, row: int, col: int, val: int) -> bool:
    '''
    Determine whether `val` can be placed at position (`row`, `col`)
    '''
    R, C = row // 2 * 2, col // 3 * 3
    for i in range(6):
        if arr[i][col] == val or arr[row][i] == val or arr[R+i//3][C+i%3] == val:
            return False
    return True

def find_open(arr: Board) -> tuple[int, int] | None:
    for r in range(6):
        for c in range(6):
            if arr[r][c] == 0:
                return r, c
    return (-1, -1)

def fill(arr: Board) -> bool:
    r, c = find_open(arr)
    
    if r == -1 or c == -1:
        return True
    
    vals = [1, 2, 3, 4, 5, 6]
    shuffle(vals)
    
    for v in vals:
        if valid(arr, r, c, v):
            arr[r][c] = v
            if fill(arr):
                return True
            arr[r][c] = 0
    return False

def num_solutions(arr: Board) -> int:
    r, c = find_open(arr)
    
    # Grid filled -> 1 solution
    if r == -1 or c == -1:
        return 1
    
    # Recursively search for solutions
    solutions = 0
    for v in (1, 2, 3, 4, 5, 6):
        if valid(arr, r, c, v):
            arr[r][c] = v
            solutions += num_solutions(arr)
            arr[r][c] = 0
    return solutions
