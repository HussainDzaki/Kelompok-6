import pygame, sys, time, random
mainClock = pygame.time.Clock()
wattage_microwave = 1000 #(Watt) 
heat_cap_microwave = 20000 #(Joule)
fan_efficiency = 20 #(Joule)
iya_tidak = ["iya", "tidak"]

from pygame.locals import *

pygame.init()
pygame.display.set_caption("Smart Microwave")
Screen = pygame.display.set_mode((500,500), 0 ,32)

font = pygame.font.SysFont(None, 20)
font_big = pygame.font.SysFont(None, 60)
font2 = pygame.font.Font('RussoOne-Regular.ttf', 12)
font2_big = pygame.font.Font('RussoOne-Regular.ttf', 36)
click = False

start_img = pygame.image.load("Start.png")
pause_bg = pygame.image.load("PauseBG.png")
up_button_img = pygame.image.load("UpButton.png")
down_button_img = pygame.image.load("DownButton.png")
up_button_img_pressed = pygame.image.load("PressedUpButton.png")
down_button_img_pressed = pygame.image.load("PressedDownButton.png")

# COLORS
BG_COLOR = (54, 56, 61)
BG_COLOR_DARK = (27, 28, 31)
TEAL = (84, 188, 209)
TEAL_DARKER = (84, 144, 209)
WHITE = (255,255,255)
GREEN = (84, 209, 99)
RED = (212, 84, 49)
BLACK = (0,0,0)

# Button sizes
Popcorn = pygame.Rect(25,350,75,25)
Baking = pygame.Rect(25,300,75,25)
Preheat = pygame.Rect(25,400,75,25)
Preset1 = pygame.Rect(125,300,75,25)
Preset2 = pygame.Rect(125,350,75,25)
Preset3 = pygame.Rect(125,400,75,25)
EcoMode = pygame.Rect(400,300,75,25)
startbutton = pygame.Rect(420,460,40,20)
timebutton = pygame.Rect(245,335, 42, 20)
tempbutton = pygame.Rect(315,335, 42, 20)

def inputOption(inputtext, validator) :
    found = False
    while found == False :
        input1 = input(inputtext)
    
        for i in validator :
            if input1 == i :
                found = True
        
        if found == False :
            errormsg = "Input tidak valid. Silakan masukan "
            for i in range(len(validator)) :
                errormsg += f"'{validator[i]}'"
                if i == (len(validator) - 2) :
                    errormsg += " atau "
                elif i == (len(validator) - 1) :
                    errormsg += "!"
                else :
                    errormsg += ", "
            print(errormsg)
        else :
            return input1


def isNumber(character) :
    found = False
    for i in "0123456789" :
        if i == character :
            found = True
    
    return found

# Drawing Text Function
def draw_text(text, font, color, surface, coords):
    textobj = font.render(text,1,color)
    textrect = textobj.get_rect()
    textrect.topleft = (coords)
    surface.blit(textobj, textrect)
    
def draw_dynamic_text(text, font, color, surface, coords) :
    prev_width = 0
    for i in range(len(text)) :
        textobj = font.render(text[i],1,color)
        textrect = textobj.get_rect()
        textrect.topleft = (coords[0] + prev_width, coords[1])
        #print([textrect.width, textrect.height])
        prev_width += textrect.width
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

def mainTimer(waktu, level_value, heat_cap_value, read_mass) :
    fan_efficiency1 = fan_efficiency
    temp_predict = 25
    flash = True
    exit_operasi = False
    asap_terdeteksi = False
    timer_nyala = True

    while waktu >= 0 and timer_nyala : 
        print(waktu)
        if temp_predict > 80 :
            fan_efficiency1 *= 10
        
        #Perhitungan untuk prediksi suhu makanan/minuman di dalam microwave (Sebagai prediksi untuk kapan munculnya asap)
        #(Sebenarnya tidak termasuk kode microwave, tetapi untuk mensimulasikan alarm asap)
        if asap_terdeteksi ==  False :
            if ((wattage_microwave * level_value) - fan_efficiency)/(heat_cap_value/100 * read_mass) < 0.5 :
                temp_predict += round(((wattage_microwave * level_value) - fan_efficiency1)/(heat_cap_value/100 * read_mass), 1) #Perhitungan suhu pemanasan microwave tiap detik
            else :
                temp_predict += 0.2
        else : 
            temp_predict -= (fan_efficiency1)/(heat_cap_value/100 * read_mass) #Pendinginan microwave menggunakan kipas internal

        
        
        if asap_terdeteksi == False : 
            tampilan_waktu = f"        {timeFormat(waktu)}   " #Menampilkan dalam bentuk 00:00 dimana menit dan detik
            waktu -= 1
        else :
            if flash == True :
                tampilan_waktu = "ASAP TERDETEKSI " #Menampilkan pendeteksian asap saat asap terdeteksi
                flash = False
            else :
                tampilan_waktu = "                " #Menampilkan efek kedap-kedip saat pendeteksian asap terjadi
                flash = True
        
        if temp_predict < 30 and asap_terdeteksi == True :
            tampilan_waktu = "AMAN DIKELUARKAN"   #Menampilkan saat makanan/minuman aman untuk dikeluarkan dari microwave
        
        #Tampilan UI
        pygame.draw.rect(Screen,BG_COLOR_DARK, timebutton)
        pygame.draw.rect(Screen,BG_COLOR_DARK, tempbutton)
        
        draw_text(timeFormat(waktu), font2, WHITE, Screen, (249,338))
        draw_text("{:.1f}".format(temp_predict), font2, WHITE, Screen, (320,338))
        pygame.display.update()
        
        if temp_predict > heat_cap_value * 0.5953125 and asap_terdeteksi == False : #Prediksi kapan terjadinya asap
            asap_terdeteksi = True
        elif random.randint(1,1000) == 1 :
            asap_terdeteksi = True
        elif temp_predict < 30 and asap_terdeteksi == True : #Saat microwave dan makanan/minuman sudah didinginkan dan aman untuk dikeluarkan
            print("Makanan aman untuk dikeluarkan.")
            asap_terdeteksi = False
            
            lanjut_operasi = inputOption("Apakah Anda ingin melanjutkan operasi microwave? (iya atau tidak): ", iya_tidak) #Opsi untuk melanjutkan operasi microwave atau memberhentikan
            if lanjut_operasi == "iya" :
                input("#Tekan tombol apapun untuk melanjutkan.")
            elif lanjut_operasi == "tidak":
                exit_operasi = True
                    
        if exit_operasi == True : #Pemberhentian operasi microwave
            print("Operasi microwave telah berhenti")
            print("")
            break
        
        #Penambahan waktu saat operasi microwave telah selesai
        if waktu == -1:
            pemastian_waktu = True
            while pemastian_waktu :
                tambah_waktu = inputOption("Apakah perlu ditambahkan waktu? (iya atau tidak): ", iya_tidak)
                if tambah_waktu == "iya":
                    input_invalid = True
                    while input_invalid :
                        input_invalid = False
                        waktu += 1 + int(input("Masukan tambahan waktu dalam detik: "))
                        if waktu <= 0 :
                            input_invalid = True
                            print("Masukkan waktu yang sesuai!")
                            waktu = -1
                elif tambah_waktu == "tidak":
                    timer_nyala = False
                    print("Sudah dipanaskan")
                    break
        time.sleep(1)

def timeSetting(waktu) :
    draw_img(0, 0, Screen, pause_bg, 1)
    
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
    confirm_button = pygame.Rect(305, 430, 100, 20)
    
    click = False
    while True :
        mx,my = pygame.mouse.get_pos()
        
        
        pygame.draw.rect(Screen, BG_COLOR, (250,340,210,120))
        pygame.draw.rect(Screen, BG_COLOR_DARK, (290,365,130,40))
        pygame.draw.rect(Screen,TEAL,confirm_button)
        
        draw_text(timeFormat(waktu), font_big, WHITE, Screen, (302,367))
        draw_text("Confirm", font, WHITE, Screen, (confirm_button.centerx-25,confirm_button.centery-7))
        
        for i in range(len(increase_buttons)) :
            draw_img(increase_buttons[i].x, increase_buttons[i].y, Screen, up_button_img, 1)
            draw_img(decrease_buttons[i].x, decrease_buttons[i].y, Screen, down_button_img, 1)
            if click :
                if increase_buttons[i].collidepoint((mx,my)) :
                    draw_img(increase_buttons[i].x, increase_buttons[i].y, Screen, up_button_img_pressed, 1)
                    pygame.display.update()
                    waktu += time_change[i]
                    
                if decrease_buttons[i].collidepoint((mx,my)) :
                    draw_img(decrease_buttons[i].x, decrease_buttons[i].y, Screen, down_button_img_pressed, 1)
                    pygame.display.update()
                    waktu -= time_change[i]

        if click :
            if confirm_button.collidepoint((mx,my)) :
                pygame.draw.rect(Screen,TEAL_DARKER,confirm_button)
                draw_text("Confirm", font, WHITE, Screen, (confirm_button.centerx-25,confirm_button.centery-7))
                pygame.display.update()
                return waktu
                
        
        if waktu < 0 :
            waktu = 0
        elif waktu > 5999 :
            waktu = 5999
        
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
    waktu = 0
    click = False
    while True : 
        
        Screen.fill(BG_COLOR)
        draw_text("Smart Microwave", font, WHITE, Screen, (20,20))
        
        # Mouse Position
        mx,my = pygame.mouse.get_pos()


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
        pygame.draw.rect(Screen,BLACK, Microwave_Screen)
        pygame.draw.rect(Screen,WHITE, text_box)
        pygame.draw.rect(Screen,BG_COLOR_DARK, timebutton)
        pygame.draw.rect(Screen,BG_COLOR_DARK, tempbutton)
        
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


        draw_text("Time", font, WHITE, Screen, (250,320))
        draw_dynamic_text(timeFormat(waktu), font2, WHITE, Screen, (249,338))
        draw_text("Temp", font, WHITE, Screen, (320,320))
        draw_text("25.0", font2, WHITE, Screen, (320,338))
        draw_text("Scan Here", font, WHITE, Screen, (360,380))
        
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
            if click and waktu > 0:
                mainTimer(waktu, 0.7, 200, 200) #Parameter masih placeholder
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
        if timebutton.collidepoint((mx,my)) :
            if click :
                waktu = timeSetting(waktu)


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