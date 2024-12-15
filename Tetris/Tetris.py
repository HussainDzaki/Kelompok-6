import time, random, math, os, pygame

pygame.init()
width = 11
height = 20
gameTick = 0.5
gameboard = [[0 for i in range(width)] for j in range(height)]
blocksize = 35
screendimension = [805,700]

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

SCORE = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1,1,0,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,1,0,1,0,1,0,1,0,0,0,0,0],
    [0,0,1,0,0,1,0,0,0,1,0,0,1,0,1,1,0,0,1,1,1,0,0,0],
    [0,0,0,1,0,1,0,0,0,1,0,0,1,0,1,0,1,0,1,0,0,0,0,0],
    [0,1,1,0,0,0,1,1,0,0,1,1,0,0,1,0,1,0,0,1,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

number = [
    [
        [1,1,1],
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [1,1,1],
    ],
    
    [
        [1,1,0],
        [0,1,0],
        [0,1,0],
        [0,1,0],
        [1,1,1],
    ],
    
    [
        [1,1,1],
        [0,0,1],
        [1,1,1],
        [1,0,0],
        [1,1,1],
    ],
    
    [
        [1,1,1],
        [0,0,1],
        [1,1,1],
        [0,0,1],
        [1,1,1],
    ],
    
    [
        [1,0,1],
        [1,0,1],
        [1,1,1],
        [0,0,1],
        [0,0,1],
    ],
    
    [
        [1,1,1],
        [1,0,0],
        [1,1,1],
        [0,0,1],
        [1,1,1],
    ],
    
    [
        [1,1,1],
        [1,0,0],
        [1,1,1],
        [1,0,1],
        [1,1,1],
    ],
    
    [
        [1,1,1],
        [0,0,1],
        [0,1,0],
        [0,1,0],
        [0,1,0],
    ],
    
    [
        [1,1,1],
        [1,0,1],
        [1,1,1],
        [1,0,1],
        [1,1,1],
    ],
    
    [
        [1,1,1],
        [1,0,1],
        [1,1,1],
        [0,0,1],
        [1,1,1],
    ]
]

colorpresets = [[255,0,0],[255,255,0],[0,255,0],[0,0,255]]
board_surface = pygame.display.set_mode(screendimension)
board_surface.fill((40,40,60))
flame1 = pygame.image.load("Flame3-frame1.png").convert_alpha()
flame2 = pygame.image.load("Flame3-frame2.png").convert_alpha()
popcorn0 = pygame.image.load("Popcorn-frame0.png").convert_alpha()
popcornflame0 = pygame.image.load("PopcornFlame-frame0.png").convert_alpha()
center0 = pygame.image.load("Center2-frame0.png").convert_alpha()
fanR1 = pygame.image.load("FanR-frame1.png").convert_alpha()
fanR2 = pygame.image.load("FanR-frame2.png").convert_alpha()
fanL1 = pygame.image.load("FanL-frame1.png").convert_alpha()
fanL2 = pygame.image.load("FanL-frame2.png").convert_alpha()

#Border
pygame.draw.rect(board_surface, (30,30,45), (width*blocksize, 0, blocksize, height*blocksize))
pygame.draw.rect(board_surface, (20,20,30), (width*blocksize, 0, blocksize/7, height*blocksize))
pygame.draw.rect(board_surface, (20,20,30), (width*blocksize + (6*blocksize/7), 0, blocksize/7, height*blocksize))

#Background
for i in range(0, blocksize*height, int(2*blocksize/7)) :
    pygame.draw.rect(board_surface, (50,50,75), (width*blocksize + blocksize, int(i), screendimension[0] - blocksize*(1 + width) , 3))

#Next Block Border
pygame.draw.rect(board_surface, (30,30,45), (blocksize*(3 + width), blocksize, 7*blocksize, 7*blocksize))
pygame.draw.rect(board_surface, (20,20,30), (blocksize*(3 + width), blocksize, 7*blocksize, 7*blocksize), int(blocksize/7))
pygame.draw.rect(board_surface, (20,20,30), (blocksize*(4 + width) - int(blocksize/7), 2*blocksize - int(blocksize/7), 5*blocksize + 2*int(blocksize/7), 5*blocksize + 2*int(blocksize/7)), int(blocksize/7))
for i in range(len(blockpresets[0])) :
        for j in range(len(blockpresets[0][i])) :
            block_coord = pygame.Rect(blocksize*(4 + width)+ j*blocksize, 2*blocksize+ i*blocksize, blocksize, blocksize)
            pygame.draw.rect(board_surface, [40,40,60], block_coord)
            pygame.draw.rect(board_surface, [30,30,45], block_coord,5)
            
def findMiddle(n) :
    center = (n - 1)/2
    
    if center % 1 != 0 :
        coinflip = random.randint(0,1)
        if coinflip == 0 :
            center = math.ceil(center)
        else :
            center = math.floor(center)
            
    return int(center)

#Score Screen
pygame.draw.rect(board_surface, (30,30,45), (blocksize*(2 + width), 12*blocksize, 9*blocksize, 6*blocksize))
pygame.draw.rect(board_surface, (20,20,30), (blocksize*(2 + width), 12*blocksize, 9*blocksize, 6*blocksize), int(blocksize/7))
pygame.draw.rect(board_surface, (20,20,30), (blocksize*(3 + width) - int(blocksize/7), 13*blocksize - int(blocksize/7), 7*blocksize + 2*int(blocksize/7), 4*blocksize + 2*int(blocksize/7)), int(blocksize/7))
pygame.draw.rect(board_surface, (40,40,60), (blocksize*(3 + width), 13*blocksize, 7*blocksize, 4*blocksize))
fontsize = 60
font = pygame.font.Font('RussoOne-Regular.ttf', fontsize)
scoretext = font.render('SCORE :', True, colorpresets[2])
scoretext_rect = scoretext.get_rect()
scoretext_rect.center = (blocksize*(3 + width) + findMiddle(7*blocksize), 13*blocksize + fontsize/2)
board_surface.blit(scoretext, scoretext_rect)

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
    for i in array :
        print(i)
    print("")
    print("")
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
            block_coord = pygame.Rect(j*blocksize, i*blocksize, blocksize, blocksize)
            img_coord = (j*blocksize, i*blocksize)
            if color_array[i][j] != 0 :
                fixedcolor = colorpresets[color_array[i][j] - 1]
                fixedshadecolor = [math.ceil(i*0.4) for i in fixedcolor]
                pygame.draw.rect(board_surface, fixedcolor, block_coord)
                pygame.draw.rect(board_surface, fixedshadecolor, block_coord ,5)
            else: 
                pygame.draw.rect(board_surface, [40,40,60], block_coord)
                pygame.draw.rect(board_surface, [30,30,45], block_coord,5)
                
            if array[i][j] == 1 or array[i][j] == 3: 
                pygame.draw.rect(board_surface, basecolor, block_coord)
                pygame.draw.rect(board_surface, shadecolor, block_coord ,5)
                if array[i][j]  == 3 :
                    board_surface.blit(center0, img_coord)
                    
            elif array[i][j] == 4 :
                if tick % 2 == 0 :
                    board_surface.blit(flame1, img_coord)
                else :
                    board_surface.blit(flame2, img_coord)
            elif array[i][j] == 5 :
                board_surface.blit(popcorn0, img_coord)
            elif array[i][j] == 6 :
                board_surface.blit(popcornflame0, img_coord)
            elif array[i][j] == 0 :
                pygame.draw.rect(board_surface, [40,40,60], block_coord)
                pygame.draw.rect(board_surface, [30,30,45], block_coord,5)
            
            for k in y_fan :
                if i == k and fan_blocked == False :
                    if array[i][j] == 0 or array[i][j] == 7 or array[i][j] == 8 :
                        if tick % 2 == 0 :
                            board_surface.blit(fan1, img_coord)
                        else :
                            board_surface.blit(fan2, img_coord)
                    else :
                        fan_blocked = True
            

    pygame.display.flip()
    
    
def displayNextBlock(blockpreview) :
    block, color = blockpreview
    basecolor = colorpresets[color]
    shadecolor = [math.ceil(i*0.4) for i in basecolor]
    for i in range(len(block)) :
        for j in range(len(block[i])) :
            block_coord = pygame.Rect(blocksize*(4 + width)+ j*blocksize, 2*blocksize+ i*blocksize, blocksize, blocksize)
            if block[i][j] == 1 or block[i][j] == 3 :
                pygame.draw.rect(board_surface, basecolor, block_coord)
                pygame.draw.rect(board_surface, shadecolor, block_coord ,5)
            else :
                pygame.draw.rect(board_surface, [40,40,60], block_coord)
                pygame.draw.rect(board_surface, [30,30,45], block_coord,5)
                

def displayScore(score) :
    digits = 6
    scoreboard = [[0 for i in range(digits*(1 + len(number[0][0])) - 1)] for j in range(len(number[0]))]
    score = "0"*(digits - len(str(score))) + str(score)
    
    offset = 0
    for k in score:
        for i in range(len(number[int(k)])) :
            for j in range(len(number[int(k)][0])) :
                scoreboard[i][offset + j] = number[int(k)][i][j]
        offset += 4
        
    for i in range(len(scoreboard)) :
        for j in range(len(scoreboard[i])) :
            if scoreboard[i][j] == 1 :
                pygame.draw.rect(board_surface, colorpresets[2], (blocksize*(3 + width) + 8 + 10*j, blocksize*(height - 5) + 10*i, 10, 10))
                pygame.draw.rect(board_surface, [math.ceil(i*0.4) for i in colorpresets[2]], (blocksize*(3 + width) + 8 + 10*j, blocksize*(height - 5) + 10*i, 10, 10),1)
            else :
                pygame.draw.rect(board_surface, (40,40,60), (blocksize*(3 + width) + 8 + 10*j, blocksize*(height - 5) + 10*i, 10, 10))


def displayScoreText(score) :
    pygame.draw.rect(board_surface, (40,40,60), (blocksize*(3 + width), blocksize*(height - 5), 7*blocksize, 2*blocksize))
    digits = 6
    score = "0"*(digits - len(str(score))) + str(score)
    for i in range(len(score)) :
        scoredisp = font.render(score[i], True, colorpresets[2])
        scoredisp_rect = scoredisp.get_rect()
        scoredisp_rect.center = (blocksize*(3 + width) + i*fontsize*2/3 + fontsize*11/30, blocksize*(height - 3) - fontsize*2/3)
        board_surface.blit(scoredisp, scoredisp_rect)         


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
    for event in pygame.event.get() : 
        if event.type == pygame.KEYDOWN : 
            if event.key == pygame.K_LEFT:
                move = 'L'
            elif event.key == pygame.K_RIGHT :
                move = 'R'
            if event.key == pygame.K_q:
                rotation = 1
            elif event.key == pygame.K_e:
                rotation = 3
            
    if pygame.key.get_pressed()[pygame.K_DOWN] :
        move = 'D'
    pygame.event.pump()
    
    if isSquare(board) == False and rotation != 0 :
        board, block, x, y = getBlock(board)
        board = placeBlock(board, blockRotate(block, rotation), x, y)
    elif move != None :
        board =  boardMove(board, move)
                            
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
                    
            
                  
            
def mainLoop(board) :
    blockspreview = [setBlock(), setBlock()]
    color_board = board
    score = 0
    mod_flame = True
    mod_popcorn = True
    mod_fan = True
    
    while True :
        board = fanSpawn(board, mod_fan)
        board = flameSpawn(board, mod_flame)
        board, color_board = popcornSpawn(board, color_board, mod_popcorn)
        displayScoreText(score)
        board = initialBlockPlace(board, blockspreview[0][0])
        block_color = blockspreview[0][1]
        if loseCondition(board) == True :
            break
        displayBoard(board, color_board, block_color, 0)
        blockspreview = [blockspreview[1], setBlock()]
        displayNextBlock(blockspreview[0])
        time.sleep(gameTick)
        while blocksPetrified(board) == False :
            board = boardMove(board,'D')
            subTick = 0
            move_per_gametick = 5
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
        board, color_board, scoreadd = clearRow(board, color_board)
        board = fanClear(board, mod_fan)
        board = flameClear(board, mod_flame)
        score = scoreUpdate(score, scoreadd)
            
            

mainLoop(gameboard)