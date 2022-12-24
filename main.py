
import pygame
import sys
import random
import pickle

pygame.init()

screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Bug Runner')
pygame.display.set_icon(pygame.image.load('Assets/fly1.png').convert_alpha())
lavac = (207, 16, 32)
lava = pygame.Rect(0, 620, 640, 20)
tile = pygame.image.load('Assets/platform.png').convert_alpha()
tile = pygame.transform.scale(tile, (tile.get_width() * 10, tile.get_height() * 10))
value = 32
tile_set = [tile.get_rect(topleft = (150, int((value - 3) * 10))), tile.get_rect(topleft = (250, int(value * 10)))]
pygame.mixer.music.load('Assets/Track.wav')
die = pygame.mixer.Sound('Assets/lava.wav')
jump = pygame.mixer.Sound('Assets/blip.wav')
font = pygame.font.Font('freesansbold.ttf', 8)
game_active = True
clock = pygame.time.Clock()
bg = []
x1 = 0
x2 = 0
x3 = 0
num = 0
spawn = pygame.USEREVENT
high_score = pickle.load(open("high_score.dat", "rb"))
pygame.time.set_timer(spawn, 3500)

for num in range(1, 4):
    img = pygame.image.load(f'Assets/background{num}.png').convert_alpha()
    img = pygame.transform.scale(img, (img.get_width() * 10, img.get_height() * 10))
    bg.append(img)

def backgroud():
    global x1, x2, x3, num
    x2 -= 10
    x3 -= 20
    num += 1
    if num >= 4:
        num = 0
        x1 -= 10
    if x1 <= -640:
        x1 = 0
    if x2 <= -640:
        x2 = 0
    if x3 <= -640:
        x3 = 0
    screen.blit(bg[2], (x1, 0))
    screen.blit(bg[2], (x1 + 640, 0))
    screen.blit(bg[1], (x2, y2))
    screen.blit(bg[1], (x2 + 640, y2))
    screen.blit(bg[0], (x3, y1))
    screen.blit(bg[0], (x3 + 640, y1))

def lines():
    for num in range(0, 64):
        color = 100
        pygame.draw.line(screen, (color, color, color), (0, num * 10), (640, num * 10))
        pygame.draw.line(screen, (color, color, color), (num * 10, 0), (num * 10, 640))

def ADD():
    y_pos = random.randrange(value - 7, value + 7)
    run = True
    while run:
        if 10 < y_pos < 54:
            run = False
        else:
            y_pos = random.randrange(value - 10, value + 10)
            run = True
    platform = tile.get_rect(topleft = (640, int(y_pos * 10)))
    cell = (platform, y_pos)
    return cell

def tiles(list):
    for tiles in list:
        tiles.x -= 20
        screen.blit(tile, tiles)

def collide():
    if char.rect.colliderect(lava) or char.rect.right <= 0:
        die.play()
        pygame.mixer.music.stop()
        return False
    else:
        return True

class play():

    def __init__ (self, x, y):
        self.img_run = [pygame.transform.scale(pygame.image.load('Assets/run1.png').convert_alpha(), (80, 50)), pygame.transform.scale(pygame.image.load('Assets/run2.png').convert_alpha(), (80, 50))]
        self.img_fly = [pygame.transform.scale(pygame.image.load('Assets/run1.png').convert_alpha(), (80, 50)), pygame.transform.scale(pygame.image.load('Assets/fly2.png').convert_alpha(), (80, 70))]
        self.num = 0
        self.count = 0
        self.image = self.img_run[self.num]
        self.rect = self.image.get_rect(topleft = (x, y))
        self.vel_y = 0
        self.jumped = False
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        dx = 0
        dy = 0
        walk_speed = 3
        self.count += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game_active and self.jumped == False:
            self.vel_y -= 80
            self.jumped = True
            jump.play()
        
        if self.count >= walk_speed:
            self.count = 0
            self.num += 1
            self.vel_y += 20
        if self.num >= len(self.img_fly):
            self.num = 0
        if self.jumped:
            self.image = self.img_fly[self.num]
        else:
            self.image = self.img_run[self.num]
        
        if self.vel_y >= 20:
            self.vel_y = 20
        dy += self.vel_y
        for tiles in tile_set:
            if tiles.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tiles.bottom - self.rect.top
                elif self.vel_y >= 0:
                    dy = tiles.top - self.rect.bottom
                    self.jumped = False
            if tiles.colliderect(self.rect.x + 20, self.rect.y, self.width, self.height):
                dx -= 20
        
        self.rect.x += dx
        self.rect.y += dy
        screen.blit(self.image, self.rect)
    def fly(self):
        walk_speed = 5
        self.image = self.img_fly[self.num]
        self.count += 1
        if self.count >= walk_speed:
            self.count = 0
            self.num += 1
        if self.num >= len(self.img_fly):
            self.num = 0
        if self.image == self.img_fly[0]:
            screen.blit(self.image, (280, 320))
        else:
            screen.blit(self.image, (280, 300))

def menu():
    global text, y1, y2
    title1 = pygame.transform.scale(pygame.image.load('Assets/title1.png').convert_alpha(), (140, 80))
    title2 = pygame.transform.scale(pygame.image.load('Assets/title.png').convert_alpha(), (270, 80))
    btn1 = pygame.transform.scale(pygame.image.load('Assets/play.png').convert_alpha(), (160, 80))
    btn2 = pygame.transform.scale(pygame.image.load('Assets/quit.png').convert_alpha(), (160, 80))
    button1 = btn1.get_rect(topleft = (260, 230))
    button2 = btn2.get_rect(topleft = (260, 330))
    shade1 = pygame.Rect(button1.x, button1.y + 10, btn1.get_width(), btn1.get_height())
    shade2 = pygame.Rect(button1.x, button2.y + 10, btn1.get_width(), btn1.get_height())
    P = False
    Q = False
    y1 = 0
    y2 = 0
    while True:
        clock.tick(10)
        click = False
        px, py = pygame.mouse.get_pos()
        if P:
            main()
        elif Q:
            pygame.quit()
            sys.exit()
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if eve.type == pygame.MOUSEBUTTONDOWN:
                if eve.button == 1:
                    click = True
        if button1.collidepoint((px, py)) and click:
            jump.play()
            button1.y += 10
            P = True
        elif button2.collidepoint((px, py)) and click:
            jump.play()
            button2.y += 10
            Q = True
        else:
            button1.y = 230
            button2.y = 330
        backgroud()
        screen.blit(title1, (270, 30))
        screen.blit(title2, (210, 130))
        pygame.draw.rect(screen, (54, 100, 22), shade1)
        screen.blit(btn1, button1)
        pygame.draw.rect(screen, (54, 100, 22), shade2)
        screen.blit(btn2, button2)
        pygame.display.update()

def main():
    global char, game_active, tile_set, y1, y2, high_score
    char = play(150, 240)
    value = 32
    tile_set = [tile.get_rect(topleft = (150, int((value - 3) * 10))), tile.get_rect(topleft = (530, int(value * 10)))]
    pygame.mixer.music.play(-1)
    counter = 0
    y1 = 0
    y2 = 0
    score = 0
    scoreDis = font.render(f'{score}', False, (255, 255, 255))
    scoreDis = pygame.transform.scale(scoreDis, (scoreDis.get_width() * 10, scoreDis.get_height() * 10))
    count = 0
    while True:
        clock.tick(10)
        high = font.render(f'Hi : {high_score}', False, (255, 255, 255))
        high = pygame.transform.scale(high, (high.get_width() * 10, high.get_height() * 10))
        if game_active:
            backgroud()
            tiles(tile_set)
            char.update()
            pygame.draw.rect(screen, lavac, lava)
            game_active = collide()
            screen.blit(scoreDis, (300, 0))
            count += 1
            if count >= 5:
                count = 0
                score += 1
                scoreDis = font.render(f'{score}', False, (255, 255, 255))
                scoreDis = pygame.transform.scale(scoreDis, (scoreDis.get_width() * 10, scoreDis.get_height() * 10))
            if score > high_score:
                pickle.dump(score, (open('high_score.dat', 'wb')))
                high_score = pickle.load(open('high_score.dat', 'rb'))
        else:
            backgroud()
            char.fly()
            screen.blit(scoreDis, (260, 0))
            screen.blit(high, (200, 100))
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if eve.type == spawn:
                tile_set.append(ADD()[0])
                value = ADD()[1]
            if eve.type == pygame.KEYDOWN:
                if eve.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    char = play(150, 240)
                    tile_set = [tile.get_rect(topleft = (150, int((value - 3) * 10))), tile.get_rect(topleft = (530, int(value * 10)))]
                    pygame.mixer.music.play(-1)
                    score = 0
        if char.rect.y <= 0:
            char.rect.y = 0
            counter = 1
        elif char.rect.y > 20:
            counter = 0
        if counter:
            y1 = 20
            y2 = 10
            lava.y = 640
        elif counter == False:
            y1 = 0
            y2 = 0
            lava.y = 620
        pygame.display.update()

menu()
