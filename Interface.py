
from pyautogui import size
import pygame
pygame.init()

from Base import *
from Sudoku import Sudoku # 6x6
from Zips import Zips # 7x7


''' ----- PYGAME SETUP -------------------- '''

SCREEN_W, SCREEN_H = size() # 1400, 700
SCREEN_W, SCREEN_H = int(SCREEN_W * 0.8), int(SCREEN_H * 0.8)

pygame.init()
dis = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Puzzle Games')


''' ----- GAME LOOP VARIABLES ------------- '''
run = True
game = Sudoku()
tile, buffer = game.init(SCREEN_W, SCREEN_H)
is_dragged = False
clicked = [0, 0]


''' ----- Render functions ----------------- '''
def render_logo(lf: float, up: float, col) -> None:
    pygame.draw.rect(dis, col, (lf, up, tile, tile))
    pygame.draw.rect(dis, BLACK, (lf, up, tile, tile), THIN)
    pygame.draw.rect(dis, WHITE, (lf + tile*0.2, up + tile*0.2, tile*0.6, tile*0.6))
    for i in range(2):
        j = [0.2, 0.8][i]
        pygame.draw.line(dis, BLACK, # Horizontal
            (lf + tile*0.2 - THIN/4, up + tile*j), (lf + tile*0.8 + THIN/4, up + tile*j), width=THIN)
        pygame.draw.line(dis, BLACK, # Vertical
            (lf + tile*j, up + tile*0.2 - THIN/4), (lf + tile*j, up + tile*0.8 + THIN/4), width=THIN)

def render() -> None: # basically Macro to plug in arguments
    game.render(dis, tile, buffer, is_dragged, clicked)
    
    # Sudoku logo
    lf, up = SCREEN_W - tile - buffer, buffer
    render_logo(lf, up, ORANGE)
    
    pygame.draw.line(dis, BLACK, (lf + tile*0.2 - THIN/4, up + tile*0.5), (lf + tile*0.8 + THIN/4, up + tile*0.5), width=THIN)
    pygame.draw.line(dis, BLACK, (lf + tile*0.5, up + tile*0.2 - THIN/4), (lf + tile*0.5, up + tile*0.8 + THIN/4), width=THIN)
    for i in range(3):
        text(dis, str(i+1), lf + tile*[0.35, 0.65][i % 2], up + tile*[0.35, 0.65][i // 2], font_size=50)
    
    # Zips logo
    up += tile + buffer
    render_logo(lf, up, (12, 77, 207))
    
    # 3rd logo
    up += tile + buffer
    render_logo(lf, up, (25, 87, 6))
    
    # 4th logo
    up += tile + buffer
    render_logo(lf, up, (133, 7, 128))
    
    # 5th logo
    up += tile + buffer
    render_logo(lf, up, (122, 34, 7))
    
    pygame.display.update()


''' ----- GAME LOOP  ---------------------- '''
render()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # exit game
                run = False
            
            if event.key == pygame.K_p:
                print(*game.grid, sep='\n')
                print(game.path)
            
            else:
                game.key_pressed(dis, tile, buffer, is_dragged, clicked, event.key)
                render()
        
        if event.type == pygame.MOUSEBUTTONUP:
            is_dragged = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_dragged = True
            clicked = list(pygame.mouse.get_pos())
            
            # Selecting event
            if clicked[0] >= SCREEN_W - tile - buffer:
                lf = SCREEN_W - tile - buffer
                for i in range(5):
                    up = buffer + (tile + buffer) * i
                    if lf <= clicked[0] <= lf + tile and up <= clicked[1] <= up + tile:
                        game = [Sudoku, Zips][i]()
                        tile, buffer = game.init(SCREEN_W, SCREEN_H)
                        break
            
            # Interacting with game
            else:
                game.mouse_down(dis, tile, buffer, is_dragged, clicked)
            render()
        
        if is_dragged and event.type == pygame.MOUSEMOTION:
            clicked = list(pygame.mouse.get_pos())
            game.mouse_drag(dis, tile, buffer, is_dragged, clicked)
            render()
            
#             x, y = find(pygame.mouse.get_pos())
#             
#             # Clicked on board
#             if 0 <= x < W and 0 <= y < H:
#                 # Find board indices
#                 r, c = int(y / V_SIZE), int(x / SIZE)
#                 for i in (r-1, r, r+1):
#                     pc, pr = c * SIZE, i * V_SIZE
#                     pts = [(pc, pr), (pc + SIZE, pr - V_SIZE), (pc + SIZE, pr + V_SIZE)] if (c+i)%2 else [(pc, pr - V_SIZE), (pc, pr + V_SIZE), (pc + SIZE, pr)]
#                     if contains((x, y), *pts):
#                         r = i
#                         break
#                 # Update board        
#                 board.arr[r][c] = color_idx
#                 render(board, palette, color_idx)
#                 continue
#             
#             # Clicked to change color
#             SZ, INC = 2/3 * Board.BUFFER * SIZE, 1/6 * Board.BUFFER * SIZE
#             if W+INC <= x < B-INC and INC <= y < H-INC:
#                 for i in range(len(palette)):
#                     lf, up = W + INC, i * (SZ + INC)
#                     if lf <= x < lf + SZ and up <= y < up + SZ:
#                         color_idx = i
#                         break
#             
#             # Clicked to restart level
#             lf, up = W + INC, len(palette) * (SZ + INC)
#             if lf <= x < lf + SZ and up <= y < up + SZ:
#                 if board.solved():
#                     puzzle_idx = min(puzzle_idx + 1, len(PUZZLES)-1)
#                 board = Board(PUZZLES[puzzle_idx])
#     
#             # render(board, Palette.GREYS, color_idx)

pygame.quit()



