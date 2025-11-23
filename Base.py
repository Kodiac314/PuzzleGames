import pygame
Board = list[list[int]]


# Colors
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
WHITE = (200, 200, 200)
BLUE = (17, 188, 214)
GREEN = (8, 168, 43)
ORANGE = (184, 123, 11)

# Display helper
def text(dis, msg: str, x: float, y: float, font_size: int = 50, font_color = BLACK) -> None:
    '''
    dis         pygame.display   surface drawn on
    msg         str              message to be displayed
    x, y        (int, int)       position (centered) for textbox to be rendered
    font_size   int              size of font
    font_color  (int, int, int)  color of font
    '''
    font = pygame.font.Font(None, font_size)
    text = font.render(msg, True, font_color)
    text_rect = text.get_rect(center=(x, y))
    dis.blit(text, text_rect)


# Line weight
THIN = 5
THICK = 10
# Rendering proportions (% whitespace buffer)
SPACER = 0.95


class template:
    
    def init(self, width, height) -> tuple[int, int]:
        '''
        width   int  maximum display width in pixels
        height  int
        
        tile        int             size in pixels of tile length
        buffer      int             offset from (0, 0)       
        '''
        self.arr = []
        self.solved = False
    
    def render(self, dis, tile, buffer, is_dragged, clicked) -> None:
        '''
        dis         Pygame.display  surface drawn on
        tile        int             size in pixels of tile length
        buffer      int             offset from (0, 0)
        is_dragged  bool            whether mouse is pressed while moved
        clicked     (int, int)      board indices of mouse click
        
        rtype       None            rendering is drawn onto `dis`       
        '''
    
    def mouse_down(self, dis, tile, buffer, is_dragged, clicked) -> None:
        return None
    
    def mouse_drag(self, dis, tile, buffer, is_dragged, clicked) -> None:
        return None
    
    def key_pressed(self, dis, tile, buffer, is_dragged, clicked, key) -> None:
        '''
        key  Pygame.event.key (int)  representation of some keyboard symbol
        '''
        return None