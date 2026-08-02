import pygame as p
import random
import numpy as np
import pygame.mixer as mixer

mixer.init()
c1 = mixer.Sound("tones/c1.wav")
c2 = mixer.Sound("tones/c2.wav")
c3 = mixer.Sound("tones/c3.wav")
c4 = mixer.Sound("tones/c4.wav")
c5 = mixer.Sound("tones/c5.wav")
c6 = mixer.Sound("tones/c6.wav")

p.init()
clock = p.time.Clock()

WIDTH, HEIGHT = (900, 632)
ROWS, COLUMNS = 100,100
CELL_SIZE = WIDTH//COLUMNS

grid = np.random.choice([0,1], size = (ROWS, COLUMNS), p=[0.9, 0.1])

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
            new_grid = grid

            if alive and n < 2:
                # Underpopulation
                new_grid[row][col] = 0
                if(random.choice([1, 2]))==1:
                    c1.play()
                else:
                    c2.play()

            elif alive and (n == 2 or n == 3):
                # Survives
                new_grid[row][col] = 1
                if(random.choice([1, 2]))==1:
                    c3.play()
                else:
                    c4.play()

            elif alive and n > 3:
                # Overpopulation
                new_grid[row][col] = 0
                c5.play()

            elif not alive and n == 3:
                # Reproduction
                new_grid[row][col] = 1
                c6.play()  

            grid = new_grid

    

    clock.tick(20)

    p.display.flip()
       
p.quit()