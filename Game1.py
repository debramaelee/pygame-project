import pygame
import random
import math

times_fatter = 1
food_counter = 0
width = 512
height = 512
blue_color = (97, 159, 182)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Super Fireball Chicken Revenge')
pygame.key.set_repeat(400, 20)

class Hero(object):
    def __init__(self):
        self.x_dir = 5
        self.y_dir = 5
        self.x = 250
        self.y = 250
        self.mapX_pos = 250
        self.health = 12
        self.food_counter = 0
        self.hero_alive = True
        self.hero_image = \
        pygame.image.load('images/brown_chicken.png').convert_alpha()
        self.hero_image = pygame.transform.scale(self.hero_image, \
        (48 + times_fatter, 48 + times_fatter))
        self.dead_image = \
        pygame.image.load('images/game_over.png').convert_alpha()

class Predator(object):
    def __init__(self):
        self.x = 255
        self.y = 240
        self.x_dir = 10
        self.y_dir = 10
        self.alive = True

        self.predator_image = \
        pygame.image.load('images/wolf.gif').convert_alpha()
        self.predator_image = pygame.transform.scale(self.predator_image, (100,100))

class Fireball(object):
    def __init__(self):
        self.fireball_image = \
        pygame.image.load('images/fireball.png').convert_alpha()
        self.x = 0
        self.y = 0

class Food(object):
    def __init__(self):
        self.x = random.randint(10, 670)
        self.y = random.randint(5, 377)
        self.x_dir = 5
        self.y_dir = 5
        self.alive = True
        self.food_image = \
        pygame.image.load('images/banana.gif').convert_alpha()

class Map(object):
    def __init__(self):
        self.mapZ = 'images/map1.bmp'

    def changeMap(self, map_image):
        self.mapZ = map_image

    def getMap(self):
        return self.mapZ

class Boss(object):
    def __init__(self):
        self.health = 50
        self.x = 330
        self.y = 150
        self.x_dir = 0
        self.y_dir = 10
        self.alive = False
        self.boss_image = \
        pygame.image.load('images/farmer1.png').convert_alpha()

def main():
    global times_fatter, food_counter
    #screen stuff
    hero = Hero()
    food = Food()
    boss = Boss()
    predator = Predator()
    map = Map()
    clock = pygame.time.Clock()
    #sound stuff
    pygame.mixer.init()
    background_music = pygame.mixer.music.load('sounds/game_tune.mp3')
    die_sound = pygame.mixer.Sound('sounds/die.flac')
    eat_sound = pygame.mixer.Sound('sounds/heal_sound.wav')
    game_over = pygame.mixer.Sound('sounds/game_over.wav')
    pygame.mixer.music.play(10)
    # Game initialization
    change_dir_countdown = 120
    fireball_countdown = 120
    pygame.init()

    #font stuff
    font = pygame.font.SysFont('tahoma', 38)

    stop_game = False

    #game loop

    while not stop_game:
        screen.fill(blue_color)
        background_image = \
        pygame.image.load(map.getMap()).convert_alpha()
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == 273:
                    hero.x_dir = 0
                    hero.y_dir = -10
                    hero.x += hero.x_dir
                    hero.y += hero.y_dir
                elif event.key == 274:
                    hero.x_dir = 0
                    hero.y_dir = 10
                    hero.x += hero.x_dir
                    hero.y += hero.y_dir
                elif event.key == 276:
                    hero.x_dir = -10
                    hero.y_dir = 0
                    hero.x += hero.x_dir
                    hero.y += hero.y_dir
                    hero.mapX_pos -= 10
                elif event.key == 275:
                    hero.x_dir = 10
                    hero.y_dir = 0
                    hero.x += hero.x_dir
                    hero.y += hero.y_dir
                    if not hero.mapX_pos + 1 > 3072:
                        hero.mapX_pos += 10
#fireball
                elif event.key == 32:
                    fireball = Fireball()
                    fireball.x = hero.x + 40
                    fireball.y = hero.y + 100

# GOING OFF SCREEEN
            if hero.mapX_pos > 512 and hero.mapX_pos <= 1024:
                boss.alive = False
                map.changeMap('images/map2.bmp')
            elif hero.mapX_pos > 1025 and hero.mapX_pos <= 1536:
                boss.alive = False
                map.changeMap('images/map3.bmp')
            elif hero.mapX_pos > 1537 and hero.mapX_pos <= 2048:
                boss.alive = False
                map.changeMap('images/map4.bmp')

            elif hero.mapX_pos > 2049 and hero.mapX_pos <= 2560:
                boss.alive = True
                map.changeMap('images/map5.bmp')

            elif hero.mapX_pos <= 512:
                boss.alive = False
                map.changeMap('images/map1.bmp')

#hero wrap around
            if hero.x > width and not hero.mapX_pos >= 3072:
                hero.x = 20
                predator.x = random.randint(20, 490)
                predator.y = random.randint(20, 490)

                food.alive = True
                food.x = random.randint(25, 450)
                food.y = random.randint(25, 450)

            elif hero.mapX_pos > 2500:
                hero.x = 460
#hero wraps back around on sides but not top
        if hero.x < 0:
            hero.x = 512
        if hero.y < 10:
            hero.y = 10
        if hero.y > 400:
            hero.y = 400

        if hero.health <= 0:
            hero.hero_alive = False
            # die_sound.play()
            screen.blit(hero.dead_image, (0, 0))


        if boss.health <= 0:
            boss.alive = False

        if predator.alive == True:
            fireball_countdown -= 1
            if fireball_countdown == 0:
                fireball_countdown = 10
            try:
                fireball.x += 10
            except Exception:
                pass

            change_dir_countdown -= 1
            if change_dir_countdown == 0:
                change_dir_countdown = 10

                z = random.randint(0,7)
                if z == 0:
                    predator.x_dir = 0
                    predator.y_dir = -5
                if z == 1:
                    predator.x_dir = 0
                    predator.y_dir = 5
                if z == 2:
                    predator.x_dir = 5
                    predator.y_dir = 0
                if z == 3:
                    predator.x_dir = -5
                    predator.y_dir = 0
                if z == 4:
                    predator.x_dir = 5
                    predator.y_dir = 5
                if z == 5:
                    predator.x_dir = -5
                    predator.y_dir = 5
                if z == 6:
                    predator.x_dir = 5
                    predator.y_dir = -5
                if z == 7:
                    predator.x_dir = -5
                    predator.y_dir = -5

            predator.x += predator.x_dir
            predator.y += predator.y_dir

            if predator.x > 490:
                predator.x = 490
            if predator.x < 15:
                predator.x = 15
            if predator.y > 390:
                predator.y = 390
            if predator.y < 15:
                predator.y = 15

            if math.sqrt(math.pow((predator.x - hero.x), 2)
            + math.pow((predator.y - hero.y), 2)) < 40:
                hero.health -= 1
                game_over.play()
            try:
                if math.sqrt(math.pow((boss.x - fireball.x), 2)
                + math.pow((boss.y - fireball.y), 2)) < 40:
                    boss.health -= 1
            except Exception:
                pass

            if math.sqrt(math.pow((food.x - hero.x), 2)
            + math.pow((food.y - hero.y), 2)) < 40 and food.alive == True:
                eat_sound.play()
                food.alive = False
                hero.health += 5
                times_fatter += 12
                hero.food_counter += 1


        status_menu_text = "Chicken Health: " + str(hero.health) + "   Boss Health: " + str(boss.health)
        # title_text = "Chicken Health: " + str(hero.health) + "   Boss Health: " + str(boss.health)
        text = font.render(status_menu_text, 1, (255, 255, 255))
        # text
        screen.blit(text, (35, 10))

# Draw characters
        # Game display
        try:
            fireball.y = hero.y
            screen. blit(fireball.fireball_image, (fireball.x, fireball.y + 5))
        except Exception:
            pass

        if food.alive == True:
            screen.blit(food.food_image, (food.x, food.y))
        if hero.hero_alive == True:

            screen.blit(pygame.transform.scale(hero.hero_image, \
        (48 + times_fatter, 48 + times_fatter)), (hero.x, hero.y))

        screen.blit(predator.predator_image, (predator.x, predator.y))
        if boss.alive == True:
            screen.blit(boss.boss_image, (boss.x, boss.y))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
