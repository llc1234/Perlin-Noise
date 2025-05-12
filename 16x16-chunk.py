import pygame
import random


# --- Settings ---
WIDTH, HEIGHT = 500, 500
SCALE = 100.0
OCTAVES = 6
PERSISTENCE = 0.5
LACUNARITY = 2.0

SEED = random.randint(10, 10000)  # Map Seed

CHUNK_SIZE = 16
random.seed(SEED)

# --- Custom Perlin Noise Implementation ---

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    return a + t * (b - a)

def grad(hash, x, y):
    h = hash & 3
    u = x if h < 2 else y
    v = y if h < 2 else x
    return (u if h & 1 == 0 else -u) + (v if h & 2 == 0 else -v)

# Initialize permutation table with seed
p = list(range(256))
random.shuffle(p)
p = p * 2  # duplicate list

def perlin(x, y):
    xi = int(x) & 255
    yi = int(y) & 255

    xf = x - int(x)
    yf = y - int(y)

    u = fade(xf)
    v = fade(yf)

    aa = p[p[xi] + yi]
    ab = p[p[xi] + yi + 1]
    ba = p[p[xi + 1] + yi]
    bb = p[p[xi + 1] + yi + 1]

    x1 = lerp(grad(aa, xf, yf), grad(ba, xf - 1, yf), u)
    x2 = lerp(grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1), u)

    return (lerp(x1, x2, v) + 1) / 2  # Normalize to [0, 1]

# --- Chunk Generation ---

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def generate_chunk(chunk_x, chunk_y, chunk_size, width, height, scale, octaves, persistence, lacunarity):
    noise_chunk = [[0 for _ in range(chunk_size)] for _ in range(chunk_size)]

    for dy in range(chunk_size):
        for dx in range(chunk_size):
            x = chunk_x + dx
            y = chunk_y + dy

            if x >= width or y >= height:
                continue

            amplitude = 1
            frequency = 1
            noise_height = 0

            for _ in range(octaves):
                sample_x = x / scale * frequency
                sample_y = y / scale * frequency

                noise_val = perlin(sample_x, sample_y)
                noise_height += noise_val * amplitude

                amplitude *= persistence
                frequency *= lacunarity

            value = int(noise_height / octaves * 255)
            noise_chunk[dy][dx] = clamp(value, 0, 255)

    return noise_chunk

# --- Drawing One Chunk ---

def draw_chunk(screen, chunk, chunk_x, chunk_y):
    for dy in range(len(chunk)):
        for dx in range(len(chunk[0])):
            x = chunk_x + dx
            y = chunk_y + dy
            if x >= WIDTH or y >= HEIGHT:
                continue
            value = chunk[dy][dx]

            if value < 25:
                color = (90, 90, 90)
            elif value < 30:
                color = (120, 120, 120)
            elif value < 35:
                color = (190, 190, 190)
            elif value < 40:
                color = (220, 220, 220)
            elif value < 45:
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)
            screen.set_at((x, y), color)

# --- Main ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Chunked Perlin Noise Map (Seed: {SEED})")

    for y in range(0, HEIGHT, CHUNK_SIZE):
        for x in range(0, WIDTH, CHUNK_SIZE):
            chunk = generate_chunk(x, y, CHUNK_SIZE, WIDTH, HEIGHT, SCALE, OCTAVES, PERSISTENCE, LACUNARITY)
            draw_chunk(screen, chunk, x, y)
            pygame.display.update(pygame.Rect(x, y, CHUNK_SIZE, CHUNK_SIZE))  # optional: only update the chunk

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
