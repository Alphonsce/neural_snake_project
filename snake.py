import numpy
import pygame
from pygame import display


from model import *
from graphics import *
from constans import *
import snakeVS


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

class Game:
    """ Объект типа игра отвечает за дисплей и циклы игры
    Также отвечает за ввод и распределение гейммодов
    """
    def __init__(self):
        """ Создание объекта типа игра"""
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.GAME_RUNNING = True

    def start_menu(self):
        """ Стартовое меню отвечает за выбор и распределение игровых модов """
        pygame.display.quit()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.menu = True
        menu_buttons = []
        menu_buttons.append(Button("Player only", WIDTH // 2, 300, 250, 55))
        menu_buttons.append(Button("PVP", WIDTH // 2, 400, 250, 55))
        menu_buttons.append(Button("AI only",  WIDTH // 2, 500, 250, 55))
        menu_buttons.append(Button("AI vs Player",  WIDTH // 2, 600, 250, 55))
        menu_buttons.append(Button("EXIT",  WIDTH // 2 , 700, 250, 55))
        while self.menu:
            x, y = pygame.mouse.get_pos()
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            click = self.keys_menu()
            for i in range(len(menu_buttons)):
                if menu_buttons[i].check_pressed(x, y) and click:
                    self.menu = False
                    if i == 0:
                        self.mainloop(["gamer"])
                    if i == 1:
                        self.VS_mod()
                    if i == 2:
                        self.mainloop(["AI"])
                    if i == 3:
                        self.mainloop(["AI", "gamer"])
                    if i == 4:
                        self.quit_game()
            draw_start_menu(menu_buttons, self.display)
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
        pygame.display.quit()
        self.display = pygame.display.set_mode((len(fields) * WIDTH, HEIGHT))
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
                self.quit_game()
                #self.menu = False
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

    def keys_menu(self):
        """ Контроллер для стартового меню. """
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
                self.menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        return click

    def VS_mod(self):
        snakeVS.GameVS(self).start_menu()

    def quit_game(self):
        self.GAME_RUNNING = False


def main():
    Game().start_menu()

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()