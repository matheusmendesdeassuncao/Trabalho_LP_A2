import pygame

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)

class Player:
    def __init__(self, x: int, y: int, image, width: int = 64, height: int = 64):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.vel_y = 0
        self.gravity = 0.5
        self.is_jumping = False
        self.is_alive = True
        self.speed = 5
        self.direction = pygame.Vector2(0, 0)

    def jump(self):
        if not self.is_jumping:
            self.vel_y = -15
            self.is_jumping = True

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

    def horizontal_movement_collision(self, obstacles):
        self.rect.x += self.direction.x * self.speed
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if self.direction.x < 0:
                    self.rect.left = obstacle.rect.right
                elif self.direction.x > 0:
                    self.rect.right = obstacle.rect.left

    def vertical_movement_collision(self, obstacles):
        self.apply_gravity()
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if self.vel_y > 0:
                    self.rect.bottom = obstacle.rect.top
                    self.is_jumping = False
                    self.vel_y = 0
                elif self.vel_y < 0:
                    self.rect.top = obstacle.rect.bottom
                    self.vel_y = 0

    def move(self, dx, obstacles):
        self.direction.x = dx
        self.horizontal_movement_collision(obstacles)

    def update(self, obstacles):
        if self.is_alive:
            self.vertical_movement_collision(obstacles)

    def draw(self, screen: pygame.Surface):
        if self.is_alive:
            screen.blit(self.image, self.rect.topleft)

    def check_death(self, level, player_name):
        if 0 <= self.rect.y // 32 < len(level) and 0 <= self.rect.x // 32 < len(level[0]):
            tile = level[self.rect.y // 32][self.rect.x // 32]
            if tile == "T":
                return True  # T mata ambos os personagens
            elif tile == "U" and player_name == "alexandre_de_morais":
                return True  # U mata apenas Alexandre de Morais
            elif tile == "V" and player_name == "peixonalta":
                return True  # V mata apenas Peixonalta
        return False
