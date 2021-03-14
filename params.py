"""
Программные параметры
"""

import os


# Пути:
GAMEDIR = os.path.dirname(__file__)
PIC = os.path.join(GAMEDIR, 'pic')
SOUND = os.path.join(GAMEDIR, 'sound')
SPRITE = os.path.join(GAMEDIR, 'sprite')
GUN = os.path.join(PIC, 'guns')
ITEM = os.path.join(PIC, 'items')
UFO = os.path.join(PIC, 'ufos')
EXPLOSION_UFO = os.path.join(SPRITE, 'explosion_ufo')
EXPLOSION_HERO = os.path.join(SPRITE, 'explosion_hero')
EXPLOSION_FREEZE = os.path.join(SPRITE, 'explosion_freeze')
EFFECT = os.path.join(SOUND, 'effects')

# Размер игрового окна:
SIZE = WIDTH, HEIGHT = 800, 800

# Фиксированная координата игрока:
HEROFIX = HEIGHT - 90
