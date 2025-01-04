import pygame
import sys
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")

# Renkler
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SKY_BLUE = (135, 206, 235)

# Kuş pozisyonu
bird_x, bird_y = 100, 300
velocity = 0
gravity = 0.5
jump = -10

# Oyun seviyesi ve zorluk
level = 1
pipes_passed = 0
PIPES_PER_LEVEL = 3

# Engel parametreleri
pipe_width = 50
pipe_gaps = {1: 400, 2: 350, 3: 300}  # Her seviye için farklı boşluk mesafeleri
pipe_x = WIDTH
pipe_height = random.randint(150, 400)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 2000)  # Borular arası mesafeyi artırmak için süreyi artırdık

# Puan
score = 0
font = pygame.font.Font(None, 36)

def create_pipe():
    height = random.randint(200, 400)
    bottom_pipe = pygame.Rect(WIDTH, height, pipe_width, HEIGHT - height)
    
    # Seviye 1'de sadece alt borular
    if level == 1:
        return [bottom_pipe]
    
    # Diğer seviyelerde üst ve alt borular
    gap = pipe_gaps[level]
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height - gap)
    return [bottom_pipe, top_pipe]

def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= 3
    return [pipe for pipe in pipes if pipe.x > -pipe_width]

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def check_collision(pipes, bird_rect):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    return False

# Oyun döngüsü
running = True
game_active = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                velocity = jump
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_y = 300
                velocity = 0
                score = 0
                level = 1
                pipes_passed = 0
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

    if game_active:
        # Fizik
        velocity += gravity
        bird_y += velocity

        # Engelleri hareket ettir
        old_pipe_count = len(pipe_list)
        pipe_list = move_pipes(pipe_list)
        
        # Geçilen boruları say
        if old_pipe_count > len(pipe_list):
            pipes_passed += 1
            score += 1
            
            # Seviye kontrolü
            if pipes_passed >= PIPES_PER_LEVEL and level < 3:
                level += 1
                pipes_passed = 0

        # Çarpışma kontrolü
        bird_rect = pygame.Rect(bird_x - 20, bird_y - 20, 40, 40)
        if check_collision(pipe_list, bird_rect):
            game_active = False

    # Ekranı temizle ve çizim yap
    screen.fill(SKY_BLUE)
    
    if game_active:
        # Kuş
        pygame.draw.circle(screen, BLUE, (bird_x, int(bird_y)), 20)
        # Engeller
        draw_pipes(pipe_list)
        # Skor ve Seviye
        score_text = font.render(f'Skor: {score}', True, WHITE)
        level_text = font.render(f'Seviye: {level}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
    else:
        # Oyun bitiş ekranı
        game_over_text = font.render('OYUN BİTTİ - TEKRAR BAŞLAMAK İÇİN BOŞLUK', True, WHITE)
        score_text = font.render(f'Skor: {score}', True, WHITE)
        level_text = font.render(f'Ulaşılan Seviye: {level}', True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 200, HEIGHT//2))
        screen.blit(score_text, (WIDTH//2 - 50, HEIGHT//2 + 50))
        screen.blit(level_text, (WIDTH//2 - 70, HEIGHT//2 + 100))

    pygame.display.flip()
    clock.tick(30)  # FPS
