import pygame
# Палитра основных цветов ----------------------------------------------------------------------------------------------
class color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
# ----------------------------------------------------------------------------------------------------------------------
# Базовый шаблон -------------------------------------------------------------------------------------------------------
class GameBase:
    ########################################
    # Инициализация
    def __init__(self, WIDTH=500, HEIGHT=500, BACKGROUND=color.BLACK) -> None:
        self.width = WIDTH
        self.height = HEIGHT
        self.background = BACKGROUND
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.__clock__ = pygame.time.Clock()
        self.__existence__ = False
        self.__display__ = pygame.display
        pygame.display.set_caption('This is game!')
    ########################################
    # Метод для запуска
    def run(self, FPS=60) -> None:
        self.screen = self.__display__.set_mode((self.width, self.height))
        self.__existence__ = True
        while self.__existence__:
            self.__clock__.tick(FPS)
            self.__execute_events__()
            self.__render__()
            pygame.display.update()
    ########################################
    # Закрытие приложения
    def __close__(self) -> None:
        self.__existence__ = False
    ########################################
    # Проверка ивентов
    def __execute_events__(self) -> None:
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                self.__close__()
    ########################################
    # Отрисовка примитивов
    def __render__(self) -> None:
        pass
# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    test = GameBase(300, 300)
    test.run()