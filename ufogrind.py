import sys
import random
import pygame as pg
from params import *
from collections import UserList


class Hero(pg.sprite.Sprite):
    """Игрок"""
    def __init__(self):
        super().__init__()
        self.image = ship
        self.rect = self.image.get_rect()
        self.rect.x = int(WIDTH / 2)
        self.rect.y = HEROFIX
        self.shield = 100
        self.power = 0
        self.lives = 3
        self.radius = int(self.rect.width / 2)
        self.hidden = False
        self.hidden_timer = pg.time.get_ticks()

    def update(self, *args):
        # Сделать видимым, если персонаж не видим:
        if self.hidden and pg.time.get_ticks() - self.hidden_timer > 1000:
            self.hidden = False
            self.rect.x = int(WIDTH / 2)
            self.rect.y = HEROFIX

        left_move, right_move = args
        # Не даём уезжать за левый край:
        if self.rect.x < 0:
            self.rect.x = 0
        # Не даём уезжать за правый край:
        if self.rect.x + self.rect.size[0] > WIDTH:
            self.rect.x = WIDTH - self.rect.size[0]
        # Перемещение влево-вправо:
        if left_move:
            self.rect.x -= 5
        if right_move:
            self.rect.x += 5
        # Ограничиваем максимальное количество боезапасов:
        if self.power > 100:
            self.power = 100

    def shoot(self, shoot_type):
        """Выстрелы разными видами оружия"""
        # Мини-лазер:
        if shoot_type == 'mini-laser':
            mini_laser = MiniLaser(self.rect.size[0], self.rect.size[1], self.rect.x)
            shoot_minilaser.play()
            all_sprites.add(mini_laser)
            minilaser_sprites.add(mini_laser)
        # Ракета:
        elif shoot_type == 'rocket':
            rocket_missile = Rocket(self.rect.size[0], self.rect.size[1], self.rect.x)
            shoot_rocket.play()
            all_sprites.add(rocket_missile)
            rocket_sprites.add(rocket_missile)
        # Мощный лазер:
        elif shoot_type == 'maxi-laser':
            maxi_laser = MaxiLaser(self.rect.size[0], self.rect.size[1], self.rect.x)
            shoot_maxilaser.play()
            all_sprites.add(maxi_laser)
            maxilaser_sprites.add(maxi_laser)
        # Заморозка:
        elif shoot_type == 'freezer':
            frozen = Freeze(self.rect.size[0], self.rect.size[1], self.rect.x)
            shoot_frozen.play()
            all_sprites.add(frozen)
            frozen_sprites.add(frozen)

    def hide(self):
        """Сокрытие корабля игрока за пределы игрового поля"""
        self.hidden = True
        self.hidden_timer = pg.time.get_ticks()
        self.rect.center = (int(WIDTH / 2), HEIGHT + 200)


class MiniLaser(pg.sprite.Sprite):
    """Мини-лазер"""
    def __init__(self, ship_width, ship_height, ship_xcoord):
        super().__init__()
        self.image = minilaser
        self.rect = self.image.get_rect()
        # Начальные координаты:
        self.rect.x = ship_xcoord + int(ship_width / 2) - 5
        self.rect.y = HEROFIX - int(ship_height / 3)
        # Скорость:
        self.speed_y = 10
        self.radius = int((self.rect.size[0] * 0.8) / 2)

    def update(self, *args):
        if self.rect.y < 0:
            self.kill()
        self.rect.y -= self.speed_y


class Rocket(pg.sprite.Sprite):
    """Ракетница"""
    def __init__(self, ship_width, ship_height, ship_xcoord):
        super().__init__()
        self.image = rocket
        self.rect = self.image.get_rect()
        self.rect.x = ship_xcoord + int(ship_width / 3) + 5
        self.rect.y = HEROFIX - int(ship_height / 3)
        self.speed_y = 3

    def update(self, *args):
        if self.rect.y < 0:
            self.kill()
        self.rect.y -= self.speed_y


class Freeze(pg.sprite.Sprite):
    """Ледяная заморозка"""
    def __init__(self, ship_width, ship_height, ship_xcoord):
        super().__init__()
        self.image = freeze
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = ship_xcoord + (ship_width % 2)
        self.rect.y = HEROFIX - int(ship_height / 2)
        self.speed_y = 3
        self.rotate_angle = 0
        self.rotateSpeed = random.randrange(-20, 20)
        self.last_update = pg.time.get_ticks()

    def update(self, *args):
        self.rotate()
        if self.rect.y < 0:
            self.kill()
        self.rect.y -= self.speed_y

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            # Угол поворота:
            self.rotate_angle = (self.rotate_angle + self.rotateSpeed) % 360
            new_img = pg.transform.rotate(self.original_image, self.rotate_angle)
            old_center = self.rect.center
            self.image = new_img
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class MaxiLaser(pg.sprite.Sprite):
    """Макси-лазер"""
    def __init__(self, ship_width, ship_height, ship_xcoord):
        super().__init__()
        self.image = maxilaser
        self.rect = self.image.get_rect()
        # Начальные координаты:
        self.rect.x = ship_xcoord + int(ship_width / 12)
        self.rect.y = HEROFIX - ship_height
        # Скорость:
        self.speed_y = 15
        self.radius = int((self.rect.size[0] * 0.8) / 2)

    def update(self, *args):
        if self.rect.y < 0:
            self.kill()
        self.rect.y -= self.speed_y


class Item(pg.sprite.Sprite):
    """Предмет"""
    def __init__(self, ufo_ship):
        super().__init__()
        self.type = random.choice(['death', 'water', 'killall', 'life', 'shield', 'speed'])
        self.image = items_pics[self.type]
        self.rect = self.image.get_rect()
        self.image.set_colorkey(pg.Color('white'))
        self.rect.center = ufo_ship.rect.center
        self.speed_x = 0
        self.speed_y = 1
        self.radius = int((self.rect.size[0] * 0.8) / 2)

    def update(self, *args):
        if self.rect.y > HEIGHT:
            self.kill()
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x - self.rect.size[0] > WIDTH:
            self.rect.x = WIDTH - self.rect.size[0]
        self.rect.y += self.speed_y


class Ufo(pg.sprite.Sprite):
    """НЛО"""
    def __init__(self):
        super().__init__()
        self.choice = random.choice(ufo_sizes)
        self.image = random.choice(ufo_images[self.choice])
        self.rect = self.image.get_rect()
        # Стартовые координаты:
        self.rect.x = random.randrange(100, WIDTH - self.rect.width - 100)
        self.rect.y = -100
        # Первоначальные векторы скорости:
        self.speed_x = random.randint(-2, 2)
        self.speed_y = random.randint(1, 9)
        self.radius = 20
        pg.draw.circle(self.image, pg.Color('green'), self.rect.center, self.radius)
        self.frozen = False
        self.frozen_time = pg.time.get_ticks()

    def update(self, *args):
        # Если НЛО заморожен:
        if self.frozen:
            if pg.time.get_ticks() - self.frozen_time >= 10000:
                self.frozen = False
        # Если НЛО не заморожен:
        if not self.frozen:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        # Если НЛО улетел за пределы экрана, то перерисовывает его от начала:
        ok1 = self.rect.x + self.rect.size[0] <= 0
        ok2 = self.rect.y - self.rect.size[1] >= HEIGHT
        ok3 = self.rect.x - self.rect.size[0] >= WIDTH
        if ok1 or ok2 or ok3:
            self.rect.x = random.randint(-200, WIDTH - self.rect.width)
            self.rect.y = 0

    def freeze(self):
        """Заморозка НЛО"""
        self.frozen = True
        self.frozen_time = pg.time.get_ticks()


class FireExplosion(pg.sprite.Sprite):
    """Огненный взрыв"""
    def __init__(self, center, choice='small'):
        super().__init__()
        self.choice = choice
        self.image = explosions[self.choice][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pg.time.get_ticks()
        self.frame = 0
        self.frame_rate = 75

    def update(self, *args):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosions[self.choice]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosions[self.choice][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class FrozenExplosion(pg.sprite.Sprite):
    """Ледяной взрыв"""
    def __init__(self, center, choice='small'):
        super().__init__()
        self.choice = choice
        self.image = explose_freeze_anim[self.choice][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pg.time.get_ticks()
        self.frame = 0
        self.frame_rate = 75

    def update(self, *args):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explose_freeze_anim[self.choice]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explose_freeze_anim[self.choice][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def indicators(scr, x, y, value, indicator):
    """Отрисовка индикаторов"""
    if value < 0:
        value = 0
    elif value > 100:
        value = 100
    width, height = 100, 10
    # Обрамление прямоугольника:
    rect_line = pg.Rect(x, y, width, height)
    # Закрашенный прямоугольник:
    rect_fill = pg.Rect(x, y, int(value / 100 * width), height)
    pg.draw.rect(scr, pg.Color('white'), rect_line, 3)

    # Изменение цвета индикатора защиты:
    if indicator == 'shield':
        if value > 60:
            pg.draw.rect(scr, pg.Color('green'), rect_fill)
        elif value > 30:
            pg.draw.rect(scr, pg.Color('yellow'), rect_fill)
        elif value < 30:
            pg.draw.rect(scr, pg.Color('red'), rect_fill)

    # Изменение цвета индикатора боезапасов:
    if indicator == 'ammo':
        if value <= 30:
            pg.draw.rect(scr, (255, 200, 220), rect_fill)
        elif value <= 60:
            pg.draw.rect(scr, (255, 150, 200), rect_fill)
        elif value <= 90:
            pg.draw.rect(scr, (255, 100, 180), rect_fill)
        elif value == 100:
            pg.draw.rect(scr, (255, 0, 130), rect_fill)


def lives(scr, x, y, lvs, picture):
    """Отрисовка количества жизней"""
    for step in range(lvs):
        rect = picture.get_rect()
        rect.x = x + (35 * step)
        rect.y = y
        scr.blit(picture, rect)


def load_hiscore():
    """Загрузка лучшего результата из текстового файла"""
    try:
        with open(os.path.join(GAMEDIR, 'hiscore.txt'), 'r') as f:
            return int(f.read())
    except FileNotFoundError or ValueError:
        return 0


def save_hiscore(hi_scr):
    """Сохранение лучшего результата в текстовом файле"""
    with open(os.path.join(GAMEDIR, 'hiscore.txt'), 'w') as f:
        f.write(str(hi_scr))


def gameover(info_screen):
    """Окончание игры"""
    endstart = pg.image.load(os.path.join(PIC, 'info.jpg'))
    screen.blit(endstart, endstart.get_rect())
    screen.blit(font_level.render(
        f'Лучший результат: {str(highscore)}', True, pg.Color('white')), (440, 555)
    )
    if not info_screen:
        screen.blit(gameOverFont.render('ИГРА ОКОНЧЕНА!', True, pg.Color('yellow')), (330, 485))
    pg.display.update()
    run_gameover = True
    while run_gameover:
        pg.time.Clock().tick(60)
        for evnt in pg.event.get():
            if evnt.type == pg.QUIT:
                save_hiscore(highscore)
                sys.exit()
            if evnt.type == pg.KEYUP:
                if evnt.key == pg.K_SPACE:
                    run_gameover = False
                    # Зацикливаем воспроизведене музыки:
                    pg.mixer.music.play(-1)


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('НЛО-мясорубка')
    screen = pg.display.set_mode(SIZE)
    pg.display.set_icon(pg.image.load(os.path.join(PIC, 'ufo.png')))

    # Фоновая музыка:
    pg.mixer.music.load(os.path.join(SOUND, 'music.ogg'))
    pg.mixer.music.set_volume(0.3)

    # Звуки взрывов:
    explosion_hero = pg.mixer.Sound(os.path.join(EFFECT, 'explosion_hero.wav'))
    explosion_ufo = pg.mixer.Sound(os.path.join(EFFECT, 'explosion_ufo.wav'))
    explosion_ufo.set_volume(0.2)

    # Звуки попадания в противника:
    kick_freeze = pg.mixer.Sound(os.path.join(EFFECT, 'kick_freeze.wav'))
    kick_fire = pg.mixer.Sound(os.path.join(EFFECT, 'kick_fire.wav'))
    kick_fire.set_volume(0.4)

    # Звуки выстрелов:
    shoot_minilaser = pg.mixer.Sound(os.path.join(EFFECT, 'shoot_minilaser.wav'))
    shoot_rocket = pg.mixer.Sound(os.path.join(EFFECT, 'shoot_rocket.wav'))
    shoot_frozen = pg.mixer.Sound(os.path.join(EFFECT, 'shoot_frozen.wav'))
    shoot_maxilaser = pg.mixer.Sound(os.path.join(EFFECT, 'shoot_maxilaser.wav'))

    # Звуки находок:
    item_life = pg.mixer.Sound(os.path.join(EFFECT, 'item_life.wav'))
    item_shield = pg.mixer.Sound(os.path.join(EFFECT, 'item_shield.wav'))
    item_speed = pg.mixer.Sound(os.path.join(EFFECT, 'item_speed.ogg'))
    item_killall = pg.mixer.Sound(os.path.join(EFFECT, 'item_killall.wav'))

    # Звук на окончание игры:
    gameOver_sound = pg.mixer.Sound(os.path.join(SOUND, 'gameover.wav'))

    # Фон космоса:
    background = pg.image.load(os.path.join(PIC, 'back.jpg'))
    # Корабль игрока:
    ship = pg.image.load(os.path.join(PIC, 'hero.png'))
    # Уменьшенная картинка корабля игрока для отображения количества жизней:
    ship_icon = pg.transform.scale(ship, (30, 30))
    # Мини-лазер:
    minilaser = pg.image.load(os.path.join(GUN, 'mini_laser.png'))
    # Ракета:
    rocket = pg.image.load(os.path.join(GUN, 'rocket.png'))
    # Заморозка:
    freeze = pg.image.load(os.path.join(GUN, 'freeze.png'))
    # Макси-лазер:
    maxilaser = pg.image.load(os.path.join(GUN, 'maxi_laser.png'))

    # Инициализация словаря для картинок НЛО
    ufo_images = {
        'size1': list(),
        'size2': list(),
        'size3': list(),
        'size4': list(),
        'size5': list()
    }

    # Генерация НЛО разных размеров:
    ufo_sizes = ['size1', 'size2', 'size3', 'size4', 'size5']
    files = sorted(os.listdir(UFO))
    for file in files:
        pic = pg.image.load(os.path.join(UFO, file))
        ufo_images['size1'].append(pg.transform.scale(pic, (60, 60)))
        ufo_images['size2'].append(pg.transform.scale(pic, (70, 70)))
        ufo_images['size3'].append(pg.transform.scale(pic, (80, 80)))
        ufo_images['size4'].append(pg.transform.scale(pic, (90, 90)))
        ufo_images['size5'].append(pg.transform.scale(pic, (100, 100)))

    # Словарь с анимациями взрывов:
    explosions = {
        'small': list(),
        'large': list(),
        'player': list()
    }

    # Взрывы НЛО:
    files = sorted(os.listdir(EXPLOSION_UFO))
    for file in files:
        pic = pg.image.load(os.path.join(EXPLOSION_UFO, file))
        pic.set_colorkey(pg.Color('white'))
        img_small = pg.transform.scale(pic, (100, 100))
        explosions['small'].append(img_small)
        img_large = pg.transform.scale(pic, (300, 300))
        explosions['large'].append(img_large)

    # Взрыв корабля игрока:
    files = sorted(os.listdir(EXPLOSION_HERO))
    for file in files:
        pic = pg.image.load(os.path.join(EXPLOSION_HERO, file))
        img_rect = pic.get_rect()
        img_small = pg.transform.scale(
            pic,
            (int(img_rect.size[0] / 3) + 10, int(img_rect.size[1] / 3) + 10)
        )
        explosions['player'].append(img_small)

    # Взрыв заморозки:
    explose_freeze_anim = {'small': list(), 'large': list()}
    files = sorted(os.listdir(EXPLOSION_FREEZE))
    for file in files:
        img = pg.image.load(os.path.join(EXPLOSION_FREEZE, file))
        img.set_colorkey(pg.Color('white'))
        img_small = pg.transform.scale(img, (40, 40))
        img_large = pg.transform.scale(img, (300, 300))
        explose_freeze_anim['small'].append(img_small)
        explose_freeze_anim['large'].append(img_large)

    # Словарь с картинками предметов:
    items_pics = {
        'death': pg.image.load(os.path.join(ITEM, 'death.png')),
        'killall': pg.image.load(os.path.join(ITEM, 'killall.png')),
        'water': pg.image.load(os.path.join(ITEM, 'water.png')),
        'life': pg.image.load(os.path.join(ITEM, 'life.png')),
        'speed': pg.image.load(os.path.join(ITEM, 'speed.png')),
        'shield': pg.image.load(os.path.join(ITEM, 'shield.png'))
    }

    # Расположение индикаторов:
    ship_shieldbar_x, ship_shieldbar_y = 5, 5
    ship_powerbar_x, ship_powerbar_y = 5, 20

    # Шрифты:
    font_level = pg.font.SysFont('Trebuchet MS', 20)
    scoreFont = pg.font.SysFont('Trebuchet MS', 20)
    gameOverFont = pg.font.SysFont('Trebuchet MS', 50)

    # Инициализация параметров перед запуском основного цикла:
    running = True
    counter_reset = True
    is_start_screen, game_over = True, True
    score, level = 0, 1
    highscore = load_hiscore()
    item_sprites, frozen_sprites = None, None
    hero, ufo_sprites, all_sprites = None, None, None
    minilaser_sprites, rocket_sprites,  maxilaser_sprites, = None, None, None
    FPS = 60

    # Основной игровой цикл:
    while running:
        if game_over:
            gameover(is_start_screen)
            game_over = False
            hero = Hero()
            # Группы спрайтов:
            all_sprites = pg.sprite.Group()
            all_sprites.add(hero)
            ufo_sprites = pg.sprite.Group()
            minilaser_sprites = pg.sprite.Group()
            rocket_sprites = pg.sprite.Group()
            maxilaser_sprites = pg.sprite.Group()
            item_sprites = pg.sprite.Group()
            frozen_sprites = pg.sprite.Group()

            ufo_number = 20
            for i in range(ufo_number):
                ufo_unit = Ufo()
                all_sprites.add(ufo_unit)
                ufo_sprites.add(ufo_unit)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                save_hiscore(highscore)
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    hero.shoot('mini-laser')
                elif event.key == pg.K_a and hero.power >= 20:
                    hero.shoot('rocket')
                    hero.power -= 20
                elif event.key == pg.K_s and hero.power >= 10:
                    hero.shoot('freezer')
                    hero.power -= 10
                elif event.key == pg.K_d and hero.power >= 15:
                    hero.shoot('maxi-laser')
                    hero.power -= 15

        screen.blit(background, background.get_rect())
        pg.time.Clock().tick(FPS)

        # Количество НЛО:
        number_of_ufo = len(ufo_sprites)

        # Информация о текущей игровой сессии (индикаторы, жизни, очки, уровень):
        indicators(screen, ship_shieldbar_x, ship_shieldbar_y, hero.shield, 'shield')
        indicators(screen, ship_powerbar_x, ship_powerbar_y, hero.power, 'ammo')
        lives(screen, 125, 5, hero.lives, ship_icon)
        text = font_level.render(f'Уровень: {level}', True, pg.Color('white'))
        screen.blit(text, (int(WIDTH - 130), 10))
        score_text = scoreFont.render(f'Очки: {score}', True, pg.Color('white'))
        screen.blit(score_text, (int(WIDTH - 280), 10))

        # Клавиши управления космическим кораблём:
        keys = pg.key.get_pressed()
        left, right = keys[pg.K_LEFT], keys[pg.K_RIGHT]

        # Столкновения:
        is_laser_hit_ufo = pg.sprite.groupcollide(
            minilaser_sprites,
            ufo_sprites,
            True,
            True
        )
        any_ufo_hit_ship = pg.sprite.spritecollide(
            hero,
            ufo_sprites,
            False,
            collided=pg.sprite.collide_circle
        )
        is_rocket_hit_ufo = pg.sprite.groupcollide(
            rocket_sprites,
            ufo_sprites,
            True,
            True
        )
        is_maxilaser_hit_ufo = pg.sprite.groupcollide(
            maxilaser_sprites,
            ufo_sprites,
            False,
            True
        )
        is_item_collected = pg.sprite.spritecollide(
            hero,
            item_sprites,
            False,
            collided=pg.sprite.collide_circle
        )
        is_freezer_hit_ufo = pg.sprite.groupcollide(
            frozen_sprites,
            ufo_sprites,
            True,
            False
        )

        # Обработка столкновений:
        if is_freezer_hit_ufo:
            it = next(is_freezer_hit_ufo.values().__iter__())
            ufo = next(UserList(it).__iter__())
            explose_frozen = FrozenExplosion(ufo.rect.center, 'small')
            all_sprites.add(explose_frozen)
            is_kick_frozen = pg.sprite.spritecollide(explose_frozen, ufo_sprites, False)
            score += 10
            if is_kick_frozen:
                for other_ufo in is_kick_frozen:
                    ufo.freeze()
                    kick_freeze.play()
                    explose_frozen = FrozenExplosion(other_ufo.rect.center, 'small')
                    all_sprites.add(explose_frozen)
                    score += 10
        if is_rocket_hit_ufo:
            it = next(is_rocket_hit_ufo.values().__iter__())
            ufo = next(UserList(it).__iter__())
            explosion_ufo.play()
            explosion = FireExplosion(ufo.rect.center, 'large')
            all_sprites.add(explosion)
            is_explode_hit = pg.sprite.spritecollide(explosion, ufo_sprites, True)
            score += 40
            if is_explode_hit:
                for other_ufo in is_explode_hit:
                    explosion = FireExplosion(other_ufo.rect.center, 'small')
                    explosion_ufo.play()
                    all_sprites.add(explosion)
                    score += 40
        if is_laser_hit_ufo:
            it = next(is_laser_hit_ufo.values().__iter__())
            ufo = next(UserList(it).__iter__())
            hero.power += int((ufo.rect.size[0] + ufo.rect.size[1]) / 7)
            explosion = FireExplosion(ufo.rect.center, 'small')
            explosion_ufo.play()
            all_sprites.add(explosion)
            if random.random() > 0.9:
                item = Item(ufo)
                all_sprites.add(item)
                item_sprites.add(item)
            score += 30
        if is_maxilaser_hit_ufo:
            it = next(is_maxilaser_hit_ufo.values().__iter__())
            ufo = next(UserList(it).__iter__())
            explosion = FireExplosion(ufo.rect.center, 'small')
            explosion_ufo.play()
            all_sprites.add(explosion)
            score += 30
        if is_item_collected:
            for itms in is_item_collected:
                score += 100
                if itms.__dict__['type'] == 'shield':
                    item_shield.play()
                    hero.shield = 100
                if itms.__dict__['type'] == 'killall':
                    for ufo in ufo_sprites:
                        explosion = FireExplosion(
                            ufo.rect.center,
                            random.choice(['small', 'large'])
                        )
                        explosion_ufo.play()
                        all_sprites.add(explosion)
                        ufo.kill()
                if itms.__dict__['type'] == 'water':
                    for ufo in ufo_sprites:
                        explosion = FrozenExplosion(
                            ufo.rect.center,
                            random.choice(['small', 'large'])
                        )
                        kick_freeze.set_volume(0.6)
                        kick_freeze.play()
                        kick_freeze.set_volume(0.4)
                        all_sprites.add(explosion)
                        ufo.freeze()
                if itms.__dict__['type'] == 'life':
                    item_life.play()
                    if hero.lives >= 5:
                        hero.lives = 5
                    else:
                        hero.lives += 1
                itms.kill()
                if itms.__dict__['type'] == 'speed':
                    item_speed.play()
                    low_speed = True
                    for ufo in ufo_sprites:
                        ufo.speed_y = int(ufo.speed_y / 3)
                        if ufo.speed_y == 0:
                            ufo.speed_y = 1
                if itms.__dict__['type'] == 'death':
                    explosion_hero.play()
                    death_explosion = FireExplosion(hero.rect.center, 'small')
                    all_sprites.add(death_explosion)
                    hero.hide()
                    hero.lives -= 1
                    hero.shield = 100
                    score -= 100

        explosion = None
        ending_time = 0
        death_explosion = FireExplosion(hero.rect.center, 'large')
        for ufo in any_ufo_hit_ship:
            hero.shield -= ufo.__dict__['radius'] / 3
            kick_fire.play()
            explosion_hero.play()
            # Если защита игрока закончилась:
            if hero.shield <= 0:
                explosion_hero.play()
                all_sprites.add(death_explosion)
                hero.hide()
                hero.lives -= 1
                hero.shield = 100
        if hero.lives == 0 and not death_explosion.alive():
            if score > highscore:
                highscore = score
            score = 0
            game_over = True
            pg.mixer.music.stop()
            gameOver_sound.play()
            is_start_screen = False
        if number_of_ufo == 0:
            if counter_reset:
                ending_time = pg.time.get_ticks()
                counter_reset = False
            if pg.time.get_ticks() - ending_time > 3000:
                counter_reset = True
                level += 1
                for i in range(level * 5):
                    ufo = Ufo()
                    all_sprites.add(ufo)
                    ufo_sprites.add(ufo)
        all_sprites.draw(screen)
        all_sprites.update(left, right)
        pg.display.update()
    pg.quit()
