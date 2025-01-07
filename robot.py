import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Программируемый робот")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Загрузка изображений
robot_img = pygame.image.load("robot.png")
battery_img = pygame.image.load("battery.png")
goal_img = pygame.image.load("goal.png")
spike_img = pygame.image.load("spikes.png")
wall_img = pygame.image.load("wall.png")
saw_img = pygame.image.load("saw.png")

# Масштабирование изображений
CELL_SIZE = 64
robot_img = pygame.transform.scale(robot_img, (CELL_SIZE, CELL_SIZE))
battery_img = pygame.transform.scale(battery_img, (CELL_SIZE, CELL_SIZE))
goal_img = pygame.transform.scale(goal_img, (CELL_SIZE, CELL_SIZE))
spike_img = pygame.transform.scale(spike_img, (CELL_SIZE, CELL_SIZE))
wall_img = pygame.transform.scale(wall_img, (CELL_SIZE, CELL_SIZE))
saw_img = pygame.transform.scale(saw_img, (CELL_SIZE, CELL_SIZE))

# Шрифт
font = pygame.font.SysFont(None, 48)

# Рисование игрового поля
def draw_grid():
    rows = SCREEN_HEIGHT // CELL_SIZE
    cols = SCREEN_WIDTH // CELL_SIZE
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

# Отображение текста
def draw_text(text, color, y_offset=0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

# Уровни
levels = [
    {"robot_start": [0, 0], "battery_pos": [2, 2], "goal_pos": [5, 5], "spike_pos": [], "wall_pos": [], "saw_path": [], "energy": 20},
    {"robot_start": [0, 0], "battery_pos": [4, 4], "goal_pos": [6, 6], "spike_pos": [], "wall_pos": [], "saw_path": [], "energy": 10},
    {"robot_start": [0, 0], "battery_pos": [4, 3], "goal_pos": [6, 6], "spike_pos": [[3, 3], [3, 4]], "wall_pos": [], "saw_path": [], "energy": 12},
    {"robot_start": [0, 0], "battery_pos": [3, 2], "goal_pos": [6, 6], "spike_pos": [[4, 2], [4, 3]],
     "wall_pos": [[1, 1], [1, 2], [1, 3], [2, 3], [3, 3], [5, 4]], "saw_path": [], "energy": 15},
    {
    "robot_start": [0, 0],
    "battery_pos": [3, 4],  # Батарейка остаётся доступной
    "goal_pos": [7, 7],
    "spike_pos": [[2, 2], [3, 3]],  # Убраны шипы, мешающие траектории пилы
    "wall_pos": [
        [1, 0], [1, 1], [1, 2], [2, 0], [3, 1], [4, 3], [5, 3], [6, 3], [6, 7]
    ],
    "saw_path": [[4, 4], [5, 4], [6, 4], [6, 5], [6, 6], [5, 6], [4, 6], [4, 5]],  # Квадратная траектория пилы
    "energy": 18  # Энергии достаточно
}
,
    {
    "robot_start": [0, 2],
    "battery_pos": [5, 2],  # Перемещаем батарейку в безопасное место
    "goal_pos": [7, 7],
    "spike_pos": [[3, 6]],  # Убираем шипы с пути пилы
    "wall_pos": [
        [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3]
    ],  # Стена остаётся неизменной
    "saw_path": [[3, 4], [3, 5], [4, 5], [4, 4]],  # Квадратная траектория пилы
    "energy": 15  # Энергии достаточно для прохождения уровня
}

,
    {
    "robot_start": [0, 0],
    "battery_pos": [3, 2],  # Батарейка размещена так, чтобы её нужно было подобрать, избегая пилы
    "goal_pos": [7, 7],
    "spike_pos": [[3, 5], [5, 3]],  # Шипы расположены вдали от основной траектории
    "wall_pos": [
        [2, 3], [2, 4], [2, 5], [2, 6], [6, 3], [6, 4], [6, 5], [6, 6]
    ],  # Стены скорректированы для интересной траектории
    "saw_path": [[4, 4], [4, 5], [5, 5], [5, 4]],  # Траектория пилы остаётся квадратной
    "saw_speed": 2,  # Пила теперь движется медленнее
    "energy": 12  # Энергия уменьшена для усложнения
}
,
   {
    "robot_start": [0, 0],  # Робот стартует в верхнем левом углу
    "battery_pos": [2, 1],  # Батарейка остаётся в доступном месте
    "goal_pos": [6, 5],  # Финиш в нижнем правом углу
    "spike_pos": [],  # Шипы убираем, чтобы пила была главным препятствием
    "wall_pos": [
        [1, 1], [1, 2], [1, 3], [1, 4], [3, 2], [3, 3], [3, 4],
        [5, 2], [5, 3], [5, 4], [6, 2], [6, 4]
    ],  # Стены образуют узкий коридор
    "saw_path": [[4, 3], [4, 2], [4, 1], [3, 1], [2, 1], [2, 2], [2, 3], [3, 3]],  # Пила двигается по сложной траектории
    "saw_speed": 1,  # Пила двигается на нормальной скорости
    "energy": 20  # Энергии достаточно для прохождения
}


]

# Глобальная переменная для максимального уровня
max_level_unlocked = 0

# Добавлены функции для пилы и игры
# Функция для перемещения пилы
def move_saw(saw_path, saw_index, saw_speed):
    if not saw_path:  # Если траектория пустая, пила не двигается
        return saw_index
    if saw_speed <= 1:
        return (saw_index + 1) % len(saw_path)  # Двигается на каждом кадре
    else:
        # Медленная пила движется каждые `saw_speed` кадров
        global_frame = pygame.time.get_ticks() // (100 * saw_speed)
        return global_frame % len(saw_path)




def draw_menu():
    screen.fill(WHITE)
    draw_text("Программируемый робот", BLACK, -100)
    
    # Начальное смещение для уровней
    y_offset = -60  
    for i in range(len(levels)):
        if max_level_unlocked >= i:
            draw_text(f"{i + 1}. Уровень {i + 1}", GREEN, y_offset)
        y_offset += 40  # Увеличиваем отступ между уровнями
    
    # Увеличиваем отступ перед надписью "Нажмите Esc для выхода"
    draw_text("Нажмите Esc для выхода", RED, y_offset + 40)


# Главная функция
def main():
    global max_level_unlocked
    clock = pygame.time.Clock()
    current_level = 0
    game_state = "menu"
    lose_reason = ""
    robot_pos = []
    battery_pos = []
    goal_pos = []
    spike_pos = []
    wall_pos = []
    saw_path = []
    saw_index = 0
    energy = 0

    def start_level(level_index):
        nonlocal robot_pos, battery_pos, goal_pos, spike_pos, wall_pos, saw_path, saw_index, energy, game_state, current_level, lose_reason
        level = levels[level_index]
        robot_pos = level.get("robot_start", [0, 0])[:]
        battery_pos = level.get("battery_pos", [-1, -1])[:]
        goal_pos = level.get("goal_pos", [-1, -1])[:]
        spike_pos = level.get("spike_pos", [])[:]
        wall_pos = level.get("wall_pos", [])[:]
        saw_path = level.get("saw_path", [])[:]
        saw_index = 0
        energy = level.get("energy", 10)
        game_state = "playing"
        current_level = level_index
        lose_reason = ""


    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == "menu":
                if event.type == pygame.KEYDOWN:
                    for i in range(len(levels)):
                        if event.key == pygame.K_1 + i and max_level_unlocked >= i:
                            start_level(i)
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            elif game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    new_pos = robot_pos[:]
                    if event.key == pygame.K_UP:
                        new_pos[1] = max(0, robot_pos[1] - 1)
                    elif event.key == pygame.K_DOWN:
                        new_pos[1] = min(SCREEN_HEIGHT // CELL_SIZE - 1, robot_pos[1] + 1)
                    elif event.key == pygame.K_LEFT:
                        new_pos[0] = max(0, robot_pos[0] - 1)
                    elif event.key == pygame.K_RIGHT:
                        new_pos[0] = min(SCREEN_WIDTH // CELL_SIZE - 1, robot_pos[0] + 1)

                    if new_pos not in wall_pos and new_pos != robot_pos:
                        robot_pos = new_pos
                        energy -= 1

                    if robot_pos in spike_pos:
                        game_state = "lose"
                        lose_reason = "Робот повреждён!"
                        break

            elif game_state in ["win", "lose"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if game_state == "win":
                            if current_level == len(levels) - 1:
                                game_state = "menu"
                            else:
                                start_level(current_level + 1)
                        else:
                            start_level(current_level)
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "menu"

        if game_state == "playing":
            if robot_pos == battery_pos:
                energy += 10
                battery_pos = [-1, -1]
            if robot_pos == goal_pos:
                game_state = "win"
                max_level_unlocked = max(max_level_unlocked, current_level + 1)
            if energy <= 0 and game_state == "playing":
                game_state = "lose"
                lose_reason = "Энергия закончилась!"
    
            # Движение пилы
            saw_index = move_saw(saw_path, saw_index, levels[current_level].get("saw_speed", 1))
    
            # Проверка столкновения с пилой
            if saw_path and robot_pos == saw_path[saw_index]:
                game_state = "lose"
                lose_reason = "Робот попал под пилу!"



        if game_state == "menu":
            draw_menu()

        elif game_state == "playing":
            draw_grid()
            for path in saw_path:
                rect = pygame.Rect(path[0] * CELL_SIZE, path[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, RED, rect)
            screen.blit(robot_img, (robot_pos[0] * CELL_SIZE, robot_pos[1] * CELL_SIZE))
            if battery_pos != [-1, -1]:
                screen.blit(battery_img, (battery_pos[0] * CELL_SIZE, battery_pos[1] * CELL_SIZE))
            screen.blit(goal_img, (goal_pos[0] * CELL_SIZE, goal_pos[1] * CELL_SIZE))
            if saw_path:
                screen.blit(saw_img, (saw_path[saw_index][0] * CELL_SIZE, saw_path[saw_index][1] * CELL_SIZE))
            for spike in spike_pos:
                screen.blit(spike_img, (spike[0] * CELL_SIZE, spike[1] * CELL_SIZE))
            for wall in wall_pos:
                screen.blit(wall_img, (wall[0] * CELL_SIZE, wall[1] * CELL_SIZE))
            draw_text(f"Энергия: {energy}", BLACK, -SCREEN_HEIGHT // 2 + 20)

        elif game_state == "win":
            screen.fill(GREEN)
            draw_text("Вы победили!", WHITE)
            draw_text("Нажмите Enter для продолжения", WHITE, 60)
            draw_text("Нажмите Esc для выхода в меню", WHITE, 120)

        elif game_state == "lose":
            screen.fill(RED)
            draw_text("Вы проиграли!", WHITE)
            draw_text(lose_reason, WHITE, 60)
            draw_text("Нажмите Enter для перезапуска", WHITE, 120)
            draw_text("Нажмите Esc для выхода в меню", WHITE, 180)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()