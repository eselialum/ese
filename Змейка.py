import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы игры
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# Цвета
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """
        Инициализация игрового объекта.

        Args:
            position: позиция объекта на игровом поле
            body_color: цвет объекта (RGB кортеж)
        """
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Абстрактный метод для отрисовки объекта.

        Args:
            surface: поверхность для отрисовки
        """
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        # Генерируем случайные координаты в пределах игрового поля
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """
        Отрисовывает яблоко на поверхности.

        Args:
            surface: поверхность для отрисовки
        """
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]  # Список позиций сегментов
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            # Проверяем, что змейка не пытается двигаться в обратном направлении
            opposite_directions = {
                UP: DOWN,
                DOWN: UP,
                LEFT: RIGHT,
                RIGHT: LEFT
            }
            if self.next_direction != opposite_directions.get(self.direction):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        # Вычисляем новую позицию головы с учетом прохождения через границы
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Вставляем новую голову в начало списка
        self.positions.insert(0, new_head)

        # Если длина змейки не увеличилась, удаляем хвост
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """
        Отрисовывает змейку на поверхности.

        Args:
            surface: поверхность для отрисовки
        """
        for position in self.positions:
            rect = pygame.Rect(
                position[0],
                position[1],
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для изменения направления движения змейки.

    Args:
        snake: объект змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры."""
    # Инициализация экрана
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Изгиб Питона")
    clock = pygame.time.Clock()

    # Создание игровых объектов
    snake = Snake()
    apple = Apple()

    # Основной игровой цикл
    while True:
        # Обработка событий
        handle_keys(snake)

        # Обновление направления змейки
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

            # Проверяем, что яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Проверка столкновения змейки с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()

        # Отрисовка
        screen.fill(BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        # Отображение счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {snake.length - 1}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Обновление экрана
        pygame.display.update()

        # Ограничение FPS (здесь управляется скорость игры)
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    
