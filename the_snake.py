from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """GameObject Общий класс для игровых объектов."""

    position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def __init__(self):
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Заглушка, метод будет определен в потомках."""
        pass


class Apple(GameObject):
    """Apple Создает объект Яблоко."""

    def __init__(self):
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR
        self.draw(screen)

    def randomize_position(self):
        """Устанавливаем случайные координаты."""
        return (randint(0, GRID_WIDTH) * GRID_SIZE,
                randint(0, GRID_HEIGHT) * GRID_SIZE
                )

    def draw(self, surface):
        """Выводим на игровое поле."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Snake Создает объект Змейка."""

    def __init__(self):
        self.positions = [(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2)]
        self.length = 1
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.draw(screen)

    def update_direction(self):
        """Обновляет направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface):
        """Выводит на игровое поле."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
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
        updated_head_pos = (self.get_head_position()[0] + d_x * GRID_SIZE,
                            self.get_head_position()[1] + d_y * GRID_SIZE
                            )
        # Проверяем на столкновение с границей игрового поля.
        if updated_head_pos[0] < 0:
            updated_head_pos = (SCREEN_WIDTH - GRID_SIZE, updated_head_pos[1])
        if updated_head_pos[0] >= SCREEN_WIDTH:
            updated_head_pos = (GRID_SIZE, updated_head_pos[1])
        if updated_head_pos[1] < 0:
            updated_head_pos = (updated_head_pos[0], SCREEN_HEIGHT - GRID_SIZE)
        if updated_head_pos[1] >= SCREEN_HEIGHT:
            updated_head_pos = (updated_head_pos[0], GRID_SIZE)
        # Смещаем голову на новую ячейку.
        self.positions.insert(0, updated_head_pos)
        # Если длина змейки не увеличилась удаляем последний элемент.
        if self.length < len(self.positions):
            self.last = self.positions.pop()
        # Проверяем на столкновение.
        if updated_head_pos in self.positions[1:]:
            self.reset()

    def reset(self):
        """Сбрасываем змейку и начинаем игру заново."""
        self.length = 1
        self.positions = super().position
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


def main():
    """Создаем классы, и логику игры."""
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw(screen)
        apple.draw(screen)
        if snake.get_head_position() == apple.position:
            apple = Apple()
            snake.length += 1
        pygame.display.update()


if __name__ == '__main__':
    main()
