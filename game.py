import pygame,time,random
from pygame.locals import *

size = 40
class game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('bgm.mp3')
        pygame.mixer.music.play()
        self.surface = pygame.display.set_mode((800, 600))  # for setting up a window
        self.surface.fill((255, 102, 153))  # filling background
        self.snake = snake(self.surface,1)
        self.snake.draw()
        self.apple = apple(self.surface)
        self.apple.draw()
        self.wait = 0.8
    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.score()
        pygame.display.flip()


        for i in range(self.snake.length):

            if self.collision(self.snake.x[i],self.snake.y[i],self.apple.x,self.apple.y):
                self.snake.increase_length()
                eat_sound = pygame.mixer.Sound('eat.mp3')
                pygame.mixer.Sound.play(eat_sound)
                self.apple.move()
                self.wait -=0.07
                if self.snake.x[i] == 0 or self.snake.x[i] == 800 or self.snake.y[i] == 0 or self.snake.y[i] == 600:
                    self.gameover()

        for i in range(3,self.snake.length):
            if self.collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
               crash = pygame.mixer.Sound('crash.mp3')
               pygame.mixer.Sound.play(crash)
               raise Exception('game over')
        if not (0 <= self.snake.x[0] <= 800 and 0 <= self.snake.y[0] <= 600):
            crash = pygame.mixer.Sound('crash.mp3')
            pygame.mixer.Sound.play(crash)
            raise Exception("Hit the boundry error")

    def gameover(self):
        self.surface.fill((153, 255, 102))
        font = pygame.font.SysFont('arial',40)
        msg = font.render(f" Game Over Your score is {self.snake.length-1}",True,(0,0,0))
        self.surface.blit(msg,(100,200))
        msg2 = font.render(f"Press Enter To Play Again.Press Esc To Exit",True,(0,0,0))
        self.surface.blit(msg2,(100,250))
        pygame.display.flip()
        pygame.mixer.music.pause()
    def reset(self):
        self.snake = snake(self.surface, 1)
        self.apple = apple(self.surface)

    def run(self):

        # event Loop
        run = True
        pause = False
        while run:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if event.key == K_UP:
                        self.snake.up()
                    if event.key == K_DOWN:
                        self.snake.down()
                    if event.key == K_LEFT:
                        self.snake.left()
                    if event.key == K_RIGHT:
                        self.snake.right()

                elif event.type == QUIT:
                    run = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.gameover()
                pause = True
                self.reset()
            time.sleep(0.2)
            pygame.display.flip()  # Updating screen
    def collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 <= x2 + size:
            if y1 >= y2 and y1 <= y2 + size:
                return True
        return False
    def score(self):
        font = pygame.font.SysFont('arial',35)
        score = font.render(f"Score: {self.snake.length-1}",True,(204, 102, 255))
        self.surface.blit(score,(650,10))



class snake:
    def __init__(self,screen,length):
        self.length = length
        self.screen = screen
        self.snake = pygame.image.load('snake.png').convert()
        self.x = [size]*self.length
        self.y = [size]*self.length
        self.direction = 'down'

    def draw(self):
        self.screen.fill((255, 255, 102))
        for i in range(self.length):
            self.screen.blit(self.snake,(self.x[i],self.y[i]))
        pygame.display.flip()
    def increase_length(self):
        self.length+=1
        self.x.append(0)
        self.y.append(0)
    def up(self):
        self.direction = 'up'

    def down(self):
        self.direction = 'down'

    def left(self):
        self.direction = 'left'

    def right(self):
        self.direction = 'right'
    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -=size
        if self.direction == 'down':
            self.y[0] +=size
        if self.direction == 'right':
            self.x[0] +=size
        if self.direction == 'left':
            self.x[0] -=size
        self.draw()

class apple:
    def __init__(self,screen):
        self.screen = screen
        self.apple = pygame.image.load('apple1.png').convert()
        self.x = size*3
        self.y = size*3
    def move(self):
        self.x = random.randint(0,20)*(size-1)
        self.y = random.randint(0,15)*(size-1)
        if self.x not in range(0,750) or self.y not in range(0,550):
            self.move()
    def draw(self):
        self.screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

if __name__ == '__main__':
    game = game()
    game.run()