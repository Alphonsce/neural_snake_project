import numpy
import pygame
from pygame import display


from model import *
from graphics import *
from constans import *
import snake
#from server import *
#from client import *

class Game_field:
    """ Собственно само независимое игровое поле"""
    def __init__(self, x):
        """ При инициализации полю сразу передается координата 
        по которой будет данное поле выводиться на экран
        """
        self.score = 0
        self.snake = Snake(FIELD_SIZE_W // 2, FIELD_SIZE_H // 2, self)
        self.fruit = Fruit(*self.snake.get_pos())
        self.screen = pygame.Surface((WIDTH, HEIGHT - BAR_HEIGHT))
        self.interf = pygame.Surface((WIDTH, BAR_HEIGHT))
        self.x = x

    def update(self):
        """ Обновление состояния поля """
        self.snake.move(self.fruit.get_pos())
        self.screen.fill((0, 0, 0))
        self.screen.blit(draw_field(
            self.screen, *self.snake.get_pos(), 
            self.fruit.get_pos(), self.snake.get_step()
            ), (0, 0))
        if self.snake.alive == False:
            draw_text("Game Over", 50, WIDTH/2, HEIGHT/2 - 100, RED, self.screen)
            draw_text("press ECS", 50, WIDTH/2, HEIGHT/2, RED, self.screen)
        self.interf.fill((90, 90, 90))
        self.interf.blit(draw_interface(self.interf, self.score), (0, 0))

    def new_fruit(self):
        """ Создание нового фрукта для данного поля"""
        self.fruit = Fruit(*self.snake.get_pos())
        self.score += 5

    def snake_down(self):
        """ На данном поле змея получает приказ повернуть вниз"""
        self.snake.direction = Direction.DOWN

    def snake_up(self):
        """ На данном поле змея получает приказ повернуть вверх"""
        self.snake.direction = Direction.UP

    def snake_left(self):
        """ На данном поле змея получает приказ повернуть налево"""
        self.snake.direction = Direction.LEFT

    def snake_right(self):
        """ На данном поле змея получает приказ повернуть направо"""
        self.snake.direction = Direction.RIGHT

class GameVS:
    """ Объект типа игра отвечает за дисплей и циклы игры
    Также отвечает за ввод и распределение гейммодов
    """
    def __init__(self, game):
        """ Создание объекта типа игра"""
        self.clock = pygame.time.Clock()
        self.game = game
        self.display = self.game.display
        self.screen = pygame.Surface((WIDTH, HEIGHT - BAR_HEIGHT))
        self.interf = pygame.Surface((WIDTH, BAR_HEIGHT))
        self.GAME_RUNNING = True

    def start_menu(self):
        """ Стартовое меню отвечает за выбор и распределение игровых модов """
        self.menu = True
        menu_buttons = []
        sliders = []
        sliders.append(Slider(WIDTH / 2, 700, 250, (1, 10, 1)))
        menu_buttons.append(Button("PLAY", WIDTH // 2, 200, 300, 55))
        menu_buttons.append(Button("RUN SERVER",  WIDTH // 2, 300, 300, 55))
        menu_buttons.append(Button("STOP SERVER",  WIDTH // 2, 400, 300, 55))
        menu_buttons.append(Button("FIND SERVER",  WIDTH // 2, 500, 300, 55))
        menu_buttons.append(Button("BACK",  WIDTH // 2 , 600, 300, 55))
        while self.menu:
            x, y = pygame.mouse.get_pos()
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.GAME_RUNNING = False 
                    self.menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        for item in sliders:
                            item.deactivate()
            for item in sliders:
                item.update(x)
                if click:
                    item.check_press(x, y)
                item.draw(self.display)
            for i in range(len(menu_buttons)):
                if menu_buttons[i].check_pressed(x, y) and click:
                    self.menu = False
                    if i == 0:
                        self.mainloop(["gamer"])
                    if 0 < i < 4:
                        self.menu = True
                    if i == 4:
                        self.game.start_menu()
            draw_start_menu(menu_buttons, self.display)
            draw_text("PLAYERS NUMBER", 30, WIDTH / 2, 650, WHITE, self.display)
            pygame.display.flip()

    def mainloop(self, fields: list):
        """ Основной цикл игры.
        На вход подается модель запускаемой игры.
        В fields передается тип игроков
        "gamer" - человек-игрок
        "AI" - искусственный интелект
        """
        self.gamer = None
        self.game_fields = []
        for i in range(len(fields)):
            game_field = Game_field(i * WIDTH)
            self.game_fields.append(game_field)
            if fields[i] == "gamer":
                self.gamer = game_field
        while self.GAME_RUNNING:
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            self.keys_loop()
            for field in self.game_fields:
                field.update()
                self.display.blit(field.screen, (field.x, BAR_HEIGHT))
                self.display.blit(field.interf, (field.x, 0))
                pygame.draw.rect(self.display, (90, 90, 90), [field.x, 0, 0, HEIGHT], 1)
            pygame.display.flip()

    def keys_loop(self):
        """ Контроллер. Отвечает за взаимодействие человека с игрой
        Функция выделена из mainloop для уменьшения длины текста при чтении
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAME_RUNNING = False 
                self.menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    while pause:
                        self.clock.tick(FPS)
                        for eventpause in pygame.event.get():
                            if eventpause.type == pygame.KEYDOWN:
                                if eventpause.key == pygame.K_p:
                                    pause = False
                            if eventpause.type == pygame.QUIT:
                                self.GAME_RUNNING = False 
                                pause = False
                if event.key == pygame.K_ESCAPE:
                    self.start_menu()
                if self.gamer != None:
                    if event.key == pygame.K_UP:
                        self.gamer.snake_up()
                    if event.key == pygame.K_DOWN:
                        self.gamer.snake_down()
                    if event.key == pygame.K_LEFT:
                        self.gamer.snake_left()                        
                    if event.key == pygame.K_RIGHT:
                        self.gamer.snake_right()


"""pygame.init()
GameVS().start_menu()
pygame.quit()"""