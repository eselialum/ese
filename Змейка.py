"""Змейка."""
from random import choice, randint



import pygame

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
SPEED = 8

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс для управления игровыми объектами (родительский)."""

    def __init__(self):
        """Инициализация атрибутов этого класса."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw():
        """Пока пустой метод рисовки объектов."""
        pass


class Apple(GameObject):
    """Класс яблока (дочерний)."""

    def __init__(self):
        """Инициализация атрибутов этого класса."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = None
        self.randomize_position()

    def randomize_position(self):
        """Метод генерирования случайных координат змейки."""
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                         randint(0, GRID_HEIGHT) * GRID_SIZE)

    def draw(self):
        """Метод рисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, (255, 0, 0), rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки (дочерний)."""

    def __init__(self):
        """Инициализация атрибутов этого класса."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод обновления направления змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод движения змейки."""
        head = Snake.get_head_position(self)
        first_coordinate = self.direction[0] * GRID_SIZE
        second_coordinate = self.direction[1] * GRID_SIZE
        snake_ = (first_coordinate, second_coordinate)
        new_head = (head[0] + snake_[0], head[1] + snake_[1])
        if new_head in self.positions[2:]:
            Snake.reset(self)
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions[-1]
                self.positions.pop()
            count = 0
            for element in self.positions:
                massive = list(element)
                if massive[0] >= SCREEN_WIDTH:
                    massive[0] = 0
                elif massive[0] < 0:
                    massive[0] = SCREEN_WIDTH
                elif massive[1] >= SCREEN_HEIGHT:
                    massive[1] = 0
                elif massive[1] < 0:
                    massive[1] = SCREEN_HEIGHT
                snake_head = tuple(massive)
                for index in range(len(self.positions)):
                    if index == count:
                        self.positions[index] = snake_head
                count += 1

    def draw(self):
        """Метод рисвоания змейки."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод получения головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сброса змейки."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция для обработки события клавиш."""
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
    """Основная функция игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw()
        snake.draw()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position()
        pygame.display.update()
        # Тут опишите основную логику игры.
        # ...


if __name__ == '__main__':
    main()


# Метод draw класса Apple


# # Метод draw класса Snake


# Функция обработки действий пользователя

# Метод обновления направления после нажатия на кнопку
