import pygame
import sys

# Pygame'i başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Renkler
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Kuş pozisyonu
bird_x, bird_y = 100, 300
velocity = 0
gravity = 0.5
jump = -10

# Oyun döngüsü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            velocity = jump

    # Fizik
    velocity += gravity
    bird_y += velocity

    # Ekranı temizle ve çizim yap
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (bird_x, int(bird_y)), 20)  # Kuş

    pygame.display.flip()
    clock.tick(30)  # FPS
