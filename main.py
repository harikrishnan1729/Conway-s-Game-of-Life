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
WIDTH, HEIGHT = (1200, 900)
ROWS, COLUMNS = 120,120
CELL_SIZE = WIDTH//COLUMNS
generation = 0

glider = np.array([
    [0, 0, 1],
    [1, 0, 1],
    [0, 1, 1]
])

patterns = {
    "glider": (glider, c5)
}

gliders = [
    glider,
    np.rot90(glider, 1),
    np.rot90(glider, 2),
    np.rot90(glider, 3)
]

def check_patterns(grid):
    count = 0
    for pat in gliders:
        windows = sliding_window_view(grid, pat.shape)

        count += np.sum(
            np.all(windows == pat, axis=(2,3))
        )
    return count



''' karplus crazy good ngl but not much use '''
# def karplus(frequency):
#     sample_rate = 44100
#     delay = int(sample_rate / frequency)
#     buffer = np.random.uniform(-1, 1, delay)
#     samples = []
#     for _ in range(44100):
#         samples.append(buffer[0])

#         first = buffer[0]
#         second = buffer[1]

#         new_sample = 0.996 * (first + second) / 2

#         buffer = np.append(buffer[1:], new_sample)

#     samples = np.array(samples)
#     samples = samples / np.max(np.abs(samples))
#     audio = (samples * 32767).astype(np.int16)
#     audio = np.column_stack((audio, audio))
#     sound = p.sndarray.make_sound(audio)
#     sound.play()
#     p.time.wait(2000)


grid = np.random.choice([0,1], size = (ROWS, COLUMNS), p=[0.9, 0.1])
screen = p.display.set_mode((WIDTH, HEIGHT))
running = True

def generate_tone(freq, duration=0.3):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = (
    np.sin(2*np.pi*freq*t)
    + 0.4*np.sin(2*np.pi*freq*2*t)
    + 0.2*np.sin(2*np.pi*freq*3*t)
    )

    phase = 0
    phase += 2*np.pi*freq*duration
    phase %= 2*np.pi

    fade = int(sample_rate * 0.05)
    envelope = np.ones(len(wave))
    envelope[:fade] = np.linspace(0,1,fade)
    envelope[-fade:] = np.linspace(1,0,fade)
    wave *= envelope
    wave /= np.max(np.abs(wave))
    audio = (wave * 32767 * 0.01).astype(np.int16)
    audio = np.column_stack((audio, audio))
    # print(audio.shape)
    return p.sndarray.make_sound(audio)


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
    notes = [
        130.81,  # C3
        146.83,  # D3
        164.81,  # E3
        174.61,  # F3
        196.00,  # G3
        220.00,  # A3
        246.94,  # B3

        261.63,  # C4
        293.66,  # D4
        329.63,  # E4
        349.23,  # F4
        392.00,  # G4
        440.00,  # A4
        493.88,  # B4

        523.25   # C5
    ]


    glider_count = check_patterns(grid)
    # if glider_count>0:
    #     print(glider_count)
    #     g_tone = generate_tone(100, duration=3)
    #     g_tone.play()

    population = np.sum(grid)
    # print(population % len(notes))
    freq = notes[population % len(notes)]
    tone = generate_tone(freq, duration=5)
    tone.play()
    mixer.set_num_channels(4)
    # print(mixer.get_num_channels())

    # if generation % 5 == 0:
    #     print(np.sum(grid))
    #     tone = generate_tone(np.sum(grid))
    #     tone.play()
    #     generation = 0


    clock.tick(30)
    p.display.flip()
       
p.quit()