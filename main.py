import pygame
from sys import exit
from random import randint, choice

#This is a groupSingle because only contains one character
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1 = pygame.image.load('graphics/walk1.png').convert_alpha()
        walk2 = pygame.image.load('graphics/walk2.png').convert_alpha()
        self.playerWalk = [walk1, walk2]
        self.playerIndex = 0
        self.jump = pygame.image.load('graphics/jump.png').convert_alpha()
        self.image = self.playerWalk[self.playerIndex]
        self.rect = self.image.get_rect(midbottom=(80, 320))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('graphics/audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    #

    #Allow player to interact with their character through keyboard
    def controlCharacter(self):
        # take the player input
        keys = pygame.key.get_pressed()
        # this will make sure the player can only jump once at a time
        if keys[pygame.K_SPACE]and self.rect.bottom >= 320:
            self.gravity = -25
            #self.jump_sound.play()

    #Stimulate the real gravity
    def gravityFall(self):
        self.gravity += 1
        self.rect.y += self.gravity
        #Creates a "floor" so that the character cannot disappear
        if self.rect.bottom >= 320:
            self.rect.bottom = 320

    #Swap 2 images really fast so that it stimulates real walking or jumping
    def animatingCharacter(self):
        #check if the Y pos higher than the ground : it's jumping
        if self.rect.bottom < 320:
            self.image = self.jump
        else:

            #Make the transition smoother and more natural
            self.playerIndex += 0.1

            if self.playerIndex >= len(self.playerWalk): self.playerIndex= 0
            self.image = self.playerWalk[int(self.playerIndex)]

    def speedup(self):
        if score > 30:
            self.playerIndex += 0.1

        if score >20:
            self.playerIndex += 0.07

        if score >10:
            self.playerIndex +=0.05

    #Updates all function of this class, so the character is "alive"
    def update(self):
        self.speedup()
        self.controlCharacter()
        self.gravityFall()
        self.animatingCharacter()


#This is the enemy group, containing 2 types of enemy. On ground : snails, in air : flies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        #Check what types of the enemy is
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 230
        else:
            snail_1 = pygame.image.load('graphics/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 320

        #Common variables of two types of enemy
        self.animationIndex = 0
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom=(randint(900,1700), y_pos))

    #Swap two images really fast so that it stimulates real enemy moving
    def animatingEnemy(self):
        self.animationIndex += 0.1
        #Make the transition smoother and more natural
        if score > 30:
            self.animationIndex += 0.1

        if score > 20:
            self.animationIndex += 0.07

        if score > 10:
            self.animationIndex += 0.05

        if self.animationIndex >= len(self.frames): self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]

    #Use to delete enemies that disappear outside the screen, so that it won't get lag over the time
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()



    def update(self):
        self.animatingEnemy()
        self.rect.x -= 6
        if score > 30:
            self.rect.x -= 7

        if score > 20:
            self.rect.x -= 6.7

        if score > 10:
            self.rect.x -= 6.3
        self.destroy()

#This is the cloud group, including 3 types of cloud
# class Cloud(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#
#         cloudImage=pygame.image.load('graphics/cloud1.png')
#         width = cloudImage.get_width()
#         height = cloudImage.get_height()
#         y_pos = 70
#         self.image = pygame.transform.scale(cloudImage, (width/5, height/5))
#         self.rect = self.image.get_rect(midbottom=(randint(800,1000), y_pos))
#
#     def destroy(self):
#         if self.rect.x <= -100:
#             self.kill()
#
#
#     def update(self):
#         self.rect.x -= 3
#         self.destroy()
#

#The score will be equal to how long you survive, measured in second
def display_score():

    #We have to minus start time, so that it can clear our curentTime and reset the score to 0
    current_time = int(pygame.time.get_ticks() / 1000) - start_time

    if current_time == 10:
        score = test_font2.render('GOODJOB', False, "Red")
        score_rect = score.get_rect(center=(450, 70))

    elif current_time == 20:
        score = test_font2.render('AMAZING', False, "Red")
        score_rect = score.get_rect(center=(450, 70))

    elif current_time == 30:
        score = test_font2.render('UNSTOPPABLE', False, "Red")
        score_rect = score.get_rect(center=(450, 70))

    else:
         score = test_font.render(f'Score: {current_time}', False, "RED")
    score_rect = score.get_rect(center=(450, 80))

    screen.blit(score, score_rect)

    #return currentTime so that we can get the score to display when we lose
    return current_time


#Check collision. Return true or false so that we can assign our gameActive to it
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, enemyGroup, False):

        #When we start the game again, there won't be error, because the collision will still happen
        enemyGroup.empty()
        lose.play()
        pygame.time.wait(1000)
        result.play()

        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((900, 450))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

#The font using in this game :
test_font = pygame.font.Font('graphics/Pixeltype.ttf', 60)
test_font2 = pygame.font.Font('graphics/Pixeltype.ttf', 70)

#Game active uses to seperate two main stages of the game.
#The first stage of the game is the main menu, so we set the gameActive = False
game_active = False

start_time = 0
score = 0

#cloud
cloudImage1=pygame.image.load('graphics/cloud1.png')
width = cloudImage1.get_width()
height = cloudImage1.get_height()
cloudImage1=pygame.transform.scale(cloudImage1, (width/5, height/5))
cloudRec1 = cloudImage1.get_rect(midbottom=(randint(1000,1200),90))

cloudImage2=pygame.image.load('graphics/cloud1.png')
width = cloudImage2.get_width()
height = cloudImage2.get_height()
cloudImage2=pygame.transform.scale(cloudImage2, (width/5, height/5))
cloudRec2 = cloudImage2.get_rect(midbottom=(randint(1500,1700),60))

cloudImage3=pygame.image.load('graphics/cloud1.png')
width = cloudImage3.get_width()
height = cloudImage3.get_height()
cloudImage3=pygame.transform.scale(cloudImage3, (width/5, height/5))
cloudRec3 = cloudImage3.get_rect(midbottom=(randint(2000,2300),120))

sun=pygame.image.load('graphics/sun.png')
width = sun.get_width()
height = sun.get_height()
sun = pygame.transform.scale(sun,(width/60,height/60))
sunRec = sun.get_rect(midbottom=(110,10))


#background music
bg_music = pygame.mixer.Sound('graphics/audio/music.wav')
menu = pygame.mixer.Sound('graphics/audio/MENU.wav')
bg_music.play(loops=-1)
menu.play(loops=-1)

#sound effect when collision
lose = pygame.mixer.Sound('graphics/audio/lose.wav')
lose.set_volume(4)

result = pygame.mixer.Sound('graphics/audio/result.wav')
result.set_volume(2)

go = pygame.mixer.Sound('graphics/audio/go.mp3')
go.set_volume(6)

cheering = pygame.mixer.Sound('graphics/audio/cheering2.mp3')
cheering.set_volume(1)

intro= pygame.mixer.Sound('graphics/audio/intro.wav')
intro.set_volume(6)

goodjob = pygame.mixer.Sound('graphics/audio/goodjob.mp3')
goodjob.set_volume(8)



# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

# cloud = pygame.sprite.GroupSingle()

#we will add enemy when the timer triggers !
enemyGroup = pygame.sprite.Group()


#background image
sky_surface = pygame.image.load('graphics/Sky.png').convert()
width = sky_surface.get_width()
height = sky_surface.get_height()
sky_surface = pygame.transform.scale(sky_surface,(width*2,height*1.25))

ground_surface = pygame.image.load('graphics/ground.png').convert()
width = ground_surface.get_width()
height = ground_surface.get_height()
ground_surface = pygame.transform.scale(ground_surface,(width*1.5,height*1.1))

# Intro screen
stand = pygame.image.load('graphics/stand.png').convert_alpha()
stand = pygame.transform.rotozoom(stand, 0, 2)
stand_rect = stand.get_rect(center=(450, 220))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(450, 70))

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(450, 370))


# Timer use to trigger events. Spawn enemies EVERY 1.4 seconds
enemyTimer = pygame.USEREVENT + 1


interval = 2000

pygame.time.set_timer(enemyTimer, interval)


while True:
    for event in pygame.event.get():

        #create an exit button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == enemyTimer:
                    #the ratio of flies and snails is 1:2
                    enemyGroup.add(Enemy(choice(['fly', 'snail', 'snail', 'snail'])))
                    if score > 30:
                        enemyGroup.add(Enemy(choice(['fly'])))
                        enemyGroup.add(Enemy(choice(['snail'])))
                        enemyGroup.add(Enemy(choice(['snail'])))

                    if score > 20:
                        enemyGroup.add(Enemy(choice([ 'snail'])))
                        enemyGroup.add(Enemy(choice([ 'snail'])))

                    if score > 10:
                        enemyGroup.add(Enemy(choice(['snail'])))


        #Allow player press "SPACE" to start the game again
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                #store the old point to reset new point by take currentTime - startTime
                start_time = int(pygame.time.get_ticks() / 1000)
                menu.stop()
                intro.play()
                pygame.time.wait(2000)
                go.play()
                bg_music.play()

    #There are 2 main stages in this game.
    # If gameActive = True, the game is running. Otherwise, the game is at the main Menu
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 320))
        screen.blit(sun,(120,30))
        menu.stop()

        #
        # cloud.draw(screen)
        # cloud.update()

        #Draw and update character and enemies
        player.draw(screen)
        player.update()
        enemyGroup.draw(screen)
        enemyGroup.update()

        cloudRec1.x -= 3
        if cloudRec1.x < -100: cloudRec1.x = randint(800, 900)
        screen.blit(cloudImage1, cloudRec1)

        cloudRec2.x -= 3
        if cloudRec2.x < -70: cloudRec2.x = randint(1300, 1600)
        screen.blit(cloudImage2, cloudRec2)

        cloudRec3.x -= 3
        if cloudRec3.x < -50: cloudRec3.x = randint(1800, 2000)
        screen.blit(cloudImage3, cloudRec3)

        score = display_score()

        game_active = collision_sprite()


    else:
        screen.fill((94, 129, 162))
        bg_music.stop()
        screen.blit(stand,stand_rect)
        #Displaying score variables
        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(450, 370))

        #display the game name
        screen.blit(game_name, game_name_rect)

        if score == 0:
            # display instruction to start the game
            screen.blit(game_message, game_message_rect)
        else:
            # display the score
            screen.blit(score_message, score_message_rect)

    pygame.display.update()

    #set the ceiling fps to 60fps
    clock.tick(60)