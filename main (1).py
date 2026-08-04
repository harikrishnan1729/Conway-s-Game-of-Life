import pygame as p
import random
import numpy as np
import pygame.mixer as mixer
from numpy.lib.stride_tricks import sliding_window_view

mixer.init(frequency = 44100, size=-16, channels=1)

c1 = mixer.Sound("tones/c1.wav")
c2 = mixer.Sound("tones/c2.wav")
c3 = mixer.Sound("tones/c3.wav")
c4 = mixer.Sound("tones/c4.wav")
c5 = mixer.Sound("tones/c5.wav")
c6 = mixer.Sound("tones/c6.wav")

p.init()
clock = p.time.Clock()
WIDTH, HEIGHT = (900, 900)
ROWS, COLUMNS = 100,100
CELL_SIZE = WIDTH//COLUMNS
generation = 0


# pattern (fixed orientation) -> sound, and a count of matches last frame
patterns = {
    "block":   (np.array([[1,1],[1,1]]), c1),
    "blinker": (np.array([[1,1,1]]), c2),
    "glider":  (np.array([[0,1,0],[0,0,1],[1,1,1]]), c3),
}
last_count = {name: 0 for name in patterns}

def check_patterns(grid):
    for name, (pat, snd) in patterns.items():
        windows = sliding_window_view(grid, pat.shape)
        count = np.sum(np.all(windows == pat, axis=(2, 3)))
        if count > last_count[name]:
            snd.play()
        last_count[name] = count


grid = np.random.choice([0,1], size = (ROWS, COLUMNS), p=[0.85, 0.15])
screen = p.display.set_mode((WIDTH, HEIGHT))
running = True


def inside(a, b):
    if 0<=a<ROWS and 0<=b<COLUMNS:
        return True

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    screen.fill((0,0,0))
    for row in range(ROWS):
        for col in range(COLUMNS):
            n = 0
            alive = grid[row][col]
                
            rect = (
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            
            if alive:
                p.draw.rect(screen, (255, 245, 0), rect)
                    
            else:
                p.draw.rect(screen, (40, 40, 40), rect)
            p.draw.rect(screen, (0, 0, 0), rect, 1)

    new_grid = grid.copy()
    for row in range(ROWS):
        for col in range(COLUMNS):
            
            
            n=0
            temp_row = row
            temp_col = col
            alive = grid[row][col]        

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == j == 0:
                        continue
                    if inside(temp_row+i, temp_col+j):
                        if grid[temp_row+i][temp_col+j] == 1:
                            n += 1
                            # s1.play()
            # print(f"co-ordinate {row}, {col} has {n} neibghours")

            if alive and n < 2:
                # Underpopulation
                new_grid[row][col] = 0


            elif alive and (n == 2 or n == 3):
                # Survives
                new_grid[row][col] = 1

            elif alive and n > 3:
                # Overpopulation
                new_grid[row][col] = 0

            elif not alive and n == 3:
                # Reproduction
                new_grid[row][col] = 1

    grid = new_grid
    generation += 1

    check_patterns(grid)

    clock.tick(30)
    p.display.flip()
       
p.quit()
