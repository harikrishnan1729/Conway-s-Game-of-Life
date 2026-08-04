import pygame as p
import numpy as np
import pygame.mixer as mixer
from numpy.lib.stride_tricks import sliding_window_view

# ------------------ INITIALIZATION ------------------

mixer.init(frequency=44100, size=-16, channels=1)
p.init()

WIDTH, HEIGHT = 900, 900
ROWS, COLUMNS = 100, 100
CELL_SIZE = WIDTH // COLUMNS

screen = p.display.set_mode((WIDTH, HEIGHT))
clock = p.time.Clock()

# ------------------ LOAD SOUNDS ------------------

c1 = mixer.Sound("tones/c7.wav")
c2 = mixer.Sound("tones/c2.wav")
c3 = mixer.Sound("tones/c3.wav")
c4 = mixer.Sound("tones/c4.wav")
c5 = mixer.Sound("tones/c5.wav")
c6 = mixer.Sound("tones/c6.wav")

# Slightly lower volume (less harsh)
for sound in [c1, c2, c3, c4, c5, c6]:
    sound.set_volume(0.6)

# Dedicated channel for every pattern
channels = {
    "block": mixer.Channel(0),
    "glider": mixer.Channel(1)
}

# ------------------ PATTERNS ------------------

patterns = {
    "block": (
        np.array([
            [1, 1],
            [1, 1]
        ]),
        c3
    ),

    "glider": (
        np.array([
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]),
        c5
    )
}

last_count = {name: 0 for name in patterns}
last_played = {name: 0 for name in patterns}

COOLDOWN_MS = 250

FADE_IN = 100
FADE_OUT = 300

# ------------------ GRID ------------------

grid = np.random.choice(
    [0, 1],
    size=(ROWS, COLUMNS),
    p=[0.85, 0.15]
)

generation = 0

# ------------------ FUNCTIONS ------------------

def inside(r, c):
    return 0 <= r < ROWS and 0 <= c < COLUMNS


def play_note(name, sound):
    channel = channels[name]

    if channel.get_busy():
        channel.fadeout(FADE_OUT)

    channel.play(sound, fade_ms=FADE_IN)


def check_patterns(grid):
    now = p.time.get_ticks()

    for name, (pat, sound) in patterns.items():

        windows = sliding_window_view(grid, pat.shape)

        count = np.sum(
            np.all(windows == pat, axis=(2, 3))
        )

        if (
            count > last_count[name]
            and now - last_played[name] > COOLDOWN_MS
        ):
            play_note(name, sound)
            last_played[name] = now

        last_count[name] = count


# ------------------ MAIN LOOP ------------------

running = True

while running:

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Draw grid
    for row in range(ROWS):
        for col in range(COLUMNS):

            rect = (
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            if grid[row][col]:
                p.draw.rect(screen, (255, 245, 0), rect)
            else:
                p.draw.rect(screen, (40, 40, 40), rect)

            p.draw.rect(screen, (0, 0, 0), rect, 1)

    # Game of Life
    new_grid = grid.copy()

    for row in range(ROWS):
        for col in range(COLUMNS):

            neighbours = 0

            for i in range(-1, 2):
                for j in range(-1, 2):

                    if i == 0 and j == 0:
                        continue

                    nr = row + i
                    nc = col + j

                    if inside(nr, nc):
                        neighbours += grid[nr][nc]

            alive = grid[row][col]

            if alive:

                if neighbours < 2:
                    new_grid[row][col] = 0

                elif neighbours > 3:
                    new_grid[row][col] = 0

            else:

                if neighbours == 3:
                    new_grid[row][col] = 1

    grid = new_grid
    generation += 1

    check_patterns(grid)

    p.display.flip()
    clock.tick(30)

p.quit()