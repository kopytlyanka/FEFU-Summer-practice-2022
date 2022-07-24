class BaseObject:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def get_coordinates(self) -> list:
        return [self.x, self.y, self.z]
class Block(BaseObject):
    def shatter(self) -> None:
        self.x = None
        self.y = None
        self.z = None
class Entity(BaseObject):
    def move(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
class Thing(BaseObject):
    pass

if __name__ == '__main__':
    pass