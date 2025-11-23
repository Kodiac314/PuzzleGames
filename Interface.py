
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
    render_logo(lf, up, BG_BLUE)
    pygame.draw.line(dis, BLACK, (lf + tile*0.2 - THIN/4, up + tile*0.5), (lf + tile*0.8 + THIN/4, up + tile*0.5), width=THIN)
    pygame.draw.line(dis, BLACK, (lf + tile*0.5, up + tile*0.2 - THIN/4), (lf + tile*0.5, up + tile*0.8 + THIN/4), width=THIN)
    for i in range(3):
        text(dis, str(i+1), lf + tile*[0.35, 0.65][i % 2], up + tile*[0.35, 0.65][i // 2], font_size=50)
    
    # Zips logo
    up += tile + buffer
    render_logo(lf, up, ORANGE)
    for i in range(5):
        x = [0.35, 0.5, 0.5, 0.5, 0.65][i]
        y = [0.35, 0.35, 0.5, 0.65, 0.65][i]
        pygame.draw.circle(dis, ORANGE, (lf+tile*x, up+tile*y), tile*0.1)
    for i in range(3):
        x = [0.35, 0.5, 0.5, 0.5, 0.5, 0.65][2*i:2*i+2]
        y = [0.35, 0.35, 0.35, 0.65, 0.65, 0.65][2*i:2*i+2]
        pygame.draw.line(dis, ORANGE,
                        (lf+tile*x[0], up+tile*y[0]),
                        (lf+tile*x[1], up+tile*y[1]), width=int(tile*0.2))
    
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
            
pygame.quit()
