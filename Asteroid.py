'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''


#Gregory Clarke
#Advanced Computer Programming
#Version 1.0
#3/15/2019


from pygame.locals import *
import pygame
import random

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    x = 0
    y = 10
    speed = 10

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("ts4.png").convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        self.rect.y = pos[1]

        if self.rect.y > 470:
            self.rect.y = 470

    def shoot(self):
        soundObj = pygame.mixer.Sound('pew_pew.wav')
        soundObj.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([25, 5])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x += 25


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("Asteroid3.png").convert_alpha()

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x -= 8

class Health(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("heart3.png").convert_alpha()

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x -= 8


class App:
    windowWidth = 960
    windowHeight = 600

    player = 0
    laser = 0
    asteroid = 0

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Asteroid')
        self._running = True
        self.bg = pygame.image.load("space_wow.jpg").convert_alpha()
        self.clock = pygame.time.Clock()

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        pygame.mixer.music.load('Power Bots Loop.wav')
        pygame.mixer.music.play(-1, 0.0)
        if self.on_init() == False:
            self._running = False

        lives = 3
        fontObj2 = pygame.font.Font('freesansbold.ttf', 32)
        textSurfaceObj2 = fontObj2.render("Lives= " + str(lives), True, WHITE, BLACK)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (250, 570)

        if lives <= 0:
            self.running = False

        score = 0
        fontObj = pygame.font.Font('freesansbold.ttf', 32)
        textSurfaceObj = fontObj.render("Score= " + str(score), True, WHITE, BLACK)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (650, 570)

        self.player = Player()

        bullet_list = pygame.sprite.Group()
        all_sprites_list = pygame.sprite.Group()
        block_list = pygame.sprite.Group()
        heart_list = pygame.sprite.Group()
        all_sprites_list.add(self.player)
        show = True

        chance = 20
        chance2 = 1000
        if show == True:

            while self._running:
                if score >= 10000 and score < 12000:
                    chance = 5

                if score >= 12000 and score < 20000:
                    chance = 15

                if score >= 20000 and score < 22000:
                    chance = 5

                if score >= 22000:
                    chance = 10

                chance_to_spawn = random.randint(1, chance)

                if chance_to_spawn == 1:
                    asteroid = Asteroid()
                    asteroid.rect.x = 1100
                    asteroid.rect.y = random.randint(0, 450)

                    # Add the block to the list of objects
                    block_list.add(asteroid)
                    all_sprites_list.add(asteroid)

                chance_to_spawn2 = random.randint(1, chance2)

                if chance_to_spawn2 == 1:
                    heart = Health()
                    heart.rect.x = 1100
                    heart.rect.y = random.randint(0, 450)

                    heart_list.add(heart)
                    all_sprites_list.add(heart)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        self.player.shoot()
                        bullet = Bullet()

                        bullet.rect.x = self.player.rect.x + 65
                        bullet.rect.y = self.player.rect.y + 32

                        all_sprites_list.add(bullet)
                        bullet_list.add(bullet)

                for item in bullet_list:

                    for y in block_list:

                        block_hit_list = pygame.sprite.spritecollide(item, block_list, True)

                        for block in block_hit_list:
                            bullet_list.remove(item)
                            block_list.remove(item)
                            all_sprites_list.remove(item)
                            score += 100
                            fontObj = pygame.font.Font('freesansbold.ttf', 32)
                            textSurfaceObj = fontObj.render("Score= " + str(score), True, WHITE, BLACK)
                            textRectObj = textSurfaceObj.get_rect()
                            textRectObj.center = (650, 570)
                            soundObj = pygame.mixer.Sound('Explosion+1.wav')
                            soundObj.play()

                for item in bullet_list:

                    for y in heart_list:

                        block_hit_list2 = pygame.sprite.spritecollide(item, heart_list, True)

                        for block in block_hit_list2:
                            bullet_list.remove(item)
                            heart_list.remove(item)
                            all_sprites_list.remove(item)
                            score += 100
                            lives += 1
                            fontObj = pygame.font.Font('freesansbold.ttf', 32)
                            textSurfaceObj = fontObj.render("Score= " + str(score), True, WHITE, BLACK)
                            textRectObj = textSurfaceObj.get_rect()
                            textRectObj.center = (650, 570)
                            fontObj2 = pygame.font.Font('freesansbold.ttf', 32)
                            textSurfaceObj2 = fontObj2.render("Lives= " + str(lives), True, WHITE, BLACK)
                            textRectObj2 = textSurfaceObj2.get_rect()
                            textRectObj2.center = (250, 570)

                for bullet in bullet_list:

                    if bullet.rect.x > 1100:
                        bullet_list.remove(bullet)
                        all_sprites_list.remove(bullet)

                for heart in heart_list:

                    if heart.rect.x > 1100:
                        heart_list.remove(heart)
                        all_sprites_list.remove(heart)

                for past in block_list:

                    if past.rect.x < -100:
                        block_list.remove(past)
                        all_sprites_list.remove(past)
                        score -= 100
                        if score < 0:
                            score = 0
                        fontObj = pygame.font.Font('freesansbold.ttf', 32)
                        textSurfaceObj = fontObj.render("Score= " + str(score), True, WHITE, BLACK)
                        textRectObj = textSurfaceObj.get_rect()
                        textRectObj.center = (650, 570)

                for comet in block_list:
                    player_hit_list = pygame.sprite.spritecollide(self.player, block_list, True)

                    for hit in player_hit_list:
                        soundObj = pygame.mixer.Sound('Explosion+7.wav')
                        soundObj.play()
                        score -= 100
                        if score < 0:
                            score = 0
                        fontObj = pygame.font.Font('freesansbold.ttf', 32)
                        textSurfaceObj = fontObj.render("Score= " + str(score), True, WHITE, BLACK)
                        textRectObj = textSurfaceObj.get_rect()
                        textRectObj.center = (650, 570)
                        lives -= 1
                        fontObj2 = pygame.font.Font('freesansbold.ttf', 32)
                        textSurfaceObj2 = fontObj2.render("Lives= " + str(lives), True, WHITE, BLACK)
                        textRectObj2 = textSurfaceObj2.get_rect()
                        textRectObj2.center = (250, 570)
                        block_list.remove(hit)
                        all_sprites_list.remove(hit)

                all_sprites_list.update()
                self.on_loop()
                self._display_surf.blit(self.bg, (0, 0))
                all_sprites_list.draw(self._display_surf)
                self._display_surf.blit(textSurfaceObj, textRectObj)
                self._display_surf.blit(textSurfaceObj2, textRectObj2)

                if lives <= 0:
                    self._running = False

                pygame.display.flip()
                pygame.display.update()
                self.clock.tick(60)

            #self._display_surf.blit(self.bg, (0, 0))
            #all_sprites_list.draw(self._display_surf)
            #pygame.display.flip()
            #pygame.display.update()
            #self.clock.tick(60)

            self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()