import pygame as pg

pg.init()
tile_width = tile_height = 30


def size(filename):
    filename = "C:/Users/1/PycharmProjects/летняя практика/1 неделя/5. ПТ\B. Ящики/level_levels/" + filename
    with open(filename, 'r') as level:
        level_map = [line.strip() for line in level]
    width = max(map(len, level_map))
    height = len(level_map)
    return width * tile_width, height * tile_height


screen = pg.display.set_mode(size('map.txt'))
player_image = pg.transform.scale(pg.image.load('C:/Users/1/PycharmProjects/летняя практика/1 неделя/5. ПТ/B. Ящики/level_assets/player.gif').convert_alpha(), (tile_width, tile_height))
player_image_rotate = pg.transform.flip(player_image, True, False)


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.tile_type = tile_type
        self.rect.x = tile_width * pos_x
        self.rect.y = tile_height * pos_y
        tiles_group.add(self)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y
        self.direction = "up"
        player_group.add(self)

    def update(self, to_x, to_y, direction):
        if self.rect.x + to_x != size('map.txt')[0] and self.rect.x + to_x != -tile_width\
                and self.rect.y + to_y != size('map.txt')[1] and self.rect.y + to_y != -tile_height:
            self.rect.x += to_x
            self.rect.y += to_y
            self.direction = direction

            for wall in tiles_group:
                if wall.tile_type == 'wall':
                    if self.rect.colliderect(wall.rect):
                        self.rect.x -= to_x
                        self.rect.y -= to_y

    def attack(self):
        to_x = to_y = 0
        if self.direction == 'right':
            to_x = tile_width
        elif self.direction == 'left':
            to_x = -tile_width
        elif self.direction == 'up':
            to_y = -tile_height
        elif self.direction == 'down':
            to_y = tile_height

        self.rect.x += to_x
        self.rect.y += to_y

        for wall in tiles_group:
            if wall.tile_type == 'wall':
                if self.rect.colliderect(wall.rect):
                    wall.image = tile_images['empty']
                    wall.tile_type = "empty"
                    self.rect.x -= to_x
                    self.rect.y -= to_y
                    return
        self.rect.x -= to_x
        self.rect.y -= to_y


all_sprites = pg.sprite.Group()
tiles_group = pg.sprite.Group()
player_group = pg.sprite.Group()

tile_images = {
    'wall': pg.transform.scale(pg.image.load('C:/Users/1/PycharmProjects/летняя практика/1 неделя/5. ПТ\B. Ящики/level_assets/box.png'), (tile_width, tile_height)),
    'empty': pg.transform.scale(pg.image.load('C:/Users/1/PycharmProjects/летняя практика/1 неделя/5. ПТ\B. Ящики/level_assets/floor.png'), (tile_width, tile_height))
}
player, level_x, level_y = generate_level(load_level('C:/Users/1/PycharmProjects/летняя практика/1 неделя/5. ПТ\B. Ящики/level_levels/map.txt'))

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player.update(-tile_width, 0, 'left')
                player.image = player_image_rotate
            elif event.key == pg.K_RIGHT:
                player.update(tile_width, 0, 'right')
                player.image = player_image
            elif event.key == pg.K_UP:
                player.update(0, -tile_height, 'up')
            elif event.key == pg.K_DOWN:
                player.update(0, tile_height, 'down')
            elif event.key == pg.K_SPACE:
                player.attack()

    tiles_group.draw(screen)
    player_group.draw(screen)
    pg.display.flip()

pg.quit()