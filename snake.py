import numpy
import pygame

from model import *
from graphics import *
from constans import *
from agent import Learning_Agent as agent

class Game_field:
    """ Собственно само независимое игровое поле"""
    def __init__(self, x, rule=1):
        """ При инициализации полю сразу передается координата 
        по которой будет данное поле выводиться на экран
        """
        self.walls = []
        if rule == 1: 
            self.rule = Snake.standart_rule
        elif rule == 2: 
            self.rule = Snake.inf_field
        elif rule == 3:
            self.rule = Snake.walls
            self.walls = []
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
        self.screen.blit(draw_field(self.screen, self), (0, 0))
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

class AI_Game_field(Game_field):
    def __init__(self, x, ai_dificalty):
        path_to_the_file_for_model='./model/learned_model.pth'
        #path_to_the_file_for_model=f'./model/learned_model{ai_dificalty}.pth'
        super().__init__(x)
        self.agent = agent()
        self.agent.model.load(path_to_the_file_for_model) 

    def direction_from_action(self, action=[0, 1, 0]):
        '''
        метод позволяет исходя из action получить direction движения змейки,
        action при этом предсказывается нейронной сетью
        
        '''
        directions_order = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        current_direction_order = directions_order.index(self.snake.direction)
        new_direction_order = current_direction_order + 0
        if np.array_equal(action, [0, 1, 0]):
            new_direction_order = current_direction_order
        elif np.array_equal(action, [0, 0, 1]):
            new_direction_order = (current_direction_order + 1) % 4
        else:       # если None остается пока agent.get_action() не сделан, то будет влево крутить
            new_direction_order = (current_direction_order - 1) % 4

        self.snake.direction = directions_order[new_direction_order]   

    def update(self):
        old_state = self.agent.get_state(self)
        move = self.agent.get_action(old_state)
        self.direction_from_action(move)

        return super().update()

    def will_be_dead(self, point):
        '''функция, которая показывает по переданной ей координате точки,
        будет ли игра проиграна, если этой точкой будет голова
        '''
        x, y = point

        # смерть об стены:
        if x >= FIELD_SIZE_W or y >= FIELD_SIZE_H:
            return True
        # смерть об хвост:
        if (x, y) in self.snake.tail:
            return True
        return False

class Game:
    """ Объект типа игра отвечает за дисплей и циклы игры
    Также отвечает за ввод и распределение гейммодов
    """
    def __init__(self):
        """ Создание объекта типа игра"""
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.GAME_RUNNING = True
        self.back = False
        self.ai_dificalty = 1

    def start_menu(self):
        """ Стартовое меню отвечает за выбор и распределение игровых модов """
        pygame.display.quit()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        menu_buttons = []
        menu_buttons.append(Button("Player only", WIDTH // 2, 300, 250, 55, self.Player_menu, ()))
        menu_buttons.append(Button("AI mod",  WIDTH // 2, 400, 250, 55, self.Ai_menu, ()))
        menu_buttons.append(Button("PvP",  WIDTH // 2, 500, 250, 55, self.wait, ()))
        menu_buttons.append(Button("Settings",  WIDTH // 2, 600, 250, 55, self.wait, ()))
        menu_buttons.append(Button("EXIT",  WIDTH // 2 , 700, 250, 55, self.quit_game, ()))
        while self.GAME_RUNNING:
            x, y = pygame.mouse.get_pos()
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            self.keys_menu()
            for item in menu_buttons:
                if item.check_pressed(x, y) and self.click:
                    item.func(*item.args)
            draw_start_menu(menu_buttons, [], self.display)
            pygame.display.flip()

    def Ai_menu(self):
        """ Меню AI отвечает за выбор модов из этого раздела"""
        menu_buttons = []
        menu_buttons.append(Button("AI only",  WIDTH // 2, 300, 250, 55, self.mainloop, (["AI"],)))
        menu_buttons.append(Button("AI VS Player",  WIDTH // 2, 400, 250, 55, self.mainloop, (["AI", "gamer"],)))
        menu_buttons.append(Button("Learning",  WIDTH // 2 , 500, 250, 55, self.wait, ()))
        menu_buttons.append(Button("BACK",  WIDTH // 2 , 600, 250, 55, self.go_back, ()))
        sliders = []
        sliders.append(Slider(WIDTH / 2, 700, 250, (1, 5, 1)))
        while self.GAME_RUNNING and not self.back:
            x, y = pygame.mouse.get_pos()
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            self.keys_menu()
            for item in menu_buttons:
                if item.check_pressed(x, y) and self.click:
                    item.func(*item.args)
            for item in sliders:
                item.update(x)
                if self.click:
                    item.check_press(x, y)
                if self.unclick:
                    item.deactivate()
            draw_start_menu(menu_buttons, sliders, self.display)
            draw_text("Dificalty", 30, WIDTH / 2, 640, WHITE, self.display)
            pygame.display.flip()
        self.back = False

    def Player_menu(self):
        """ Меню Player отвечает за выбор модов из этого раздела"""
        menu_buttons = []
        sliders = []
        menu_buttons.append(Button("Standart",  WIDTH // 2, 300, 250, 55, self.mainloop, (["gamer"], 1)))
        menu_buttons.append(Button("Infinity",  WIDTH // 2, 400, 250, 55, self.mainloop, (["gamer"], 2)))
        menu_buttons.append(Button("Walls",  WIDTH // 2 , 500, 250, 55, self.mainloop, (["gamer"], 3)))
        menu_buttons.append(Button("BACK",  WIDTH // 2 , 600, 250, 55, self.go_back, ()))
        while self.GAME_RUNNING and not self.back:
            x, y = pygame.mouse.get_pos()
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            self.keys_menu()
            for item in menu_buttons:
                if item.check_pressed(x, y) and self.click:
                    item.func(*item.args)
            draw_start_menu(menu_buttons, sliders, self.display)
            pygame.display.flip()
        self.back = False

    def mainloop(self, fields: list, rule=1):
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
            if fields[i] == "gamer":
                game_field = Game_field(i * WIDTH, rule)
                self.gamer = game_field
            if fields[i] == "AI":
                game_field = AI_Game_field(i * WIDTH, self.ai_dificalty)
            self.game_fields.append(game_field)
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

    def quit_game(self):
        self.GAME_RUNNING = False 
    
    def wait(self):
        pass

    def go_back(self):
        self.back = True

def main():
    Game().start_menu()

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()