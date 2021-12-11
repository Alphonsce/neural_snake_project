import numpy
import pygame
from pygame import display


from model import *
from graphics import *
from constans import *
import snake
from server import *
from client import *

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
        self.back = False
        self.client = None
        self.server = None
        self.players = 1
        self.gamers = 0
        self.searching = False
        self.VS_mod = True

    def start_menu(self):
        """ Стартовое меню отвечает за выбор и распределение игровых модов """
        self.menu = True
        menu_buttons = []
        sliders = []
        sliders.append(Slider(WIDTH / 2, 700, 250, (1, 10, 1)))
        menu_buttons.append(Button("PLAY", WIDTH // 2, 200, 300, 55, self.wait, ()))
        menu_buttons.append(Button("RUN SERVER",  WIDTH // 2, 300, 300, 55, self.wait, ()))
        menu_buttons.append(Button("STOP SERVER",  WIDTH // 2, 400, 300, 55, self.wait, ()))
        menu_buttons.append(Button("FIND SERVER",  WIDTH // 2, 500, 300, 55, self.wait, ()))
        menu_buttons.append(Button("BACK",  WIDTH // 2 , 600, 300, 55, self.go_back, ()))
        while self.GAME_RUNNING and self.VS_mod:
            x, y = pygame.mouse.get_pos()
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            self.keys_menu()
            for item in menu_buttons:
                if item.check_pressed(x, y) and self.click:
                    item.func(*item.args)
            for item in sliders:
                item.update(x)
                self.players = item.pos
                if self.click:
                    item.check_press(x, y)
                if self.unclick:
                    item.deactivate()
            if self.server != None:
                self.server.update()
            draw_start_menu(menu_buttons, sliders, self.display)
            draw_text("Number of players", 30, WIDTH // 2, 640, WHITE, self.display)
            pygame.display.flip()
        self.back = False
        return self.GAME_RUNNING

    def mainloop(self):
        """ Основной цикл игры.
        """
        while self.GAME_RUNNING and self.VS_mod:
            """if self.client.check_server_fall():
                
            if self.server != None:
                self.server.update()
            """
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            self.keys_loop()
            #draw_field_VSmod(self.display, self)
            pygame.display.flip()

    def keys_loop(self):
        """ Контроллер. Отвечает за взаимодействие человека с игрой
        Функция выделена из mainloop для уменьшения длины текста при чтении
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAME_RUNNING = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.start_menu()
                if event.key == pygame.K_UP:
                    self.snake = Direction.UP
                if event.key == pygame.K_DOWN:
                    self.snake = Direction.DOWN
                if event.key == pygame.K_LEFT:
                    self.snake = Direction.LEFT                    
                if event.key == pygame.K_RIGHT:
                    self.snake = Direction.RIGHT

    def keys_menu(self):
        """ Контроллер для стартового меню. """
        self.click = False
        self.unclick = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAME_RUNNING = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.unclick = True
    
    def wait(self):
        pass

    def go_back(self):
        self.VS_mod = False

    def run_server(self):
        self.server = Server(self.players)

    def stop_server(self):
        self.server.stop()
        self.server = None

    def find_server(self):
        self.client = Client()
        self.searching = True

    def run_game(self):
        if self.players == self.gamers:
            self.mainloop()

    def quit_game(self):
        # delete #self.server.stop()
        self.GAME_RUNNING = False

if __name__ == "__main__":
    print("This is not a main module")