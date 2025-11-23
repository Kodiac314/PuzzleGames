from Base import *
from random import randrange, shuffle

SZ = 6

class Zips(template):
    def __init__(self):
        self.grid = [[0] * SZ for _ in range(SZ)]
        self.clues, self.walls = generate()
        
        self.path = [self.clues[0]]
        self.grid[self.path[0][0]][self.path[0][1]] = 1
        
        self.solved = False
    
    def init(self, width: int, height: int) -> tuple[int, int]:
        tile   = min(width*6/7 / SZ * SPACER, height / SZ * SPACER)
        buffer = min(width*6/7 - SZ * tile,   height - SZ * tile) / 2
        return int(tile), int(buffer)
    
    def render(self, dis, tile, buffer, is_dragged, clicked) -> None:
        dis.fill((125, 125, 125))
        
        # Draw grid lines
        end = tile * SZ
        if self.solved:
            pygame.draw.rect(dis, GREEN, (buffer, buffer, end, end))
        pygame.draw.rect(dis, BLACK, (buffer, buffer, end, end), THICK)
        for i in range(1, SZ):
            pygame.draw.line(dis, BLACK,
                (0   + buffer, i * tile + buffer),
                (end + buffer, i * tile + buffer), width = THIN)
            pygame.draw.line(dis, BLACK,
                (i * tile + buffer, 0   + buffer),
                (i * tile + buffer, end + buffer), width = THIN)
        
        # Draw path
        for i in range(len(self.path)):
            pygame.draw.circle(dis, ORANGE, (self.path[i][1]*tile + buffer + tile/2, self.path[i][0]*tile + buffer + tile/2), int(tile * 0.2))
            if i + 1 == len(self.path):
                continue
            r, c = self.path[i]
            rr, cc = self.path[i+1]
            pygame.draw.line(dis, ORANGE,
                (c*tile + buffer + tile/2, r*tile + buffer + tile/2),
                (cc*tile + buffer + tile/2, rr*tile + buffer + tile/2), width = int(tile * 0.4))
        
        # Draw clues and walls
        for i, (r, c) in enumerate(self.clues, 1):
            text(dis, str(i), c*tile + buffer + tile/2, r*tile + buffer + tile/2, font_size=100)
        for r in range(SZ):
            for c in range(SZ):
                x, y = c*tile + buffer, r*tile + buffer    
                if self.walls[r][c][0]:
                    pygame.draw.line(dis, BLACK, (x, y), (x + tile, y), width=THICK)
                if self.walls[r][c][1]:
                    pygame.draw.line(dis, BLACK, (x, y), (x, y + tile), width=THICK)
    
    def mouse_down(self, dis, tile, buffer, is_dragged, clicked) -> None:
        return None
    
    def mouse_drag(self, dis, tile, buffer, is_dragged, clicked) -> None:
        if self.solved:
            return None
        
        cx, cy = (clicked[0] - buffer) // tile, (clicked[1] - buffer) // tile
        if not (0 <= cx < SZ and 0 <= cy < SZ):
            return None
        
        # Backtracking the line
        if self.grid[cy][cx] == len(self.path)-1 and len(self.path) > 1:
            r, c = self.path.pop()
            self.grid[r][c] = 0
            return
        
        # Adding to the line
        if self.grid[cy][cx] != 0:
            return
        for i in range(4):
            nr, nc = cy + D[i], cx + D[i+1]
            if 0 <= nr < SZ and 0 <= nc < SZ and self.grid[nr][nc] == len(self.path):
                self.path.append((cy, cx))
                self.grid[cy][cx] = len(self.path)
                break
        if all(0 not in row for row in self.grid):
            self.solved = True
    
    def key_pressed(self, dis, tile, buffer, is_dragged, clicked, key) -> None:
        '''
        key  Pygame.event.key (int)  representation of some keyboard symbol
        '''
        return None


'''
    +------------------+
    | Helper functions |
    +------------------+
'''

def generate() -> tuple[Board, list[tuple[int, int]]]:
    '''
    rtype   (board, walls)
     board  (int, int)[]    ordered sequence of points to hit
     walls  [7][7]bool      binary matrix marking wall segments
    '''
    grid = [[0] * SZ for _ in range(SZ)]
    path = []
    
    # Init some Hamiltonian path
    sr, sc = randrange(SZ), randrange(SZ)
    fill(grid, path, sr, sc)
    
    print(*grid, sep='\n')
    
    # Randomly pick only a few points to show
    i = 0
    checkpoints = []
    while i < len(path):
        checkpoints.append(path[i])
        i += randrange(3, 7)
    if i + 1 != len(path):
        checkpoints[-1] = path[-1]
    
    # Randomly sample for walls
    walls = [[[False] * 4 for _ in range(SZ + 1)] for _ in range(SZ + 1)]
    for _ in range(SZ * SZ // 2):
        r, c = randrange(SZ), randrange(SZ)
        if r > 0 and abs(grid[r][c] - grid[r-1][c]) > 1:
            walls[r][c][0] = True
        if c > 0 and abs(grid[r][c] - grid[r][c-1]) > 1:
            walls[r][c][1] = True
    
    # DEBUG demo print
    grid2 = [[0] * SZ for _ in range(SZ)]
    for i,(r,c) in enumerate(checkpoints, 1):
        grid2[r][c] = i
    
    
    print(*grid2, sep='\n')
    
    return checkpoints, walls

D = [1, 0, -1, 0, 1]
TARGET = SZ * SZ

def fill(grid: list[list[int]], path: list[list[int]], row: int, col: int) -> bool:
    path.append((row, col))
    grid[row][col] = len(path)
    
    if len(path) == TARGET:
        return True
    
    adj = [0, 1, 2, 3]
    shuffle(adj)
    
    for i in range(4):
        j = adj[i]
        nr, nc = row + D[j], col + D[j+1]
        
        if 0 <= nr < SZ and 0 <= nc < SZ and grid[nr][nc] == 0:
            if fill(grid, path, nr, nc):
                return True
    grid[row][col] = 0
    path.pop()
    return False
