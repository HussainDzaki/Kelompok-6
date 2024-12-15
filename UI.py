import pygame, sys
mainClock = pygame.time.Clock()

from pygame.locals import *

pygame.init()
pygame.display.set_caption("Smart Microwave")
Screen = pygame.display.set_mode((500,500), 0 ,32)

font = pygame.font.SysFont(None, 20)    
click = False

start_img = pygame.image.load("./Asset/Start.png")

# COLORS
TEAL = (84, 188, 209)
WHITE = (255,255,255)
GREEN = (84, 209, 99)
RED = (212, 84, 49)
BLACK = (0,0,0)

# Drawing Text Function
def draw_text(text, font, color, surface, coords):
    textobj = font.render(text,1,color)
    textrect = textobj.get_rect()
    textrect.topleft = (coords)
    surface.blit(textobj, textrect)

# Drawing Image Function
def draw_img(x,y,surface,img,scale):
    width = img.get_width()
    height = img.get_height()
    img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
    imgrect = img.get_rect()
    imgrect.topleft = (x,y)
    surface.blit(img, (x,y))

def Baking_function():
    running = True
    
    while running: 
        Screen.fill((0,0,0))
        draw_text("Baking", font, WHITE, Screen, (20,20))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
       
        pygame.display.update()
        mainClock.tick(60)

def Heating_function():
    running = True
    while running: 
        Screen.fill((0,0,0))
        draw_text("Heating", font, WHITE, Screen, (20,20))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pygame.display.update()
        mainClock.tick(60)

def Popcorn_preset():
    kotak = pygame.Rect(50,250,100,100)
    pygame.draw.rect(Screen,WHITE, kotak)
    
def main_loop():
    while True : 
        
        Screen.fill((54, 56, 61))
        draw_text("Smart Microwave", font, WHITE, Screen, (20,20))
        
        # Mouse Position
        mx,my = pygame.mouse.get_pos()


        # Button sizes
        Popcorn = pygame.Rect(25,350,75,25)
        Baking = pygame.Rect(25,300,75,25)
        Preheat = pygame.Rect(25,400,75,25)
        Preset1 = pygame.Rect(125,300,75,25)
        Preset2 = pygame.Rect(125,350,75,25)
        Preset3 = pygame.Rect(125,400,75,25)
        EcoMode = pygame.Rect(400,300,75,25)
        startbutton = pygame.Rect(420,460,40,20)

        # text box size 
        text_box = pygame.Rect(360,400,70,15)

        # Microwave Screen
        Microwave_Screen = pygame.Rect(20,50,460,200)

        # Placing Buttons/Object
        pygame.draw.rect(Screen,TEAL,startbutton)
        pygame.draw.rect(Screen,TEAL, Popcorn)
        pygame.draw.rect(Screen,TEAL, Baking)
        pygame.draw.rect(Screen,TEAL, Preheat)
        pygame.draw.rect(Screen,TEAL, Preset1)
        pygame.draw.rect(Screen,TEAL, Preset2)
        pygame.draw.rect(Screen,TEAL, Preset3)
        pygame.draw.rect(Screen,GREEN, EcoMode)
        pygame.draw.rect(Screen,WHITE, Microwave_Screen)
        pygame.draw.rect(Screen,WHITE, text_box)

       # Checking Collider with Mouse

        if Popcorn.collidepoint((mx,my)):
            if click:
                Popcorn_preset()

        if Baking.collidepoint((mx,my)):
            if click: 
                Baking_function()
        if Preheat.collidepoint((mx,my)):
            if click:
                pass
        if startbutton.collidepoint((mx,my)):
            if click:
                pass
        if Preset1.collidepoint((mx,my)):
            if click:
                pass
        if Preset2.collidepoint((mx,my)):
            if click:
                pass
        if Preset3.collidepoint((mx,my)):
            if click:
                pass
        if EcoMode.collidepoint((mx,my)):
            if click:
                pass
        
        # Placing Image and text
        draw_img(startbutton.x,startbutton.y,Screen,start_img,1.5)
        draw_text("Preset: ", font, WHITE, Screen,(25,280))
        draw_text("Popcorn", font, WHITE, Screen, (Popcorn.centerx-25,Popcorn.centery-5))
        draw_text("Baking", font, WHITE, Screen, (Baking.centerx-25, Baking.centery-5))
        draw_text("Preheat", font, WHITE, Screen, (Preheat.centerx-25, Preheat.centery-5))

        draw_text("Preset1", font, WHITE, Screen, (Preset1.centerx-25, Preset1.centery-5))
        draw_text("Preset2", font, WHITE, Screen, (Preset2.centerx-25, Preset2.centery-5))
        draw_text("Preset3", font, WHITE, Screen, (Preset3.centerx-25, Preset3.centery-5))

        draw_text("EcoMode", font, WHITE, Screen, (EcoMode.centerx-30, EcoMode.centery-5))

        draw_text("00:01", font, WHITE, Screen, (250,360))
        draw_text("Time", font, WHITE, Screen, (250,320))
        draw_text("Temp", font, WHITE, Screen, (320,320))
        draw_text("27", font, WHITE, Screen, (320,360))
        draw_text("Scan Here", font, WHITE, Screen, (360,380))


        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


main_loop()