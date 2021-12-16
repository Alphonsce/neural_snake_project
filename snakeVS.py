
import pygame




from graphics import *
from constans import *
from server import *
from client import *
from graphicsVS import *

class GameVS:
    """ Объект типа онлайн игра отвечает за дисплей и циклы игры
    Также отвечает за ввод и распределение гейммодов
    """
    def __init__(self, game):
        """ Создание объекта типа игра
        game - игра типа Game из файла snake
        """
        self.clock = pygame.time.Clock()
        self.game = game
        self.display = self.game.display
        self.screen = pygame.Surface((2000, 2000))
        self.interf = pygame.Surface((WIDTH, BAR_HEIGHT))
        self.GAME_RUNNING = True
        self.back = False
        self.client = None
        self.server = None
        self.players = 1
        self.gamers = 0
        self.VS_mod = True
        self.snake = Direction.RIGHT

    def start_menu(self):
        """ Стартовое меню отвечает за запуск и остановку сервера
        корректировку количества игроков. Поиск сервера для игры
         """
        self.menu = True
        menu_buttons = []
        sliders = []
        sliders.append(Slider(WIDTH / 2, 700, 250, (1, 10, 1)))
        menu_buttons.append(Button("RUN SERVER",  WIDTH // 2, 300, 300, 55, self.run_server, ()))
        menu_buttons.append(Button("STOP SERVER",  WIDTH // 2, 400, 300, 55, self.stop_server, ()))
        menu_buttons.append(Button("FIND SERVER",  WIDTH // 2, 500, 300, 55, self.find_server, ()))
        menu_buttons.append(Button("BACK",  WIDTH // 2 , 600, 300, 55, self.go_back, ()))
        while self.GAME_RUNNING and self.VS_mod:
            x, y = pygame.mouse.get_pos()
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            draw_start_menu(menu_buttons, sliders, self.display)
            draw_text("Number of players", 30, WIDTH // 2, 640, WHITE, self.display)
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
            if self.client != None:
                self.client.update()
            self.run_game()
            pygame.display.flip()
        self.back = False
        return self.GAME_RUNNING

    def mainloop(self):
        """ Основной цикл игры.
        """
        while self.GAME_RUNNING and self.VS_mod:
            #if self.client.check_server_fall():
            if self.client != None:
                self.clock.tick(FPS)
                self.screen.fill((0, 0, 0))
                try:
                    draw_field_VSmod(self.screen, self.client)
                    step = self.client.snakes[0][0]
                    (x_0, y_0) = tuple(self.client.snakes[0][1])
                    (x, y) = tuple(self.client.snakes[0][2][-1])
                    x_0 += step / FRAMES_PER_STEP * (x_0 - x)
                    y_0 += step / FRAMES_PER_STEP * (y_0 - y)
                    self.display.blit(self.screen, (
                        -CELL_SIDE * (x_0) + WIDTH / 2,
                        - (y_0)* CELL_SIDE + (HEIGHT - BAR_HEIGHT) / 2)
                        )
                except:
                    print(self.client.snakes)
                pygame.display.flip()
            if self.server != None:
                self.server.update()
            self.client.update()
            self.keys_loop()

    def keys_loop(self):
        """ Контроллер. Отвечает за взаимодействие человека с игрой
        Функция выделена из mainloop для уменьшения длины текста при чтении
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAME_RUNNING = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.go_back()
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
        """Пустая функция ожидания"""
        pass

    def go_back(self):
        """Возврат в основную игру"""
        self.stop_server()
        if self.client != None:
            self.client.quit_game()
            self.client = None
        self.VS_mod = False

    def run_server(self):
        """Запуск сервера"""
        if self.server == None:
            self.server = Server(self.players)
            print("start")

    def stop_server(self):
        """Остановка сервера"""
        if self.server != None:
            self.server.stop()
            self.server = None
            print("stop")

    def find_server(self):
        """Начало поиска сервера"""
        if self.client == None:
            self.client = Client(self)
            print("searching")

    def stop_client(self):
        """Остановка клиента"""
        if self.client != None:
            self.client.stop()
            self.client = None
            self.go_back()

    def run_game(self):
        """Запуск игрового поля"""
        if self.client != None:
            if self.client.game_started:
                self.mainloop()

    def quit_game(self):
        """ Выход из игры"""
        self.server.stop()
        self.GAME_RUNNING = False

if __name__ == "__main__":
    print("This is not a main module")