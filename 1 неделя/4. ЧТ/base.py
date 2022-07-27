import pygame
from PyQt6.QtWidgets import QMainWindow
# Палитра основных цветов ----------------------------------------------------------------------------------------------
class colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
# ----------------------------------------------------------------------------------------------------------------------

# Шаблон для всех игр --------------------------------------------------------------------------------------------------
class Game:
    ########################################
    # Инициализация
    def __init__(self, WIDTH: int, HEIGHT: int, BACKGROUND=colors.BLACK) -> None:
        self.width = WIDTH
        self.height = HEIGHT
        self.background = BACKGROUND
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.__clock__ = pygame.time.Clock()
        self.__existence__ = False
        pygame.display.set_caption("This is game")
    ########################################
    # Метод для запуска
    def run(self, FPS=60) -> None:
        self.__existence__ = True
        while self.__existence__:
            self.__clock__.tick(FPS)
            self.screen.fill(self.background)
            self.__execute_events__()
            self.__render__()
            pygame.display.update()

    ########################################
    # Внутренние методы

        ########################################
        ## Закрытие приложения
    def __close__(self) -> None:
        self.__existence__ = False

        ########################################
        ## Проверка ивентов
    def __execute_events__(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__close__()

        ########################################
        ## Отрисовка примитивов
    def __render__(self) -> None:
        pass

        ########################################
    ########################################
# ----------------------------------------------------------------------------------------------------------------------