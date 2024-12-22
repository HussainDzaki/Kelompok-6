import pygame, sys, time, random, math
mainClock = pygame.time.Clock()


from pygame.locals import *

pygame.init()
pygame.display.set_caption("Smart Microwave")
Screen = pygame.display.set_mode((500,500), 0 ,32)

font_small = pygame.font.SysFont(None, 20)
font_medium = pygame.font.SysFont(None, 40)
font_big = pygame.font.SysFont(None, 60)
font2 = pygame.font.Font('./Asset/RussoOne-Regular.ttf', 12)
font2_big = pygame.font.Font('./Asset/RussoOne-Regular.ttf', 36)
gamefontsize = 16
gamefont = pygame.font.Font('./Asset/RussoOne-Regular.ttf', gamefontsize)
click = False

start_img = pygame.image.load("./Asset/Start.png")
onoff_img = pygame.image.load("./Asset/OnOffButton.png")
pause_bg = pygame.image.load("./Asset/PauseBG.png")
game_pause_bg = pygame.image.load("./Asset/GamePauseBG.png")
up_button_img = pygame.image.load("./Asset/UpButton.png")
down_button_img = pygame.image.load("./Asset/DownButton.png")
left_button_img = pygame.image.load("./Asset/LeftButton.png")
right_button_img = pygame.image.load("./Asset/RightButton.png")
up_button_img_pressed = pygame.image.load("./Asset/PressedUpButton.png")
down_button_img_pressed = pygame.image.load("./Asset/PressedDownButton.png")
left_button_img_pressed = pygame.image.load("./Asset/PressedLeftButton.png")
right_button_img_pressed = pygame.image.load("./Asset/PressedRightButton.png")
play_button_img = pygame.image.load("./Asset/StartButton.png")
LED_on_img = pygame.image.load("./Asset/LEDOn.png")
LED_off_img = pygame.image.load("./Asset/LEDOff.png")
LED_alert_img = pygame.image.load("./Asset/LEDAlert.png")
flame1 = pygame.image.load("./Asset/Flame3-frame1.png").convert_alpha()
flame2 = pygame.image.load("./Asset/Flame3-frame2.png").convert_alpha()
popcorn0 = pygame.image.load("./Asset/Popcorn-frame0.png").convert_alpha()
popcornflame0 = pygame.image.load("./Asset/PopcornFlame-frame0.png").convert_alpha()
center0 = pygame.image.load("./Asset/Center2-frame0.png").convert_alpha()
fanR1 = pygame.image.load("./Asset/FanR-frame1.png").convert_alpha()
fanR2 = pygame.image.load("./Asset/FanR-frame2.png").convert_alpha()
fanL1 = pygame.image.load("./Asset/FanL-frame1.png").convert_alpha()
fanL2 = pygame.image.load("./Asset/FanL-frame2.png").convert_alpha()

# COLORS
BG_COLOR = (54, 56, 61)
BG_COLOR_DARK = (27, 28, 31)
TEAL = (84, 188, 209)
TEAL_DARKER = (84, 144, 209)
WHITE = (255,255,255)
GREEN = (84, 209, 99)
RED = (212, 84, 49)
ORANGE = (255, 127, 42)
BLACK = (0,0,0)

# Inisiasi pembuatan variable scan to cook
kode = 0
value = 1

# Contoh dari kode scan to cook: FM11011 menyatakan: Makanan Daging, Suhu awal: 10, Dipanaskan hingga: 50, Kering, Massa dibawah 600, Menggunakan efisiensi microwave 50%

scan_database = [
[['F', 1], ['D', 2]],  #'F' untuk Food dan 'D' untuk Drink 
[['M',320], ['V',370], ['P',180], ['S',340], ['B',272], ['R',153]], # Food: 'M' untuk meat, 'V' untuk vegetable, 'P' untuk pasta, 'S' untuk soup, 'B' untuk bread, 'R' untuk Rice
[['C',398],['T',357],['W',420],['M',383]], # Drink: 'C' untuk coffee. 'T' untuk Tea, 'W' untuk water, 'M' untuk milk
[['0',0], ['1',10], ['2',20]], # Temperatur Awal
[['0',30],['1',50],['2',70]], # Temperatur Akhir
[['0',1],['1',1.2]], # Kelembaban awal makanan/minuman
[['0',300], ['1',600], ['2',900]], # Jangkauan massa makanan/minuman
[['0',0.2], ['1',0.5], ['2,',0.7]], # Level kegunaan energi dari microwave
]

# Button sizes
presetbuttons = [0 for j in range(6)]
for i in range(0, 6, 2) :
    presetbuttons[i], presetbuttons[i + 1] = pygame.Rect(25,300 + i*25,75,25), pygame.Rect(125,300 + i*25,75,25)

scrollupbutton = pygame.Rect(210,279,19,16)
scrolldownbutton = pygame.Rect(210,430,19,16)
EcoMode = pygame.Rect(400,300,75,50)
scan_box = pygame.Rect(100,460,75,20)
startbutton = pygame.Rect(420,460,60,30)
onbutton = pygame.Rect(420,400,60,30)
savebutton = pygame.Rect(280,460,110,20)
timebutton = pygame.Rect(245,335, 42, 20)
tempbutton = pygame.Rect(315,335, 42, 20)
levelbutton = pygame.Rect(245, 380, 150, 30)
LED_light = pygame.Rect(450, 15, 25, 25)
alarmtest = pygame.Rect(320, 15, 75, 25)
voice_command = pygame.Rect(180, 15, 120, 25)
move_left_button = pygame.Rect(0, 0, 16, 19)
move_right_button = pygame.Rect(0, 0, 16, 19)
move_down_button = pygame.Rect(0, 0, 19, 16)
rotate_right_button = pygame.Rect(0, 0, 18, 19)
rotate_left_button = pygame.Rect(0, 0, 18, 19)
# Microwave Screen
Microwave_Screen = pygame.Rect(20,50,460,200)
move_left_button.center = (Microwave_Screen.centerx + 95, Microwave_Screen.centery + 49)
move_right_button.center = (Microwave_Screen.centerx + 155, Microwave_Screen.centery + 50)
move_down_button.center = (Microwave_Screen.centerx + 125, Microwave_Screen.centery + 71)
rotate_right_button.center = (Microwave_Screen.centerx + 115, Microwave_Screen.centery + 50)
rotate_left_button.center = (Microwave_Screen.centerx + 135, Microwave_Screen.centery + 50)

# Inisiasi Game Tetris
game_width = 11
game_height = 20
gameTick = 0.5
blocksize = 10
blockpresets = [
    [
        [0,0,0,0,0],
        [0,0,1,0,0],
        [0,0,3,1,0],
        [0,0,0,1,0],
        [0,0,0,0,0]
    ],
    
    [
        [0,0,0,0,0],
        [0,0,0,1,0],
        [0,0,3,1,0],
        [0,0,1,0,0],
        [0,0,0,0,0]
    ],
    
    [
        [0,0,0,0,0],
        [0,0,1,0,0],
        [0,0,3,0,0],
        [0,0,1,1,0],
        [0,0,0,0,0]
    ],
    
    [
        [0,0,0,0,0],
        [0,0,1,0,0],
        [0,0,3,0,0],
        [0,1,1,0,0],
        [0,0,0,0,0]
    ],
    
    [
        [0,0,0,0,0],
        [0,0,1,0,0],
        [0,0,3,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0]
    ],
        
    [
        [0,0,0,0,0],
        [0,1,1,1,0],
        [0,0,3,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0]
    ],
    
    [
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,1,1,0],
        [0,0,1,1,0],
        [0,0,0,0,0]
    ]
]

colorpresets = [[255,0,0],[255,255,0],[0,255,0],[0,0,255]]
images = [flame1, flame2, popcorn0, popcornflame0, center0, fanR1, fanR2, fanL1, fanL2]

for i in range(len(images)) :
    images[i] = pygame.transform.scale(images[i], (blocksize, blocksize))

flame1, flame2, popcorn0, popcornflame0, center0, fanR1, fanR2, fanL1, fanL2 = images


wattage_microwave = 1000 #(Watt) 
heat_cap_microwave = 20000 #(Joule)
fan_efficiency = 20 #(Joule)

    #Fungsi dan Prosedur untuk Game Tetris

def findMiddle(n) :
    center = (n - 1)/2
    
    if center % 1 != 0 :
        center = math.ceil(center)
            
    return int(center)

def initialGameDisplay() :
    pygame.draw.rect(Screen, (40,40,60), Microwave_Screen)
    #Border
    pygame.draw.rect(Screen, (30,30,45), (20 + game_width*blocksize, 50, blocksize, game_height*blocksize))
    pygame.draw.rect(Screen, (20,20,30), (20 + game_width*blocksize, 50, blocksize/5, game_height*blocksize))
    pygame.draw.rect(Screen, (20,20,30), (20 + game_width*blocksize + (4*blocksize/5), 50, blocksize/5, game_height*blocksize))

    #Background
    for i in range(0, blocksize*game_height, int(2*blocksize/7)) :
        pygame.draw.rect(Screen, (50,50,75), (20 + game_width*blocksize + blocksize, 50 + int(i), 460 - blocksize*(1 + game_width) , 1))

    #Next Block Border
    pygame.draw.rect(Screen, (30,30,45), (20 + blocksize*(3 + game_width), 50 + blocksize, 7*blocksize, 7*blocksize))
    pygame.draw.rect(Screen, (20,20,30), (20 + blocksize*(3 + game_width), 50 + blocksize, 7*blocksize, 7*blocksize), int(blocksize/5))
    pygame.draw.rect(Screen, (20,20,30), (20 + blocksize*(4 + game_width) - int(blocksize/5), 50 + 2*blocksize - int(blocksize/5), 5*blocksize + 2*int(blocksize/5), 5*blocksize + 2*int(blocksize/5)), int(blocksize/5))
    for i in range(len(blockpresets[0])) :
            for j in range(len(blockpresets[0][i])) :
                block_coord = pygame.Rect(20 + blocksize*(4 + game_width)+ j*blocksize, 50 + 2*blocksize+ i*blocksize, blocksize, blocksize)
                pygame.draw.rect(Screen, [40,40,60], block_coord)
                pygame.draw.rect(Screen, [30,30,45], block_coord,5)
    
    #Score Screen
    pygame.draw.rect(Screen, (30,30,45), (20 + blocksize*(2 + game_width), 50 + 12*blocksize, 9*blocksize, 6*blocksize))
    pygame.draw.rect(Screen, (20,20,30), (20 + blocksize*(2 + game_width), 50 + 12*blocksize, 9*blocksize, 6*blocksize), int(blocksize/5))
    pygame.draw.rect(Screen, (20,20,30), (20 + blocksize*(3 + game_width) - int(blocksize/7), 50 + 13*blocksize - int(blocksize/5), 7*blocksize + 2*int(blocksize/5), 4*blocksize + 2*int(blocksize/5)), int(blocksize/5))
    pygame.draw.rect(Screen, (40,40,60), (20 + blocksize*(3 + game_width), 50 + 13*blocksize, 7*blocksize, 4*blocksize))
    
    scoretext = gamefont.render('SCORE :', True, colorpresets[2])
    scoretext_rect = scoretext.get_rect()
    scoretext_rect.center = (20 + blocksize*(3 + game_width) + findMiddle(7*blocksize), 50 + 13*blocksize + gamefontsize*2/3)
    Screen.blit(scoretext, scoretext_rect)

def boardClear(board) :
    return [[0 for i in range(len(board[0]))] for j in range(len(board))]

def blockRotate(block, n) :
    centerfound = False
    dimension = len(block)
    for i in block :
        for j in i :
            if j == 3 :
                centerfound = True
    
    if centerfound == True :
        for i in range(n) :
            for j in range(int(dimension/2)) :
                for k in range(dimension - j - 1) :
                    temp = block[j][k]
                    block[j][k] = block[dimension - 1 - k][j]
                    block[dimension - 1 - k][j] = block[dimension - 1 - j][dimension - 1 - k]
                    block[dimension - 1 - j][dimension - 1 - k] = block[k][dimension - 1 - j]
                    block[k][dimension - 1 - j] = temp
    
    return block

def furthestPointBlock(block, furthest) :
    xpoint = findMiddle(len(block[0]))
    ypoint = findMiddle(len(block))
    for i in range(len(block)) :
        for j in range(len(block[i])) :
            if furthest == "left" :
                if (block[i][j] == 1 or block[i][j] == 3) and j < xpoint :
                    xpoint = j
            elif furthest == "right" :
                if (block[i][j] == 1 or block[i][j] == 3) and j > xpoint :
                    xpoint = j
            elif furthest == "up" :
                if (block[i][j] == 1 or block[i][j] == 3) and i < ypoint :
                    ypoint = i
            elif furthest == "down" :
                if (block[i][j] == 1 or block[i][j] == 3) and i > ypoint :
                    ypoint = i
            
    if furthest == "left" or furthest == "right" :
        return xpoint
    if furthest == "up" or furthest == "down" :
        return ypoint

def isSquare(board) : 
    square = True
    for i in board :
        for j in i :
            if j == 3 :
                square = False
                
    return square

def isRoofed(board, x, y) :
    roofed = False
    for i in range(y - 1, -1, -1) :
        if board[i][x] == 2 :
            roofed = True
    
    return roofed

def spaceAvailable(board, block, x, y) :
    overlap = False
    out_of_bounds = False
    for i in range(len(block)) :
        for j in range(len(block[i])) :
            offset = findMiddle(len(block[i]))
            if len(board) > (i + y - offset) >= 0 :
                if len(board[i + y - offset]) > (j + x - offset) >= 0 :
                    if board[i + y - offset][j + x - offset] == 2 and (block[i][j] == 1 or block[i][j] == 3) :
                        overlap = True
                else :
                    if block[i][j] == 1 or block[i][j] == 3 :
                        out_of_bounds = True
            else :
                if block[i][j] == 1 or block[i][j] == 3 :
                    out_of_bounds = True
    
    if overlap == True or out_of_bounds == True :
        return False
    else :
        return True

def setBlock() :
    block = blockpresets[random.randint(0,len(blockpresets) - 1)]
    block = blockRotate(block, random.randint(0,3))
    blockcolor = random.randint(0,len(colorpresets) - 1)
    
    return block, blockcolor

def getBlock(board) :
    blockgotten = [[0 for i in range(len(blockpresets[0][0]))] for j in range(len(blockpresets[0]))]
    
    for i in range(len(board)) :
        for j in range(len(board[i])) :
            if board[i][j] == 3 :
                xcenter, ycenter = j, i
                
    for i in range(len(blockgotten)) :
        for j in range(len(blockgotten[i])) :
            offset = findMiddle(len(blockgotten[i]))
            if len(board) > (i + ycenter - offset) >= 0 :
                if len(board[i + ycenter - offset]) > (j + xcenter - offset) >= 0 :
                    if board[i + ycenter - offset][j + xcenter - offset] == 1 or board[i + ycenter - offset][j + xcenter - offset] == 3 :
                        blockgotten[i][j] = board[i + ycenter - offset][j + xcenter - offset]
                        board[i + ycenter - offset][j + xcenter - offset] = 0
    
    return board, blockgotten, xcenter, ycenter

def placeBlock(board, block, x, y) : 
    while spaceAvailable(board, block, x, y) == False :
        while y + (furthestPointBlock(block, "up") - findMiddle(len(block))) < 0 :
            y += 1

        while y + (furthestPointBlock(block, "down") - findMiddle(len(block))) >= len(board) :
            y -= 1
                
        while (x + (furthestPointBlock(block, "left") - findMiddle(len(block[0])))) < 0 :
            x += 1

        while (x + (furthestPointBlock(block, "right") - findMiddle(len(block[0])))) >= len(board[y]) :
            x -= 1
        
            
        y_up = x_left = x_right = 0
        go_left = go_right = True
        
        while spaceAvailable(board, block, x, y - y_up) == False :
            y_up += 1
            print("i")
                
        while (spaceAvailable(board, block, x - x_left, y) == False) or x_left > 5:
            x_left += 1
            if x_left > 5:
                go_left = False
                break
        
        while (spaceAvailable(board, block, x + x_right, y) == False) or x_right > 5:
            x_right += 1
            if x_right > 5 :
                go_right = False
                break
        
        if (2*y_up <= 3*x_left) and (2*y_up <= 3*x_right) :
            y -= y_up
        elif (x_left < x_right) and go_left == True :
            x -= x_left
        elif (x_right < x_left) and go_right == True :
            x += x_right

        
    
    for i in range(len(block)) :
        for j in range(len(block[i])) :
            offset = findMiddle(len(block[i]))
            if len(board) > (i + y - offset) >= 0 :
                if len(board[i + y- offset]) > (j + x - offset) >= 0 :
                    if block[i][j] == 1 or block[i][j] == 3 :
                        board[i + y - offset][j + x - offset] = block[i][j]
    
    return board
               
def initialBlockPlace(board, block) :
    h = furthestPointBlock(block, "up")
    cboard = findMiddle(len(board[0]))
    cblock = findMiddle(len(block[0]))
    
    for i in range(len(block)) :
        for j in range(len(block[i])) :
            if i - h >= 0  :
                if board[i - h][cboard - cblock + j] != 2 :
                    board[i - h][cboard - cblock + j] = block[i][j]
    
    return board

def petrifyScan(board, currentcolor,color_board) :
    petrify = False
    for i in range(len(board)) :
        for j in range(len(board[i])) :
            if board[i][j] == 1 or board[i][j] == 3 :
                if i == (len(board) - 1) : 
                    petrify = True
                elif board[i + 1][j] == 2 :
                    petrify = True
                    
    if petrify == True :
        for i in range(len(board)) :
            for j in range(len(board[i])) :
                if board[i][j] == 1 or board[i][j] == 3 :
                    board[i][j] = 2
                    color_board[i][j] = currentcolor + 1
    
    return board, color_board

def blocksPetrified(board) :
    petrified = True
    for i in range(len(board)) :
        for j in range(len(board[i])) :
            if board[i][j] == 1 or board[i][j] == 3 :
                petrified = False
    
    return petrified
            
def displayBoard(array, color_array, color, tick) :
    y_fan = []
    order = range(len(array[0]))
    for i in range(len(array)) :
        for j in range(len(array[i])) :
            if array[i][j] == 7 :
                y_fan.append(i)
                fan1, fan2 = fanR1, fanR2
            elif array[i][j] == 8 :
                y_fan.append(i)
                fan1, fan2 = fanL1, fanL2
                order = range(len(array[i]) - 1, -1, -1)
                
    basecolor = colorpresets[color]
    shadecolor = [math.ceil(i*0.4) for i in basecolor]
    for i in range(len(array)) :
        fan_blocked = False
        for j in order :
            block_coord = pygame.Rect(20 + j*blocksize, 50 + i*blocksize, blocksize, blocksize)
            img_coord = (20 + j*blocksize, 50 + i*blocksize)
            if color_array[i][j] != 0 :
                fixedcolor = colorpresets[color_array[i][j] - 1]
                fixedshadecolor = [math.ceil(i*0.4) for i in fixedcolor]
                pygame.draw.rect(Screen, fixedcolor, block_coord)
                pygame.draw.rect(Screen, fixedshadecolor, block_coord ,2)
            else: 
                pygame.draw.rect(Screen, [40,40,60], block_coord)
                pygame.draw.rect(Screen, [30,30,45], block_coord,2)
                
            if array[i][j] == 1 or array[i][j] == 3: 
                pygame.draw.rect(Screen, basecolor, block_coord)
                pygame.draw.rect(Screen, shadecolor, block_coord ,2)
                if array[i][j]  == 3 :
                    Screen.blit(center0, img_coord)
                    
            elif array[i][j] == 4 :
                if tick % 2 == 0 :
                    Screen.blit(flame1, img_coord)
                else :
                    Screen.blit(flame2, img_coord)
            elif array[i][j] == 5 :
                Screen.blit(popcorn0, img_coord)
            elif array[i][j] == 6 :
                Screen.blit(popcornflame0, img_coord)
            elif array[i][j] == 0 :
                pygame.draw.rect(Screen, [40,40,60], block_coord)
                pygame.draw.rect(Screen, [30,30,45], block_coord,2)
            
            for k in y_fan :
                if i == k and fan_blocked == False :
                    if array[i][j] == 0 or array[i][j] == 7 or array[i][j] == 8 :
                        if tick % 2 == 0 :
                            Screen.blit(fan1, img_coord)
                        else :
                            Screen.blit(fan2, img_coord)
                    else :
                        fan_blocked = True
            

    pygame.display.flip()

def displayNextBlock(blockpreview) :
    block, color = blockpreview
    basecolor = colorpresets[color]
    shadecolor = [math.ceil(i*0.4) for i in basecolor]
    for i in range(len(block)) :
        for j in range(len(block[i])) :
            block_coord = pygame.Rect(20 + blocksize*(4 + game_width)+ j*blocksize, 50 + 2*blocksize+ i*blocksize, blocksize, blocksize)
            if block[i][j] == 1 or block[i][j] == 3 :
                pygame.draw.rect(Screen, basecolor, block_coord)
                pygame.draw.rect(Screen, shadecolor, block_coord ,2)
            else :
                pygame.draw.rect(Screen, [40,40,60], block_coord)
                pygame.draw.rect(Screen, [30,30,45], block_coord, 2)
                
def displayScoreText(score) :
    pygame.draw.rect(Screen, (40,40,60), (20 + blocksize*(3 + game_width), 50 + blocksize*(game_height - 5), 7*blocksize, 2*blocksize))
    digits = 6
    score = "0"*(digits - len(str(score))) + str(score)
    for i in range(len(score)) :
        scoredisp = gamefont.render(score[i], True, colorpresets[2])
        scoredisp_rect = scoredisp.get_rect()
        scoredisp_rect.center = (20 + blocksize*(3 + game_width) + i*gamefontsize*2/3 + gamefontsize/2, 50 + blocksize*(game_height - 3) - gamefontsize*2/3)
        Screen.blit(scoredisp, scoredisp_rect)         

def hitborder(board) :
    left = right = down = True
    for i in range(len(board)) :
        for j in range(len(board[i])) :
            if (board[i][j] == 1 or board[i][j] == 3) :
                if j == 0 :
                    left = False
                elif board[i][j - 1] == 2 :
                    left = False
                
                if j == len(board[i]) - 1 :
                    right = False
                elif board[i][j + 1] == 2 :
                    right = False
                    
                if i == len(board) - 1 :
                    down = False
                elif board[i + 1][j] == 2 :
                    down = False
    
    return left, right, down
        
def boardMove(board, direction) :
    boardupdate = boardClear(board)
    x_move = 0
    y_move = 0
    
    move_left, move_right, move_down = hitborder(board)
    
    if direction == 'D' and move_down == True:
        y_move = 1
    elif direction == 'L' and move_left == True:
        x_move = -1
    elif direction == 'R' and move_right == True :
        x_move = 1
    
    for i in range(len(board) - 1, -1, -1) :
        for j in range(len(board[i])) : 
            if board[i][j] != 1 and board[i][j] != 3 and board[i][j] != 0 :
                boardupdate[i][j] = board[i][j]
            elif (board[i][j] == 1 and board[i + y_move][j] != 6) or board[i][j] == 3 :
                boardupdate[i + y_move][j + x_move] = board[i][j]
                
                
    return boardupdate

def moveControl(board) :
    move = None
    rotation = 0
    click = False
    for i in range(60) :
        mx,my = pygame.mouse.get_pos()
        
        initialGameDisplay()
        draw_img(move_left_button.left, move_left_button.top, Screen, left_button_img, 1)
        draw_img(move_right_button.left, move_right_button.top, Screen, right_button_img, 1)
        draw_img(move_down_button.left, move_down_button.top, Screen, down_button_img, 1)
        pygame.draw.rect(Screen, TEAL, rotate_left_button)
        pygame.draw.rect(Screen, TEAL, rotate_right_button)
        
        if move_left_button.collidepoint((mx,my)) :
            draw_img(move_left_button.left, move_left_button.top, Screen, left_button_img_pressed, 1)
            if click :
                move = 'L'
                
        if move_right_button.collidepoint((mx,my)) :
            draw_img(move_right_button.left, move_right_button.top, Screen, right_button_img_pressed, 1)
            if click :
                move = 'R'
        
        if move_down_button.collidepoint((mx,my)) :
            draw_img(move_down_button.left, move_down_button.top, Screen, down_button_img_pressed, 1)
            if click :
                move = 'D'
        
        if rotate_right_button.collidepoint((mx,my)) :
            pygame.draw.rect(Screen, TEAL_DARKER, rotate_right_button)
            if click :
                rotation = 3
                
        if rotate_left_button.collidepoint((mx,my)) :
            pygame.draw.rect(Screen, TEAL_DARKER, rotate_left_button)
            if click :
                rotation = 1
        
        pygame.display.update
        
        click = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    
        if isSquare(board) == False and rotation != 0 :
            board, block, x, y = getBlock(board)
            board = placeBlock(board, blockRotate(block, rotation), x, y)
            break
        elif move != None :
            board =  boardMove(board, move)
            break
                            
    return board

def clearRow(board, color_board) :
    s = 0
    for i in range(len(board) - 1, -1, -1) :
        while board[i] == [2 for j in range(len(board[i]))] :
            board.pop(i)
            board.insert(0, [0 for j in range(len(board[i - 1]))])
            color_board.pop(i)
            color_board.insert(0, [0 for j in range(len(board[i - 1]))])
            displayBoard(board, color_board, 0, 0)
            s += (s + 1)
    
    if s > 0 :
        for i in range(len(board)) :
            for j in range(len(board[i])) :
                if board[i][j] == 4 :
                    board[i][j] = 0
                    
    return board, color_board, s*100
        
def loseCondition(board) :
    moving_block_amount = 0
    cboard = findMiddle(len(board[0]))
    cblock = findMiddle(len(blockpresets[0][0]))
    
    for i in range(len(board)) :
        for j in range(len(board[i])) :
            if board[i][j] == 1 or board[i][j] == 3 :
                moving_block_amount += 1
    
    if moving_block_amount == 4 :
        return False
    else :
        return True

def scoreUpdate(score, addition) :
    score += addition
    if score < 0 :
        score = 0
        
    displayScoreText(score)
        
    return score

#Modifications
def flameAmount(board, modstate) :
    amount = 0
    if modstate == True :
        for i in board :
            for j in i :
                if j == 4 :
                    amount += 1
    
    return amount

def flameSpawn(board, modstate) :
    if modstate == True :
        for i in range(len(board)) :
            for j in range(len(board[i])) :
                random1 = random.randint(1, 25 - 2*flameAmount(board, modstate))
                if board[i][j] == 2 and isRoofed(board, j, i) == False:
                    if random1 <= 2 :
                        board[i - 1][j] = 4
    
    return board

def flameClear(board, modstate) :
    if modstate == True :
        for i in range(len(board)) :
            for j in range(len(board[i])) :
                if board[i][j] == 4 and board[i + 1][j] == 0 :
                    board[i][j] == 0
                    
    return board

def popcornSpawn(board, color_board, modstate) :
    popcorn_amount = 0
    max_popcorn = 2
    if modstate == True :
        for i in range(len(board) - 1, -1, -1) :
            for j in range(len(board[i])) :
                if board[i][j] == 2 and isRoofed(board, j, i) == False:
                    random1 = random.randint(1,20)
                    if random1 <= 2  and (popcorn_amount < max_popcorn) :
                        board[i][j] = 5
                        popcorn_amount += 1
                        color_board[i][j] = 0
                        
    return board, color_board

def popcornMove(board, modstate) :
    scoreminus = 0
    if modstate == True :
        boardupdate =  boardClear(board) 
        for i in range(len(board)) :
            for j in range(len(board[i])) :
                if board[i][j] != 5 and board[i][j] != 6 :
                    boardupdate[i][j] = board[i][j]
                else :
                    if i == 0 :
                        if board[i][j] == 6 :
                            scoreminus += 50
                        elif board[i][j]== 5 :
                            scoreminus += 20
                        boardupdate[i][j] = 0
                    elif (board[i][j] == 6 and board[i - 1][j] == 3) or  (board[i][j] == 5 and (board[i - 1][j] == 1 or board[i - 1][j] == 3)) :
                        boardupdate[i][j] = 0
                    elif board[i - 1][j] == 4 :
                        boardupdate[i - 1][j] = 6
                    else : 
                        boardupdate[i - 1][j] = board[i][j]
        
        return boardupdate, scoreminus
    else :
        return board, scoreminus
                  
def fanSpawn(board, modstate) :
    if modstate == True :
        y_edge = 0
        random1 = random.randint(0,20) 
        if random1 <= 2 :
            random2 = random.randint(0,1)
            if random2 == 0 :
                x = len(board[0]) - 1
                fan = 8             #Right to Left
                move = -1
            else :
                x = 0  
                fan = 7             #Left to Right
                move = 1
                
            for i in range(len(board)) :
                if board[i][x] == 2 :
                    y_edge = i - 2
                    break
            if y_edge > 2 :
                y = random.randint(0, y_edge)
                for i in range(2) :
                    if board[y + i][x] == 5 or board[y + i][x] == 6 :
                        board[y + i][x + move] = board[y + i][x]
                    board[y + i][x] = fan
    
    return board
                      
def fanMove(board, color_board, modstate) :
    if modstate == True :
        fanstate = 0
        boardupdate = boardClear(board)
        color_boardupdate = boardClear(color_board)
        
        for i in range(len(board) - 1, -1, -1) :
            for j in range(len(board[i])) :
                if board[i][j] == 7  or board[i][j] == 8 :
                    fanstate = board[i][j]
                    y_topfan = i
        
        if fanstate != 0 :
            block_in_fan_range = False
            for i in range(len(board) - 1, -1, -1) :
                if fanstate == 7 :
                    order = range(len(board[i]) - 1, -1, -1)
                    direction = 'R'
                    move = 1
                else :
                    order = range(len(board[i]))
                    direction = 'L'
                    move = -1
                for j in order :
                    if (i == y_topfan or i == y_topfan + 1) and (len(board[i]) > (j + move) >= 0) and (board[i][j] != fanstate) :
                        if (boardupdate[i][j + move] == 0) and (board[i][j] != 1 and board[i][j] != 3) :
                            boardupdate[i][j + move] = board[i][j]
                            color_boardupdate[i][j + move] = color_board[i][j]
                        else :
                            if board[i][j] == 1 or board[i][j] == 3 :
                                block_in_fan_range = True
                            boardupdate[i][j] = board[i][j]
                            color_boardupdate[i][j] = color_board[i][j]
                    else :
                        boardupdate[i][j] = board[i][j]
                        color_boardupdate[i][j] = color_board[i][j]
            
            if block_in_fan_range == True :
                boardupdate = boardMove(boardupdate, direction)

            return boardupdate, color_boardupdate
        else :
            return board, color_board
    else :
        return board, color_board

def fanClear(board, modstate) :
    if modstate == True :
        for i in range(len(board)) :
            for j in range(len(board[i])) :
                if board[i][j] == 7 or board[i][j] == 8 :
                    board[i][j] = 0
                
    return board                    
                
                
            

def isNumber(character) :
    found = False
    for i in "0123456789" :
        if i == character :
            found = True
    
    return found

def scanToCook(kode_full) :
    kode_invalid = False
    nilai_full = [0 for i in range(len(kode_full) + 1)]
    for i in range(len(kode_full)) :
        if i == 0 :
            k = i
        elif i == 1 :
            k = nilai_full[0]
        else :
            k = i + 1
        
        found = False
        for j in range(len(scan_database[k])) :
            if kode_full[i] == scan_database[k][j][kode] :
                nilai_full[i] = scan_database[k][j][value]
                found = True
        
        if found == False :
            kode_invalid = True
    nilai_full[7] = kode_invalid
    
    return nilai_full

# Drawing Text Function
def draw_text(text, font, color, surface, coords, centered) :
    textobj = font.render(text,1,color)
    textrect = textobj.get_rect()
    if centered :
        textrect.center = (coords)
    else :
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

def timeFormat(waktu) :
    w_m = waktu // 60
    w_d = waktu % 60
    
    if w_m < 10 :
        w_m = f"0{w_m}"
    
    if w_d < 10 :
        w_d = f"0{w_d}"
    
    return f"{w_m}:{w_d}"

def timeSetting(waktu) : 
    increase_buttons = []
    decrease_buttons = []
    time_change = [600, 60, 10, 1]
    prev_width = 0
    for i in "00:00" :
        if isNumber(i) == True :
            increase_buttons.append(pygame.Rect(304 + prev_width, 344, 19, 16))
            decrease_buttons.append(pygame.Rect(304 + prev_width, 410, 19, 16))
            prev_width += 23
        else :
            prev_width +=14
    time_display = pygame.Rect(290,365,130,40)
    confirm_button = pygame.Rect(305, 430, 100, 20)
    
    click = False
    while True :
        mx,my = pygame.mouse.get_pos()
        
        
        pygame.draw.rect(Screen, BG_COLOR, (250,340,210,120))
        pygame.draw.rect(Screen, BG_COLOR_DARK, time_display)
        pygame.draw.rect(Screen,TEAL,confirm_button)
        
        draw_text(timeFormat(waktu), font_big, WHITE, Screen, (time_display.centerx, time_display.centery + 3), True)
        draw_text("Confirm", font_small, WHITE, Screen, confirm_button.center, True)
        
        for i in range(len(increase_buttons)) :
            draw_img(increase_buttons[i].x, increase_buttons[i].y, Screen, up_button_img, 1)
            draw_img(decrease_buttons[i].x, decrease_buttons[i].y, Screen, down_button_img, 1)
            
            if increase_buttons[i].collidepoint((mx,my)) :
                draw_img(increase_buttons[i].x, increase_buttons[i].y, Screen, up_button_img_pressed, 1)
                if click :
                    pygame.display.update()
                    waktu += time_change[i]
                
            if decrease_buttons[i].collidepoint((mx,my)) :
                draw_img(decrease_buttons[i].x, decrease_buttons[i].y, Screen, down_button_img_pressed, 1)
                if click :
                    pygame.display.update()
                    waktu -= time_change[i]
                    
        if confirm_button.collidepoint((mx,my)) :
            pygame.draw.rect(Screen,TEAL_DARKER,confirm_button)
            draw_text("Confirm", font_small, WHITE, Screen, confirm_button.center, True)
            if click :
                pygame.display.update()
                return waktu
                
        
        if waktu < 0 :
            waktu = 0
        elif waktu > 5999 :
            waktu = 5999
        
        click = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()
        mainClock.tick(60)

def levelSetting(level) :
    level = int(level*100)
    popup_box = pygame.Rect(250,340,210,120)
    level_display = pygame.Rect(261,356,188,48)
    confirm_button = pygame.Rect(305, 430, 100, 20)
    level_slider = []
    
    for i in range(20) :
        level_slider.append(pygame.Rect(265 + i*9, 360, 9, 40))
    click = False
    while True :
        mx,my = pygame.mouse.get_pos()
        
        pygame.draw.rect(Screen, BG_COLOR, popup_box)
        pygame.draw.rect(Screen, BG_COLOR_DARK, level_display)
        pygame.draw.rect(Screen,TEAL, confirm_button)
        
        
        for i in range(len(level_slider)) :
            if i < level/5 :
                pygame.draw.rect(Screen, ORANGE, level_slider[i])
            else :
                pygame.draw.rect(Screen, BLACK, level_slider[i])
            if i % 2 != 0 :
                l = 12
                k = 6
            else :
                l = 6
                k = 12
                
            pygame.draw.rect(Screen, WHITE, (level_slider[i].left, level_slider[i].top, 1, k))
            pygame.draw.rect(Screen, WHITE, (level_slider[i].right - 1, level_slider[i].top, 1, l))
            pygame.draw.rect(Screen, WHITE, (level_slider[i].left, level_slider[i].bottom - k, 1, k))
            pygame.draw.rect(Screen, WHITE, (level_slider[i].right - 1, level_slider[i].bottom - l, 1, l))
        
        draw_text("Confirm", font_small, WHITE, Screen, confirm_button.center, True)
        draw_text(f"{level}%", font2, WHITE, Screen, level_display.center, True)        
        
        for i in range(len(level_slider)) :
            if click :
                if level_slider[i].collidepoint((mx,my)) :
                    level = (i + 1) * 5
            
        if confirm_button.collidepoint((mx,my)) :
            pygame.draw.rect(Screen,TEAL_DARKER,confirm_button)
            draw_text("Confirm", font_small, WHITE, Screen, confirm_button.center, True)
            if click :
                pygame.display.update()
                return level/100
        
        click = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 0.7
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()
        
def keyboardInput(popuptext, min_char, max_char) :
    popup_box = pygame.Rect(250,340,210,120)
    text_box = pygame.Rect(265,375,180,40)
    confirm_button = pygame.Rect(305, 430, 100, 20)
    input_active = True
    text = ""
    click = False
    while input_active :
        mx,my = pygame.mouse.get_pos()
        
        pygame.draw.rect(Screen, BG_COLOR, popup_box)
        pygame.draw.rect(Screen,TEAL,confirm_button)
        pygame.draw.rect(Screen, BG_COLOR_DARK, text_box)
        
        
        draw_text(popuptext, font_small, WHITE, Screen, (popup_box.centerx, popup_box.centery - 45), True)
        draw_text("Confirm", font_small, WHITE, Screen, confirm_button.center, True)
        draw_text(text, font_medium, WHITE, Screen, text_box.center, True)
        
        pygame.display.flip()
        
        if confirm_button.collidepoint((mx,my)) :
            if len(text) >= min_char :
                pygame.draw.rect(Screen,TEAL_DARKER,confirm_button)
                draw_text("Confirm", font_small, WHITE, Screen, confirm_button.center, True)
            if click :
                input_active = False
        
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN and len(text) >= min_char:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE :
                    text =  text[:-1]
                elif event.key != pygame.K_TAB and len(text) < max_char :
                    text += event.unicode
                    
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        mainClock.tick(60)
    return text

def popupMessage(text1, text2, yesorno) :
    popup_box = pygame.Rect(250,340,210,120)
    button = pygame.Rect(305, 430, 100, 20)
    yes_button = pygame.Rect(280, 430, 60, 20)
    no_button = pygame.Rect(370, 430, 60, 20)
    popup_open = True
    click = False
    while popup_open :
        mx,my = pygame.mouse.get_pos()
        
        pygame.draw.rect(Screen, BG_COLOR, popup_box)
        draw_text(text1, font_small, WHITE, Screen, popup_box.center, True)
        
        if yesorno :
            pygame.draw.rect(Screen, GREEN, yes_button)
            pygame.draw.rect(Screen, RED, no_button)
            draw_text("Yes", font_small, WHITE, Screen, yes_button.center, True)
            draw_text("No", font_small, WHITE, Screen, no_button.center, True)
        else :
            pygame.draw.rect(Screen, TEAL, button)
            draw_text(text2, font_small, WHITE, Screen, button.center, True)
        pygame.display.update()
        

        if yesorno :
            if yes_button.collidepoint((mx,my)) :
                if click :
                    return True
            if no_button.collidepoint((mx,my)) :
                if click :
                    return False
        else :
            if button.collidepoint((mx,my)) :
                pygame.draw.rect(Screen,TEAL_DARKER,button)
                draw_text("Confirm", font_small, WHITE, Screen, button.center, True)
                if click :
                    pygame.display.update()
                    return True
        
        click = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

def voiceInput() :
    vinput_invalid = True
    while vinput_invalid :
        masukan_suara = input("Berikan perintah suara : ")
        masukan_suara = masukan_suara.lower()
        # print(masukan_suara)
        
        #Pemisahan kalimat menjadi kata-kata
        kata_masukan_suara = masukan_suara.split()

        # Inisiasi variabel
        # waktu = 0
        waktu_menit = 0
        waktu_detik = 0
        kode_full = ""
        vcommand_invalid = True

        # Cocokkan dengan kata kunci 
        
        if kata_masukan_suara[0] == "microwave": 
            vinput_invalid = False
            for i in range(len(kata_masukan_suara)) :
                if kata_masukan_suara[i] == "daging" :
                    kode_full = "FM21121"
                    heat_cap_value = 320
                elif kata_masukan_suara[i] == "sayuran" :
                    kode_full = "FV21110"
                    heat_cap_value = 370
                elif kata_masukan_suara[i] == "pasta" :
                    kode_full = "FP10111"
                    heat_cap_value = 180
                elif kata_masukan_suara[i] == ("beras" or "nasi"):
                    kode_full = "FR22121"
                    heat_cap_value = 153
                elif kata_masukan_suara[i] == "roti": 
                    kode_full = "FB01111"
                    heat_cap_value = 272
                elif kata_masukan_suara[i] == "sup":
                    kode_full = "FS22111"
                    heat_cap_value = 340
                elif kata_masukan_suara[i] == "susu":
                    kode_full = "DM00100"
                    heat_cap_value = 383
                elif kata_masukan_suara[i] == "air":
                    kode_full = "DW01111"
                    heat_cap_value = 420
                elif kata_masukan_suara[i] == "kopi":
                    kode_full = "DC11100"
                    heat_cap_value = 398
                elif kata_masukan_suara[i] == "teh":
                    kode_full = "DT11100"
                    heat_cap_value = 357
                elif kata_masukan_suara [i] == "menit":
                    waktu_menit = kata_masukan_suara[i-1]
                elif kata_masukan_suara [i] == "detik":
                    waktu_detik = kata_masukan_suara[i-1]
                elif kata_masukan_suara[i] == "popcorn":
                    waktu_menit = 10
                elif kata_masukan_suara[i] == "hangatkan":
                    waktu_menit = 2
        else :
            print("Ucapkan kata kunci ""microwave"" untuk memberikan perintah suara.")

        # print(kode_full, waktu_menit, waktu_detik) 

    # pemilihan mode preset atau manual
    if waktu_menit == 0 and waktu_detik == 0 :
        #Penentuan nilai variabel untuk menghitung waktu pemanasan microwave berdasarkan kode
        j, heat_cap_value, initialtemp, finaltemp, humid_value, mass_value, level_value, kode_invalid = scanToCook(kode_full)  
        temp_difference = finaltemp - initialtemp
        
        #Rumus menghitung waktu dengan nilai variabel yang berdasarkan kode
        # print(mass_value, heat_cap_value, temp_difference, humid_value, wattage_microwave, level_value)
        waktu_raw = (mass_value*(heat_cap_value/100) * temp_difference) * humid_value / (wattage_microwave * (level_value/100))

        #Pembulatan nilai waktu
        waktu = math.ceil(waktu_raw)
    else :
        level_value = 0.7
        heat_cap_value = 200
        waktu = int(waktu_menit)*60 + int(waktu_detik)
        
    return waktu, level_value, heat_cap_value

def mainTimer(waktu, level_value, heat_cap_value, read_mass, mod_popcorn) :
    # Inisiasi Microwave
    fan_efficiency1 = fan_efficiency
    temp_predict = 25
    flash = True
    restart = False
    asap_terdeteksi = False
    timer_nyala = True
    click = False
    
    
    play_game = False
    board = [[0 for i in range(game_width)] for j in range(game_height)]
    color_board = board
    blockspreview = [setBlock(), setBlock()]
    mod_flame = level_value >= 0.6
    mod_fan = False
    lose = False
    score = 0
    initialGameDisplay()
    displayBoard(board, board, 0, 0)
    draw_img(20, 50, Screen, game_pause_bg, 1)
    playbutton = pygame.Rect(0,0, 80, 80)
    playbutton.center = (Microwave_Screen.centerx*3/2, Microwave_Screen.centery)
    
    def timetemptick(temp_predict, waktu, flash) :
        #Perhitungan untuk prediksi suhu makanan/minuman di dalam microwave (Sebagai prediksi untuk kapan munculnya asap)
        #(Sebenarnya tidak termasuk kode microwave, tetapi untuk mensimulasikan alarm asap)
        if asap_terdeteksi ==  False :
            if ((wattage_microwave * level_value) - fan_efficiency)/(heat_cap_value/100 * read_mass) < 0.5 :
                temp_predict += round(((wattage_microwave * level_value) - fan_efficiency1)/(heat_cap_value/100 * read_mass), 1) #Perhitungan suhu pemanasan microwave tiap detik
            else :
                temp_predict += 0.2
        else : 
            temp_predict -= (fan_efficiency1 * 3)/(heat_cap_value/100 * read_mass) #Pendinginan microwave menggunakan kipas internal

        mod_fan = temp_predict >= 40
        
        if asap_terdeteksi == False : 
            waktu -= 1
        else :
            if flash == True :
                draw_img(LED_light.x, LED_light.y, Screen, LED_alert_img, 1)
                draw_text
                flash = False
            else :
                draw_img(LED_light.x, LED_light.y, Screen, LED_off_img, 1)
                flash = True
        
        if temp_predict < 30 and asap_terdeteksi == True :
            draw_img(LED_light.x, LED_light.y, Screen, LED_on_img, 1)
        
        #Tampilan UI
        pygame.draw.rect(Screen,BG_COLOR_DARK, timebutton)
        pygame.draw.rect(Screen,BG_COLOR_DARK, tempbutton)
        
        draw_text(timeFormat(waktu), font2, WHITE, Screen, timebutton.center, True)
        draw_text("{:.1f}".format(temp_predict), font2, WHITE, Screen, tempbutton.center, True)
        pygame.display.update()   
    
        return temp_predict, waktu, flash

    # Timer Microwave
    while waktu >= 0 and timer_nyala :  
       
        
        
        if temp_predict > heat_cap_value * 0.5953125 and asap_terdeteksi == False : # Prediksi kapan terjadinya asap
            asap_terdeteksi = True
        elif random.randint(1,1000) == 1 :
            asap_terdeteksi = True
        elif temp_predict < 30 and asap_terdeteksi == True :                        # Saat microwave dan makanan/minuman sudah didinginkan dan aman untuk dikeluarkan
            draw_img(0, 0, Screen, pause_bg, 1)
            popupMessage("Makanan Aman Dikeluarkan", "Continue", False)
            asap_terdeteksi = False
            lanjut_operasi = popupMessage("Lanjut Operasi Microwave?", "", True)
            
            if lanjut_operasi == False :                                            # Pemberhentian operasi microwave
                popupMessage("Operasi telah diberhentikan", "Continue", False)
                return False, waktu
            else :
                restart = True
        
        #Penambahan waktu saat operasi microwave telah selesai
        if waktu <= 0 or restart:
            if restart :
                return True, waktu
            else :
                time.sleep(1)
                draw_img(LED_light.x, LED_light.y, Screen, LED_off_img, 1)
                draw_img(0, 0, Screen, pause_bg, 1)
                pygame.display.update()
                if popupMessage("Add Time?", "", True) :
                    return True, waktu
                else :
                    return False, waktu
                    
        
        
        if play_game and lose == False:
            initialGameDisplay()
            draw_img(move_left_button.left, move_left_button.top, Screen, left_button_img, 1)
            draw_img(move_right_button.left, move_right_button.top, Screen, right_button_img, 1)
            draw_img(move_down_button.left, move_down_button.top, Screen, down_button_img, 1)
            pygame.draw.rect(Screen, TEAL, rotate_left_button)
            pygame.draw.rect(Screen, TEAL, rotate_right_button)
            while True :
                board = fanSpawn(board, mod_fan)
                board = flameSpawn(board, mod_flame)
                board, color_board = popcornSpawn(board, color_board, mod_popcorn)
                displayScoreText(score)
                board = initialBlockPlace(board, blockspreview[0][0])
                block_color = blockspreview[0][1]
                if loseCondition(board) == True :
                    lose = True
                    break
                displayBoard(board, color_board, block_color, 0)
                blockspreview = [blockspreview[1], setBlock()]
                displayNextBlock(blockspreview[0])
                while blocksPetrified(board) == False :
                    for i in range(2) :
                        board = boardMove(board,'D')
                        subTick = 0
                        move_per_gametick = 5
                        for i in range(2) :
                            while subTick != move_per_gametick :
                                for i in range(3) :
                                    board, color_board = fanMove(board, color_board, mod_fan)
                                board = moveControl(board)
                                board, scoreminus = popcornMove(board, mod_popcorn)
                                score = scoreUpdate(score, -scoreminus) 
                                displayBoard(board, color_board, block_color, subTick)
                                subTick += 1
                                time.sleep(gameTick/move_per_gametick)
                        board, color_board = petrifyScan(board,block_color,color_board)
                        score = scoreUpdate(score, -flameAmount(board, mod_flame)) 
                        displayBoard(board, color_board, block_color, 0)
                        
                    temp_predict, waktu, flash = timetemptick(temp_predict, waktu, flash)
                    if waktu <= 0 :
                        lose = True
                        break
                board, color_board, scoreadd = clearRow(board, color_board)
                board = fanClear(board, mod_fan)
                board = flameClear(board, mod_flame)
                score = scoreUpdate(score, scoreadd)
                break
            
            if lose :
                time.sleep(1)
        else :
            for p in range(60) :
                
                
                if p == 0 :
                    if lose == False :
                        draw_text("START", font2_big, WHITE, Screen, (Microwave_Screen.centerx*3/2, Microwave_Screen.centery - 20), True)
                        draw_text("GAME", font2_big, WHITE, Screen, (Microwave_Screen.centerx*3/2, Microwave_Screen.centery + 10), True)
                    else :
                        draw_text("GAME", font2_big, WHITE, Screen, (Microwave_Screen.centerx*3/2, Microwave_Screen.centery - 20), True)
                        draw_text("OVER", font2_big, WHITE, Screen, (Microwave_Screen.centerx*3/2, Microwave_Screen.centery + 10), True)
                
                if p == 30 : 
                    initialGameDisplay()
                    displayBoard(board, board, 0, 0)
                    draw_img(20, 50, Screen, game_pause_bg, 1)
                
                pygame.display.update()
                    
                
                mx,my = pygame.mouse.get_pos()
                
                if click :
                    if alarmtest.collidepoint(mx,my) :
                        asap_terdeteksi = True
                    if playbutton.collidepoint(mx,my) and lose == False:
                        play_game = True
                
                click = False
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click = True
                
                time.sleep(1/60)
            temp_predict, waktu, flash = timetemptick(temp_predict, waktu, flash)

    
def main_loop():
    waktu = 0
    level_value = 0.7
    heat_cap_value = 250
    ecomode_status = "OFF"
    eco_multiplier = 1
    auto_start = False
    click = False
    Presets = [[["Popcorn", 180, 0.7, 165], False], [["Baking", 900, 0.7, 289], False], [["Preheat", 120, 0.7, 200], False]]
    displayed_presets = [None for i in range(len(presetbuttons))]
    scroll_offset = 0
    microwave_on = False
    
    while True :
        for i in range(len(presetbuttons)) :
            if i + scroll_offset*2 < len(Presets) :
                displayed_presets[i] = [Presets[i + scroll_offset*2][0][0], Presets[i  + scroll_offset*2][1]]
            else :
                displayed_presets[i] = None
            
        
        Screen.fill(BG_COLOR)
        
        
        # Mouse Position
        mx,my = pygame.mouse.get_pos()



        # Placing Buttons/Object
        pygame.draw.rect(Screen,BG_COLOR_DARK, scan_box)
        pygame.draw.rect(Screen,BG_COLOR_DARK, timebutton)
        pygame.draw.rect(Screen,BG_COLOR_DARK, tempbutton)
        pygame.draw.rect(Screen,BG_COLOR_DARK, levelbutton)
        
        if microwave_on :
            pygame.draw.rect(Screen,TEAL,startbutton)
            
            for i in range(len(displayed_presets)) :
                if displayed_presets[i] != None :
                    pygame.draw.rect(Screen,TEAL, presetbuttons[i])
                    if displayed_presets[i][1] == True :
                        pygame.draw.rect(Screen,TEAL_DARKER, presetbuttons[i])
            if ecomode_status == "ON" :
                pygame.draw.rect(Screen,GREEN, EcoMode)
                level_color = GREEN
            else :
                pygame.draw.rect(Screen,RED, EcoMode)
                level_color = ORANGE
                
            pygame.draw.rect(Screen,BG_COLOR_DARK, Microwave_Screen)
            pygame.draw.rect(Screen,GREEN, savebutton)
            pygame.draw.rect(Screen,RED, alarmtest)
            pygame.draw.rect(Screen,GREEN, voice_command)
            pygame.draw.rect(Screen,level_color, (248,383, math.ceil(level_value*eco_multiplier*144), 24))
            
        else :
            for i in range(len(presetbuttons)) :
                pygame.draw.rect(Screen,BG_COLOR_DARK, presetbuttons[i])
            pygame.draw.rect(Screen,BG_COLOR_DARK, EcoMode)
            pygame.draw.rect(Screen,BG_COLOR_DARK, savebutton)
            pygame.draw.rect(Screen,BG_COLOR_DARK, alarmtest)
            pygame.draw.rect(Screen,BG_COLOR_DARK, voice_command)
            pygame.draw.rect(Screen,BLACK, Microwave_Screen)
        
        
        
        
        if (len(Presets) > len(presetbuttons)) and microwave_on:
            pygame.draw.rect(Screen,BG_COLOR_DARK, (208, 278, 23, 171))
            scroll_bar_length = math.floor(125 * ((len(presetbuttons)/2) / math.ceil(len(Presets)/2)))
            page_number = math.ceil((len(Presets) - len(presetbuttons)) / 2)
            scroll_bar_empty = 125 - scroll_bar_length
            pygame.draw.rect(Screen,TEAL, (211, 300 + math.ceil(scroll_offset*scroll_bar_empty/page_number), 17, scroll_bar_length))
            draw_img(scrollupbutton.x, scrollupbutton.y, Screen, up_button_img,1)
            draw_img(scrolldownbutton.x, scrolldownbutton.y, Screen, down_button_img,1)
        
        
        # Placing Image 
        draw_img(LED_light.x, LED_light.y, Screen, LED_off_img, 1)
        draw_img(startbutton.x,startbutton.y,Screen,start_img,1.5)
        draw_img(onbutton.x,onbutton.y,Screen,onoff_img,1.5)

        
        if microwave_on :
            # Placing Text
            draw_text("Smart Microwave", font_small, WHITE, Screen, (20,20), False)
            draw_text("Preset: ", font_small, WHITE, Screen,(25,280), False)
            for i in range(len(displayed_presets)) :
                if displayed_presets[i] != None :
                    draw_text(displayed_presets[i][0], font_small, WHITE, Screen, presetbuttons[i].center, True)

            draw_text("EcoMode", font_small, WHITE, Screen, (EcoMode.centerx, EcoMode.centery - 10) , True)
            draw_text(ecomode_status, font_small, WHITE, Screen, (EcoMode.centerx, EcoMode.centery + 10) , True)
            
            draw_text("Save to Preset", font_small, WHITE, Screen, savebutton.center, True)
            draw_text("Alarm Test", font_small, WHITE, Screen, alarmtest.center, True)
            draw_text("Voice Command", font_small, WHITE, Screen, voice_command.center, True)


            draw_text("Time", font_small, WHITE, Screen, (250,320), False)
            draw_text(timeFormat(waktu), font2, WHITE, Screen, timebutton.center, True)
            draw_text("Temp", font_small, WHITE, Screen, (320,320), False)
            draw_text("25.0", font2, WHITE, Screen, tempbutton.center, True)
            draw_text("Scan Here", font_small, WHITE, Screen, (25,463), False)
            draw_text("Power Level", font_small, WHITE, Screen, (250,365), False)
            draw_text("{:.1f}%".format(level_value*eco_multiplier*100), font2, WHITE, Screen, levelbutton.center, True)
        
               # Checking Collider with Mouse
            
                # Preset Buttons
            for i in range(len(presetbuttons)) :
                if presetbuttons[i].collidepoint((mx,my)):
                    if displayed_presets[i] != None :
                        pygame.draw.rect(Screen,TEAL_DARKER, presetbuttons[i])
                        draw_text(displayed_presets[i][0], font_small, WHITE, Screen, presetbuttons[i].center, True)
                    if click :
                        p, waktu, level_value, heat_cap_value = Presets[i + scroll_offset*2][0]
                        for j in range(len(Presets)) :
                            Presets[j][1] = False
                        Presets[i + scroll_offset*2][1] = True
        
            # Scrollbar Buttons
        
            if len(Presets) > len(presetbuttons) :
                if scrolldownbutton.collidepoint((mx,my)) :
                    draw_img(scrolldownbutton.x, scrolldownbutton.y, Screen, down_button_img_pressed,1)
                    pygame.display.update
                    if click and (len(Presets) > len(presetbuttons)) and (scroll_offset + 1 <= page_number):
                        scroll_offset += 1
                        
                if scrollupbutton.collidepoint((mx,my)) :
                    draw_img(scrollupbutton.x, scrollupbutton.y, Screen, up_button_img_pressed,1)
                    pygame.display.update
                    if click and (len(Presets) > len(presetbuttons)) and (scroll_offset - 1 >= 0):
                        scroll_offset -= 1
            
            
            if startbutton.collidepoint((mx,my)) or auto_start:
                if (click and waktu > 0) or auto_start:
                    draw_img(LED_light.x, LED_light.y, Screen, LED_on_img, 1)
                    pygame.display.update()
                    auto_start, waktu = mainTimer(waktu, level_value * eco_multiplier, heat_cap_value, 200, Presets[0][1]) #Parameter masih placeholder
                    if auto_start :
                        waktu = timeSetting(waktu)
                        time.sleep(1)
                        
            
            if EcoMode.collidepoint((mx,my)) :
                if click : 
                    if ecomode_status == "ON" :
                        ecomode_status = "OFF"
                        eco_multiplier = 1
                    else :
                        ecomode_status = "ON"
                        eco_multiplier = 0.5
                    
            if levelbutton.collidepoint((mx,my)):
                if click:
                    draw_img(0, 0, Screen, pause_bg, 1)
                    level_value = levelSetting(level_value)
                
            if timebutton.collidepoint((mx,my)) :
                if click :
                    draw_img(0, 0, Screen, pause_bg, 1)
                    for j in range(len(Presets)) :
                            Presets[j][1] = False
                    waktu = timeSetting(waktu)
                    heat_cap_value = 250
                    
            if scan_box.collidepoint((mx,my)) :
                if click :
                    draw_img(0, 0, Screen, pause_bg, 1)
                    kode_invalid = True
                    while kode_invalid :
                    #Penentuan nilai variabel untuk menghitung waktu pemanasan microwave berdasarkan kode
                        u, heat_cap_value_scan, initialtemp, finaltemp, humid_value, mass_value, level_value_scan, kode_invalid = scanToCook(keyboardInput("Scan Code :", 7,7))
                        temp_difference = finaltemp - initialtemp
                        if kode_invalid :
                            popupMessage("Invalid Code", "Try Again", False)
                    
                    waktu = math.ceil((mass_value*(heat_cap_value_scan/100) * temp_difference) * humid_value / (wattage_microwave * (level_value_scan)))
                    level_value, heat_cap_value = level_value_scan, heat_cap_value_scan
                    
            if savebutton.collidepoint((mx,my)) :
                if click :
                    draw_img(0, 0, Screen, pause_bg, 1)
                    pygame.display.update
                    #Penginputan nama preset baru
                    nama_preset = keyboardInput("Preset Name :", 1, 10)
                            
                    Presets.append([[nama_preset, waktu, level_value, heat_cap_value], False])
            
            if voice_command.collidepoint((mx,my)) :
                if click : 
                    waktu, level_value, heat_cap_value = voiceInput()
                    auto_start = True
        
        if onbutton.collidepoint((mx,my)) :
            if click :
                if microwave_on :
                    microwave_on = False 
                else :
                    microwave_on = True

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