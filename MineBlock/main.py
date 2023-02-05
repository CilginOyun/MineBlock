from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
from perlin_noise import PerlinNoise
import random
import pymunk
import time

block_pick = 1

app = Ursina()

stone_texture = load_texture('textures/stone.png')
brick_texture = load_texture('textures/brick.png')
grass_texture = load_texture('textures/grass.png')
wood_texture = load_texture('textures/wood.png')
dirt_texture = load_texture('textures/dirt.png')
place_sound = Audio('sounds/place.wav', loop=False, autoplay=False)
break_sound = Audio('sounds/punch.aiff', loop=False, autoplay=False)

z = 1
x = 1
y = 1
ydirt = 1

while True:
    z = z + 1
    x = x + 1

    time.sleep(0.1)

    if z and x == 12:
        print(x, z)
        break

while True:
    y = y + 1
    time.sleep(0.1)
    if y == 3:
        break

while True:
    ydirt = ydirt + 1
    time.sleep(0.1)
    if ydirt == 3:
        break

class Brick(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='blocks/block.obj',
            origin_y=.5,
            texture=brick_texture,
            color=color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color=color.lime,
            scale=0.5,
            shader=basic_lighting_shader,
            collider="box",
        )

class Bedrock(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='blocks/block.obj',
            origin_y=.5,
            texture=brick_texture,
            color=color.gray,
            highlight_color=color.lime,
            scale=0.5,
            shader=basic_lighting_shader,
            collider="box",
        )

class Stone(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='blocks/block.obj',
            origin_y=.5,
            texture=stone_texture,
            color=color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color=color.lime,
            scale=0.5,
            shader=basic_lighting_shader,
            collider='box',
        )


class Grass(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='blocks/block.obj',
            origin_y=.5,
            texture=grass_texture,
            color=color.white,
            highlight_color=color.lime,
            scale=0.5,
            shader=basic_lighting_shader,
            collider="box",
        )


class Wood(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='blocks/block.obj',
            origin_y=.5,
            texture=wood_texture,
            color=color.white,
            highlight_color=color.lime,
            scale=0.5,
            shader=basic_lighting_shader,
            collider="box",
        )


class Dirt(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='blocks/block.obj',
            origin_y=.5,
            texture=dirt_texture,
            color=color.white,
            highlight_color=color.lime,
            scale=0.5,
            shader=basic_lighting_shader,
            collider="box",
        )


def update():
    global block_pick
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4
    if held_keys['5']: block_pick = 5


def remove_voxel(brick):
    global Brick
    brick.enabled = False
    del brick


def remove_stone(stone):
    global Stone
    stone.enabled = False
    del stone


def remove_grass(grass):
    global Grass
    grass.enabled = False
    del grass


def remove_dirt(dirt):
    global Dirt
    dirt.enabled = False
    del dirt


def remove_wood(wood):
    global Wood
    wood.enabled = False
    del wood


def input(key):
    if key == 'right mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            place_sound.play()
            if block_pick == 1: Grass(position=hit_info.entity.position + hit_info.normal)
            if block_pick == 2: Stone(position=hit_info.entity.position + hit_info.normal)
            if block_pick == 3: Brick(position=hit_info.entity.position + hit_info.normal)
            if block_pick == 4: Dirt(position=hit_info.entity.position + hit_info.normal)
            if block_pick == 5: Wood(position=hit_info.entity.position + hit_info.normal)
    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            if hit_info.entity.__class__.__name__ == 'Grass':
                break_sound.play()
                remove_voxel(hit_info.entity)
            if hit_info.entity.__class__.__name__ == 'Stone':
                break_sound.play()
                remove_stone(hit_info.entity)
            if hit_info.entity.__class__.__name__ == 'Brick':
                break_sound.play()
                remove_voxel(hit_info.entity)
            if hit_info.entity.__class__.__name__ == 'Dirt':
                break_sound.play()
                remove_dirt(hit_info.entity)
            if hit_info.entity.__class__.__name__ == 'Wood':
                break_sound.play()
                remove_wood(hit_info.entity)

for ztime in range(z):
    for xtime in range(x):
            grass = Grass(position=(xtime,0,ztime))

for ystonetime in range(y):
    for xstonetime in range(x):
        for zstonetime in range(z):
            stone = Dirt(position=(xstonetime, -ystonetime - 1, zstonetime))
            stone.position_y = -2

for ydirttime in range(ydirt):
    for xdirttime in range(x):
        for zdirttime in range(z):
            stone = Stone(position=(xdirttime, -ydirttime - 4, zdirttime))
            stone.position_y = -2

for bedrockxtime in range(x):
     for bedrockztime in range(z):
        stone = Bedrock(position=(bedrockxtime, 0 - 7, bedrockztime))
        stone.position_y = -2

sky = Sky()

player = FirstPersonController()
app.run()
