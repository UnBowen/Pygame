import sys, pygame
import time
pygame.init()


vscreen = pygame.display.Info()
size = width, height = vscreen.current_w, vscreen.current_h
speed = [10, 10]
black = 0, 0, 0
red = 255,0,0

screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()
Starttime = time.time()
Endtime = Starttime

while 1:
    text = pygame.font.Font(r'.\Material\灵动指书手机字体.ttf', 50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed[0] = speed[0] - 1
            if event.key == pygame.K_RIGHT:
                speed[0] = speed[0] + 1
            if event.key == pygame.K_UP:
                speed[1] = speed[1] - 1
            if event.key == pygame.K_DOWN:
                speed[1] = speed[1] + 1
            if event.key == pygame.K_ESCAPE:
                sys.exit()


    if speed != [0,0]:
        Endtime = time.time()

    elif speed == [0,0]:
        text_fmt_1 = text.render(str("弱鸡，Congratulations!"), 1, (255, 0, 0))
        screen.blit(text_fmt_1, (310, 300))
        pygame.display.flip()


    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)

    time_1 = Endtime - Starttime
    text_fmt = text.render(str("弱鸡，总共用 {} 秒".format(float('%.2f' % time_1))), 1, (255, 255, 255))
    screen.blit(text_fmt, (20, 20))

    screen.blit(ball, ballrect)
    pygame.display.flip()
