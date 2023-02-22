from random import choice, randint
from sys import exit
from time import time

try:
    import keyboard
except ImportError:
    print('The "keyboard" package needs to be installed for user input.')
    exit(1)

# Matrix size
MATRIX_W = 16
MATRIX_H = 16

# Frame rate settings
FPS = 8
T = 1 / FPS

# Game settings
MOUSE_EVERY_NO_POINTS = 10  # How often a mouse appears
MOUSE_DURATION = 15  # For how many frames the mouse stays
MOUSE_REWARD = 3
FOOD_REWARD = 1

# Colors
SNAKE = (73, 255, 106)  # Green-to-teal-ish
SNAKE_DEAD = (255, 255, 0)  # Yellow-to-red-ish
MOUSE = (112, 128, 144)  # Grey-to-blue-ish
FOOD = (210, 120, 17)  # Orange

# Where to display
MATRIX = True
SCREEN = False

if MATRIX:
    from led_matrix import update_matrix

if SCREEN:
    try:
        import pygame
    except ImportError:
        print('The "pygame" package needs to be installed for rendering to screen.')
        exit(1)

    PIXEL_SIZE = 30
    SCREEN_W = MATRIX_W * PIXEL_SIZE
    SCREEN_H = MATRIX_H * PIXEL_SIZE

    # Set up the screen
    pygame.init()
    pygame.display.set_caption(f"Snake {MATRIX_W}x{MATRIX_H}")
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    def update_screen(data):
        screen.fill((0, 0, 0))
        data = data[1::2]  # Strip pixel enumeration
        pixel_index = 0
        # Draw line by line
        for y in range(MATRIX_H):
            for x in range(MATRIX_W):
                pixel = tuple(int(data[pixel_index][i : i + 2], 16) for i in (0, 2, 4))
                pygame.draw.rect(
                    screen,
                    pixel,
                    (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
                )
                pixel_index += 1
        pygame.display.update()


class Snake:
    def __init__(self):
        self.X = randint(0, MATRIX_W - 1)
        self.Y = randint(0, MATRIX_H - 1)
        self.body = [
            [self.X, self.Y],
            [self.X + 1, self.Y],
        ]
        self.last_node = None
        self.direction = choice(["right", "left", "up", "down"])
        self.color = SNAKE

    def move(self, key_input):
        if key_input is not None and {key_input, self.direction} not in [
            {"left", "right"},  # Can't turn left if going right (and vice versa)
            {"up", "down"},
        ]:
            self.direction = key_input

        if self.direction == "left":
            self.X = self.X - 1 if self.X - 1 >= 0 else MATRIX_W - 1
        elif self.direction == "right":
            self.X = self.X + 1 if self.X + 1 < MATRIX_W else 0
        elif self.direction == "up":
            self.Y = self.Y - 1 if self.Y - 1 >= 0 else MATRIX_H - 1
        elif self.direction == "down":
            self.Y = self.Y + 1 if self.Y + 1 < MATRIX_H else 0

        self.body.insert(0, [self.X, self.Y])
        self.last_node = self.body.pop()

    def grow(self):
        self.body.append(self.last_node)

    def die(self):
        self.color = SNAKE_DEAD

    def render(self, frame):
        head = 1
        color_fade = 40
        for node in self.body:
            if head:
                frame[node[1]][node[0]] = self.color
                head = 0
            else:
                frame[node[1]][node[0]] = [
                    self.color[0],
                    max(0, self.color[1] - color_fade),
                    self.color[2],
                ]
                color_fade += 4


class Food:
    def __init__(self):
        self.X = randint(0, MATRIX_W - 1)
        self.Y = randint(0, MATRIX_H - 1)
        self.color = FOOD

    def render(self, frame):
        frame[self.Y][self.X] = self.color


class Mouse:
    def __init__(self):
        self.X = randint(0, MATRIX_W - 2)  # Mouse is 2 pixels wide
        self.Y = randint(0, MATRIX_H - 1)
        self.body = [
            [self.X, self.Y],
            [self.X + 1, self.Y],
        ]
        self.frames_alive = 0
        self.color = MOUSE

    def render(self, frame):
        for node in self.body:
            frame[node[1]][node[0]] = self.color


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.mouse = None
        self.score = 0
        self.key_input = None

    def read_key_input(self):
        if keyboard.is_pressed("esc"):
            self.key_input = "esc"
        elif keyboard.is_pressed("left"):
            self.key_input = "left"
        elif keyboard.is_pressed("right"):
            self.key_input = "right"
        elif keyboard.is_pressed("up"):
            self.key_input = "up"
        elif keyboard.is_pressed("down"):
            self.key_input = "down"

    def update_frame(self):
        # Move the snake first
        self.snake.move(self.key_input)

        # Logic of interactions between game objects
        # Snake hits itself
        if [self.snake.X, self.snake.Y] in self.snake.body[1:]:
            self.game_over()

        # Snake eats food
        if [self.snake.X, self.snake.Y] == [self.food.X, self.food.Y]:
            self.score += FOOD_REWARD
            print(f"\nFood! +1 point! Current score: {self.score}")
            self.snake.grow()

            # Food spawning
            while [self.food.X, self.food.Y] in self.snake.body:
                del self.food
                self.food = Food()

            # Mouse spawning
            if self.mouse is None and self.score % MOUSE_EVERY_NO_POINTS == 0:
                self.mouse = Mouse()
                while any(node in self.mouse.body for node in self.snake.body):
                    del self.mouse
                    self.mouse = Mouse()

        # Mouse logic
        if self.mouse is not None:
            self.mouse.frames_alive += 1

            # Snake eats a mouse
            if [self.snake.X, self.snake.Y] in self.mouse.body:
                self.score += MOUSE_REWARD
                print(f"\nMouse! +3 points! Current score: {self.score}")
                del self.mouse
                self.mouse = None
                self.snake.grow()

            # Mouse runs away
            elif self.mouse.frames_alive >= MOUSE_DURATION:
                del self.mouse
                self.mouse = None

    def render_frame(self):
        # Prepare empty frame line by line
        current_frame = list(
            list([0, 0, 0] for _ in range(MATRIX_W)) for _ in range(MATRIX_H)
        )

        # Render game objects into the frame
        self.snake.render(current_frame)
        self.food.render(current_frame)
        if self.mouse is not None:
            self.mouse.render(current_frame)

        # Convert the frame into pixel data
        data = []
        pixel_index = 0
        for line in current_frame:
            for pixel in line:
                data.append(pixel_index)
                data.append(f"{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}")
                pixel_index += 1

        # Display frame
        if SCREEN:
            update_screen(data)
        if MATRIX:
            update_matrix(data)

    def game_over(self):
        self.snake.die()
        self.render_frame()
        print(f"\nGame over! Final score: {self.score}")
        exit(0)

    def run(self):
        print("New game, good luck!")
        next_frame = T
        while self.key_input != "esc":
            # Keyboard input
            self.read_key_input()

            # Frame rendering
            now = time()
            if now >= next_frame:
                self.update_frame()
                self.render_frame()
                next_frame = now + T
        self.game_over()


# Init and run game
Game().run()
