from ursina import * # $pip install ursina
import random
from ursina.shaders import lit_with_shadows_shader

app = Ursina()
foodCount = []
EnemyCount = []
HealthBlock = []
score = 0
score_text = Text(text=f'Score: {score}', position=(-0.4, 0.44), color=color.dark_text, scale=2.5)


def change_texture():
    for i in EnemyCount:
        i.texture = 'assets/food.png'


def reload():
    application.hot_reloader.reload_code()


def play():
    player.disable()

    def start():
        player.enable()
        PlayButton.disable()

    PlayButton = Button(icon='assets/play.png', scale=0.3, position=(0, 0), color=color.white10)
    PlayButton.on_click = start


class Enemy(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'sphere'
        self.collider = 'sphere'
        self.parent = board
        self.position = (random.uniform(-0.47, 0.47), 2.5, random.uniform(-0.47, 0.47))
        self.texture = 'assets/food.png'
        self.scale = 0.05
        self.scale_y = 5

    def update(self):
        self.rotation_y += 1


class Food(Entity):
    def __init__(self):
        super().__init__()
        self.parent = board
        self.model = 'sphere'
        self.scale = 0.05
        self.scale_y = 5
        self.texture = 'assets/food.png'
        self.collider = 'sphere'
        self.position = (random.uniform(-0.47, 0.47), 2.5, random.uniform(-0.47, 0.47))
        self.shader = lit_with_shadows_shader

    def update(self):
        self.rotation_y += 1


class HealthBar(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'quad'
        self.texture = 'assets/health.png'
        self.scale = 0.1
        self.position = (0.02, 0.5)
        self.parent = camera.ui

    def update(self):
        try:
            for i in HealthBlock[player.health:]:
                destroy(i)
        except:
            pass


class GameOver(Entity):
    def __init__(self):
        super().__init__()
        self.parent = camera.ui
        self.model = 'quad'
        self.texture = 'assets/over.png'
        self.scale = 0

    def update(self):
        if self.scale_x < 1.5 and self.scale_y < 1:
            self.scale_x += 0.01
            self.scale_y += 0.01


class Snake(Entity):
    def __init__(self):
        super().__init__()
        self.parent = board
        self.scale = 0.05
        self.scale_y = 5
        self.model = 'sphere'
        self.collider = 'sphere'
        self.position = (0, 2.5, 0)
        self.dx = 0
        self.dz = 0
        self.speed = 0.3
        self.texture = 'assets/head.png'
        self.body = []
        self.shader = lit_with_shadows_shader
        self.health = 3
        self.EnemyEaten = 0

    def update(self):
        global score
        self.x += self.dx * time.dt
        self.z += self.dz * time.dt
        if self.health <= 0:
            for i in player.body:
                i.disable()
            player.disable()
            for i in EnemyCount:
                i.fade_out()
            GameOver()
            Reload = Button(icon='assets/replay.png', scale=0.3, position=(-0.5, -0.06), color=color.white10)
            Reload.on_click = reload
        if self.x > 0.47:
            self.x = -self.x + 0.01
        if self.z > 0.47:
            self.z = -self.z + 0.01
        if self.z < -0.47:
            self.z = -self.z - 0.01
        if self.x < -0.47:
            self.x = -self.x - 0.01

        for i in foodCount:
            if self.intersects(i).hit:
                Audio('eat.mp3')
                i.position = (random.uniform(-0.47, 0.47), 2.5, random.uniform(-0.47, 0.47))
                a = Entity(model='sphere',
                           texture='assets/body.png',
                           scale=0.04,
                           scale_y=4,
                           parent=board,
                           collider='sphere',
                           position=(0, 2.5, 0),
                           shader=lit_with_shadows_shader
                           )
                self.body.append(a)
                score += 1
                score_text.text = f"Score: {score}"
                self.speed += 0.001
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].position = self.body[i - 1].position
        if len(self.body) > 0:
            self.body[0].position = self.position
        for i in EnemyCount:
            if self.intersects(i).hit:
                Audio('assets/eat.mp3')
                i.texture = 'assets/enemy_red.png'
                invoke(change_texture, delay=1)
                self.EnemyEaten += 1
                if self.EnemyEaten > 1:
                    self.health -= 1
                i.position = (random.uniform(-0.47, 0.47), 2.5, random.uniform(-0.47, 0.47))

    def input(self, key):
        if key == 'right arrow':
            self.dx = self.speed
            self.dz = 0
            self.rotation_y = -50
        if key == 'left arrow':
            self.dx = -self.speed
            self.dz = 0
            self.rotation_y = 120
        if key == 'up arrow':
            self.dx = 0
            self.dz = self.speed
            self.rotation_y = -150
        if key == 'down arrow':
            self.dx = 0
            self.dz = -self.speed
            self.rotation_y = 30


board = Entity(model='cube', scale=10, texture='assets/sand.jpg', scale_y=0.1, shader=lit_with_shadows_shader)

DirectionalLight(y=2.5, z=2, rotation=(45, -45, 45))

Sky(texture='assets/sky.png')
camera.position = (0, 12, -15)
camera.rotation = (39, 0, 0)
player = Snake()
for i in range(3):
    food = Food()
    foodCount.append(food)
for i in range(1):
    enemy = Enemy()
    EnemyCount.append(enemy)
offset = 0.02
for i in range(player.health):
    healthB = HealthBar()
    healthB.position = (offset, 0.42)
    offset += 0.09
    HealthBlock.append(healthB)
for i in range(20):
    a = Entity(model='sphere',
               texture='assets/body.png',
               scale=0.04,
               scale_y=4,
               parent=board,
               collider='sphere',
               position=(0, 2.5, 0),
               shader=lit_with_shadows_shader
               )
    player.body.append(a)
play()
app.run()
