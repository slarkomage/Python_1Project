import pygame
import sys
import time
import random
from button import Button

difficulty = 228  # дефолтная сложность
start_difficulty = 0
# Размер окна
frame_size_x = 720
frame_size_y = 480

check_errors = pygame.init()

if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Создаем экран
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Инициализируем цвета на будущее
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
light_blue = pygame.Color(0, 255, 255)

# ФПС контроллер
fps_controller = pygame.time.Clock()

# Спавн змейки
snake_pos = [100, 50]
snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
snake_color = green

# Спавн еды
food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
food_spawn = True

# Спавн бонуса (у нас замедляющий бонус будет)
bonus_spawn = False
bonus_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]

direction = 'RIGHT'
change_to = direction

score = 0



# Game Over
def game_over():
    my_font = pygame.font.SysFont('times', 90)
    game_over_surface = my_font.render('GAME OVER', True, white)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, white, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Отображение счета
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
        f = open('results.txt', 'r')
        list_of_results = f.readlines()
        f.close()
        for i in range(0, len(list_of_results)):
            j = list_of_results[i]
            if j[len(j) - 1] == '\n':
                j = j[0:len(j) - 1]
            list_of_results[i] = int(j)
        list_of_results.append(int(score))
        list_of_results.sort(reverse=True)
        best_score = list_of_results[0]
        f = open('results.txt', 'w')
        for j in list_of_results:
            f.write(str(j) + '\n')
        f.close()
        best_score_surface = score_font.render('Best Score : ' + str(best_score), True, color)
        best_score_rect = best_score_surface.get_rect()
        best_score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.15)
        game_window.blit(best_score_surface, best_score_rect)
    game_window.blit(score_surface, score_rect)


# Меню
objects = []
font = pygame.font.SysFont('Verdana', 20)
is_pressed = False


def set_difficulty(level):
    def setter():
        global difficulty
        global start_difficulty
        start_difficulty = level
        difficulty = level
        global is_pressed
        is_pressed = True

    return setter


def set_color(color):
    def setter():
        global snake_color
        snake_color = color
        global is_pressed
        is_pressed = True

    return setter


Button(235, 80, 250, 75, objects, 'Easy', set_difficulty(10))
Button(235, 155, 250, 75, objects, 'Medium', set_difficulty(25))
Button(235, 230, 250, 75, objects, 'Hard', set_difficulty(40))
Button(235, 305, 250, 75, objects, 'Harder', set_difficulty(60))
Button(235, 380, 250, 75, objects, 'ФПМИ ПМФ moment', set_difficulty(120))

while True:
    fps_controller.tick(30)
    game_window.fill(black)
    menu_surf = pygame.font.SysFont('times', 45).render('Выберите сложность:', True, white)
    menu_rect = menu_surf.get_rect()
    menu_rect.midtop = (frame_size_x / 2, 20)
    game_window.blit(menu_surf, menu_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for object in objects:
        object.process(game_window)
    if (is_pressed):
        time.sleep(0.5)
        objects.clear()
        break
    pygame.display.flip()

# Выбор цвета:

Button(235, 80, 250, 75, objects, 'Green', set_color(green))
Button(235, 155, 250, 75, objects, 'Red', set_color(red))
Button(235, 230, 250, 75, objects, 'Blue', set_color(blue))
Button(235, 305, 250, 75, objects, 'White', set_color(white))

is_pressed = False

while True:
    fps_controller.tick(30)
    game_window.fill(black)
    menu_surf = pygame.font.SysFont('times', 45).render('Выберите цвет:', True, white)
    menu_rect = menu_surf.get_rect()
    menu_rect.midtop = (frame_size_x / 2, 20)
    game_window.blit(menu_surf, menu_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for object in objects:
        object.process(game_window)
    if (is_pressed):
        break
    pygame.display.flip()
objects.clear()

# Game:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Передвигаем змейку
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Рост тела
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        difficulty += 0.5  # Делать ускорение со временем = криндж, делаем по еде
        food_spawn = False
    elif bonus_spawn and (snake_pos[0] == bonus_pos[0] and snake_pos[1] == bonus_pos[1]):
        score += 1
        difficulty /= 1.25
        bonus_spawn = False
    else:
        snake_body.pop()

    # Новое яблоко
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
        food_spawn = True
    # Новый бонус
    if not bonus_spawn:
        if random.randrange(0, 1100, 1) == 11:
            bonus_pos = [random.randrange(1, (frame_size_x // 10)) * 10,
                         random.randrange(1, (frame_size_y // 10)) * 10]
            bonus_spawn = True

    # Отрисовка
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, snake_color, pygame.Rect(pos[0], pos[1], 10, 10))

    # Еда
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    # Бонус
    if bonus_spawn:
        pygame.draw.rect(game_window, light_blue, pygame.Rect(bonus_pos[0], bonus_pos[1], 10, 10))
    # Проигрыш:
    # Выход за границу (ударились о край)
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
        game_over()
    # Сами в себя ударились
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, white, 'consolas', 20)
    # Обновляем экран
    pygame.display.update()
    fps_controller.tick(difficulty)

