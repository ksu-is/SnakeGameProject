# Hungry Snake by Kenneth Grassel

import pygame, sys, time, random
pygame.init()

# Difficulty
# Rookie = 15
# Average = 20
# Good = 30
# Great = 60
# Spectacular = 120
Difficulty = 15

# application size
frame_size_x = 1000
frame_size_y = 750
screen = pygame.display.set_mode((frame_size_x, frame_size_y))
game_state = "start_menu"
gameover = False
startmenu = True

# error check
check_errors = pygame.init()
if check_errors[1]>0:
    print(f'[!] Had {check_errors[1]} error when launching game, closing application...')
    sys.exit(-1)
else:
    print('[+] Launching Game...')

#game window
pygame.display.set_caption('Hungry Snake')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

#Game colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
forestgreen = pygame.Color(0, 50, 0)
green = pygame.Color(0, 255, 0)

#fps
fps_controller = pygame.time.Clock()

#Varibles
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True
         
direction = 'RIGHT'
change_to = direction

score = 0
# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('SCORE:' + str(score), True, white)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()

def start_menu():
    global startmenu
    screen.fill((0, 255, 0))
    font = pygame.font.SysFont('times new roman', 80)
    title = font.render('Hungry Snake', True, (255, 255, 255))
    start_button = font.render('game is loading....', True, (255, 255, 255))
    screen.blit(title, (frame_size_x/2 - title.get_width()/2, frame_size_y/2 - title.get_height()/2))
    screen.blit(start_button, (frame_size_x/2 - start_button.get_width()/2, frame_size_y/2 + start_button.get_height()/2))
    pygame.display.update()
    time.sleep(1)
    startmenu = True
    
# Game Over
def game_over():
    global gameover
    my_font = pygame.font.SysFont('times new roman', 80)
    restart_game = pygame.font.SysFont('time new roman', 40)
    game_over_surface = my_font.render('GAME OVER..', True, white)
    restart_game_surface = restart_game.render('press SPACEBAR to play again, or ESC to exit...', True, white )
    game_over_rect = game_over_surface.get_rect()
    restart_game_rect = restart_game_surface.get_rect()
    game_over_rect.midtop = (500, 300)
    restart_game_rect.midtop = (500, 500)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    game_window.blit(restart_game_surface, restart_game_rect)
    show_score(0, white, 'times', 20)
    pygame.display.update()
    time.sleep(1)
    gameover = True 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
                game_state = False
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
                game_state = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
                game_state = False
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
                game_state = False
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.key == pygame.K_SPACE:
                 food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
                 food_spawn = True
                 snake_pos = [100, 50]
                 snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
                 direction = 'RIGHT'
                 change_to = direction
                 score = 0
                 gameover = False  
        if game_state == "start_menu":
            start_menu()
            
# Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    # GFX
    game_window.fill(forestgreen)
    for pos in snake_body:
        # Snake body
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Game Over conditions
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, black, 'consolas', 20)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(Difficulty)
    