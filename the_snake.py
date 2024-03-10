from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
S_BAR_WIDTH = 640
S_BAR_HEIGHT = 80
WINDOW_WIDTH = SCREEN_WIDTH
WINDOW_HEIGHT = SCREEN_HEIGHT + S_BAR_HEIGHT

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет текста.
FONT_COLOR = (255, 215, 0)

# Скорость движения змейки:
speed = 20
MIN_SPEED = 5
MAX_SPEED = 50
SPEED_STEP = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настраиваем шрифт надписей.
font = pygame.font.Font(None, 48)

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """GameObject Общий класс для игровых объектов."""

    def __init__(self, position=SCREEN_CENTER,
                 body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заглушка, метод будет определен в потомках."""
        raise NotImplementedError(f'Определите Draw {type(self).__name__}')


class Apple(GameObject):
    """Apple Создает объект Яблоко."""

    def randomize_position(self, object):
        """Устанавливаем случайные координаты."""
        # Проверяем есть ли хотя бы одна свободная клетка.
        if object.length < (GRID_HEIGHT * GRID_WIDTH):
            new_pos = get_rnd_pos()
        else:
            object.reset()
        # Если новая позиция занята змейкой, запрашиваем новые координаты.
        if new_pos in object.positions:
            self.randomize_position(object)
        return new_pos

    def draw(self, surface):
        """Выводим на игровое поле."""
        draw_rect(surface, self.position, self.body_color)


class Snake(GameObject):
    """Snake Создает объект Змейка."""

    def __init__(self, position=SCREEN_CENTER,
                 body_color=SNAKE_COLOR):
        self.positions = [position]
        self.length = 1
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        super().__init__(position, body_color)

    def update_direction(self):
        """Обновляет направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface):
        """Выводит на игровое поле."""
        draw_rect(surface, self.positions[0], self.body_color)
        # # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает координаты головы."""
        return self.positions[0]

    def move(self):
        """Основная функция перемещения."""
        d_x, d_y = self.direction
        updated_head_pos = ((self.get_head_position()[0] + d_x * GRID_SIZE) %
                            SCREEN_WIDTH,
                            (self.get_head_position()[1] + d_y * GRID_SIZE) %
                            SCREEN_HEIGHT
                            )
        # Смещаем голову на новую ячейку.
        self.positions.insert(0, updated_head_pos)
        # Если длина змейки не увеличилась удаляем последний элемент.
        if self.length < len(self.positions):
            self.last = self.positions.pop()
        self.draw(screen)

    def reset(self):
        """Сбрасываем змейку и начинаем игру заново."""
        self.length = 1
        self.positions = [self.position]
        # Метод спорный, но такая конструкция выглядит лучше чем 4 if.
        self.direction = globals()[choice(('UP',
                                           'DOWN',
                                           'LEFT',
                                           'RIGHT'
                                           ))]
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            # Добавим регулировку скорости игры
            elif event.key == pygame.K_PAGEDOWN and speed > MIN_SPEED:
                globals()['speed'] -= SPEED_STEP
            elif event.key == pygame.K_PAGEUP and speed < MAX_SPEED:
                globals()['speed'] += SPEED_STEP


def get_rnd_pos():
    """Возвращает случайные координаты на игровом поле."""
    # Избегаем прорисовки квадрата за пределами поля.
    return (randint(1, GRID_WIDTH) * GRID_SIZE - GRID_SIZE,
            randint(1, GRID_HEIGHT) * GRID_SIZE - GRID_SIZE
            )


def draw_rect(surface, position, color):
    """Рисуем квадрат"""
    rect = pygame.Rect((position[0], position[1]),
                       (GRID_SIZE, GRID_SIZE)
                       )
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def draw_s_bar(surface):
    """Рисуем рамку экрана"""
    rect = pygame.Rect(0, SCREEN_HEIGHT, S_BAR_WIDTH, S_BAR_HEIGHT)
    pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)
    pygame.draw.rect(surface, BORDER_COLOR, rect,3)


def main():
    """Создаем классы, и логику игры."""
    # Тут нужно создать экземпляры классов.
    snake = Snake(SCREEN_CENTER,
                  SNAKE_COLOR
                  )
    apple = Apple(get_rnd_pos(),
                  APPLE_COLOR
                  )

    while True:
        clock.tick(speed)
        draw_s_bar(screen)
        text = font.render(f'Длина змейки: {snake.length}. '
                           f'Скорость игры: {speed // 5}.',
                           True,
                           FONT_COLOR
                           )
        screen.blit(text, (15, SCREEN_HEIGHT + 10))
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw(screen)
        # Проверяем на столкновение головы с телом змейки.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        # Проверяем съели ли яблоко.
        if snake.get_head_position() == apple.position:
            apple.position = apple.randomize_position(snake)
            snake.length += 1
        pygame.display.update()


if __name__ == '__main__':
    main()
