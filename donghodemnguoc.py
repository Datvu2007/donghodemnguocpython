import pygame
from datetime import datetime
from math import sin,cos,pi
import ctypes, threading

pygame.init()
pygame.mixer.init()
pygame.font.init()

screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption('Clock')

pygame.mixer.music.load("sound.mp3")

font = pygame.font.SysFont('arial', 25)
font1 = pygame.font.SysFont('arial', 40)

start_text = font.render('Start', False, (0, 0, 0))
reset_text = font.render('Reset', False, (0, 0, 0))

h_text     = font.render('Hour', False, (0, 0, 0))
m_text     = font.render( 'Min', False, (0, 0, 0))
s_text     = font.render( 'Sec', False, (0, 0, 0))
add_text   = font.render(  '+' , False, (0, 0, 0))
minus_text = font.render(  '-' , False, (0, 0, 0))

def get_text_time(h,m,s):
    time=[str(h),str(m),str(s)]
    for i in range(len(time)):
        if len(time[i])==1:
            time[i]='0'+time[i]
    return ' : '.join(time)
def getxy(n,a):
    while a>=360:
        a-=360
    if a==0:
        return [0,n]
    elif a==90:
        return [n,0]
    elif a==180:
        return [0,-n]
    elif a==270:
        return [-n,0]
    elif 0<a<90:
        return [sin(a)*n,cos(a)*n]
    elif 90<a<180:
        return [cos(a-90)*n,sin(a-90)*n]
    elif 180<a<270:
        return [-sin(a-180)*n,-cos(a-180)*n]
    else:
        return [-cos(a-270)*n,sin(a-270)*n]

running=True

h=0
m=0
s=0
xs=0
ys=85
xm=0
ym=70
xh=0
yh=50
button_color=(0, 150, 255)
process_bar=0
start_count=False
play_sound=False
popup = ctypes.windll.user32.MessageBoxW

while running:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx,my=pygame.mouse.get_pos()
            if play_sound:
                pygame.mixer.music.stop()
            if 57<=my<=92:
                if 85<=mx<=120:
                    h-=1
                elif 130<=mx<=165:
                    h+=1
            elif 117<=my<=152:
                if 85<=mx<=120:
                    m-=1
                elif 130<=mx<=165:
                    m+=1
            elif 177<=my<=212:
                if 85<=mx<=120:
                    s-=1
                elif 130<=mx<=165:
                    s+=1
            elif 5<=mx<=85 and 250<=my<=290 and [h,m,s]!=[0,0,0]:
                start_count=True
                time=datetime.now().strftime("%S")
                max_time_sec=s+m*60+h*3600
            elif 92<=mx<=172 and 250<=my<=290:
                h=0
                m=0
                s=0
                process_bar=0
                start_count=False

            if h<0:h=0
            if m<0:m=0
            if s<0:s=0
            if h>99:h=99
            if m>59:
                h+=1
                m=0
            if s>59:
                m+=1
                s=0
            if not start_count:
                if [h,m,s]!=[0,0,0]:
                    process_bar=100
                else:
                    process_bar=0

    if start_count and datetime.now().strftime("%S")!=time:
        time=datetime.now().strftime("%S")
        if h==m==s==0:
            start_count=False
            play_sound=True
            pygame.mixer.music.play()
            threading.Thread(target = lambda :popup(None, ' '*15+'!!! Time out !!!\nclick to screen to pause sound', 'Clock', 0)).start()
        else:
            s-=1
            if s<0:
                s=59
                m-=1
            if m<0:
                m=59
                h-=1
            process_bar=(s+m*60+h*3600)/max_time_sec*100
    screen.fill((150,150,150))
    xs,ys=getxy(85,(360/60)*s*pi/180)
    xm,ym=getxy(70,(360/60)*m*pi/180)
    xh,yh=getxy(50,(360/12)*h*pi/180)

    #draw time
    screen.blit(font1.render(get_text_time(h,m,s),False,(255,255,255)),(50,0))

    #hour text button
    screen.blit(h_text,(25,60))
    pygame.draw.rect(screen, button_color, (85 , 57, 35, 35))
    pygame.draw.rect(screen, button_color, (130, 57, 35, 35))
    screen.blit(add_text  ,(143 ,60))
    screen.blit(minus_text,(95,60))

    #min text button
    screen.blit(m_text,(25,120))
    pygame.draw.rect(screen, button_color, (85, 117, 35, 35))
    pygame.draw.rect(screen, button_color, (130,117, 35, 35))
    screen.blit(add_text  ,(143 ,120))
    screen.blit(minus_text,(95,120))

    #sec text button
    screen.blit(s_text,(25,180))
    pygame.draw.rect(screen, button_color, (85, 177, 35, 35))
    pygame.draw.rect(screen, button_color, (130,177, 35, 35))
    screen.blit(add_text  ,(143 ,180))
    screen.blit(minus_text,(95,180))

    #draw clock
    pygame.draw.circle(screen, (0,0,0), (330, 140), 100)
    pygame.draw.circle(screen, (255,255,255), (330, 140), 95)
    for i in range(12):
        tx,ty=getxy(91,(360/12)*i*pi/180)
        pygame.draw.circle(screen, (0,0,0), (330+tx, 140-ty), 3)
    #draw hand
    pygame.draw.line(screen, (150,150,150), (330, 140), (330+xs, 140-ys), 2)
    pygame.draw.line(screen, (0,0,0), (330, 140), (330+xm, 140-ym), 4)
    pygame.draw.line(screen, (255,0,0), (330, 140), (330+xh, 140-yh), 4)
    #draw dot
    pygame.draw.circle(screen, (100,100,100), (331, 140), 5)

    #draw start button
    pygame.draw.rect(screen, (0,255,0), (5, 250, 80, 40))
    screen.blit(start_text  ,(17 ,253))

    #draw reset button
    pygame.draw.rect(screen, (255,150,150), (92, 250, 80, 40))
    screen.blit(reset_text  ,(97 ,253))

    #draw process bar
    pygame.draw.rect(screen, (0  ,0  ,0  ), (200, 250, 250, 40))
    pygame.draw.rect(screen, (255,255,255), (205, 255, 240, 30))
    pygame.draw.rect(screen, (255,  0,  0), (205, 255, (240/100)*process_bar, 30))

    pygame.display.update()
pygame.quit()