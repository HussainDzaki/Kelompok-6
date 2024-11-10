import time
import os

kode = 0
value = 1

Type = ['F','D'] 
FoodDrink = [[['M',1400], ['V',900], ['P',650], ['S',1100], ['B',500], ['R',800]], [['C',1120],['T',1080],['W',1000],['M',1030]]]
Temp = [[['0',0], ['1',10], ['2',20]], [['0',30],['1',50],['2',70]]] # Temperatur 
Humidity = [['0',1],['1',1.2]] # Kelembaban makanan/minumannya
Mass = [['0',300], ['1',600], ['2',900]] #Selang massa <300, 300<=m<600
Level = [['0',20], ['1',50], ['2,',70]] #Level kegunaan energi dari microwave

Saved_Presets = [[None,None] for i in range(50)] #Tempat menyimpan preset
current_taken_slot = 0 #Jumlah preset yang ada
input_preset = 0
no_scan = 4

memasukkan_waktu = True
microwave_nyala = True

while microwave_nyala == True :
    waktu = 0
    timer_nyala = True

    print("1. Manual")
    print("2. Preset")

    input_invalid = True
    while input_invalid == True :
        input_invalid = False
        input_mode = input("Pilih cara input waktu: ")

        if input_mode == "1" :
            waktu_menit = int(input("Masukan waktu dalam menit: "))
            waktu_detik = int(input("Masukan waktu dalam detik: "))
            total_waktu = waktu_menit * 60 + waktu_detik
            waktu = total_waktu

        elif input_mode == "2" :  
            print("1. Popcorn")
            print("2. Baking")
            print("3. Preheat")
            for i in range(current_taken_slot) :
                print(f"{i + 4}. {Saved_Presets[i][0]} ({Saved_Presets[i][1]} detik)")
                if i == (current_taken_slot - 1) :
                    no_scan = i + 5
            print(f"{no_scan}. Scan kode")
            
            input_invalid2 = True
            while input_invalid2 == True :
                input_invalid2 = False
                input_preset = input("Pilih preset: ")
                
                if input_preset == "1" :
                    waktu = 180
                elif input_preset == "2" :
                    waktu = 900
                elif input_preset == "3" :
                    waktu = 120
                elif 3 < int(input_preset) < no_scan :
                    waktu = Saved_Presets[int(input_preset) - 4][1]  
                elif input_preset == str(no_scan) :
                    kode_invalid = True
                    type_value = 0
                    temp_value = [None,None]
                    temp_difference = 0
                    humid_value = 0
                    mass_value = 0
                    level_value = 0
                    
                    while kode_invalid == True :
                        kode_invalid = False
                        kode_full = input("Masukkan Kode: ")
                        
                        panjang_kode = 0
                        for i in kode_full :
                            panjang_kode += 1
                            
                        if panjang_kode != 7 :
                            kode_invalid = True

                        if kode_invalid == False :
                            for i in range(2) :
                                if kode_full[0] == Type[i] :
                                    j = 0
                                    loop_done = False
                                    while (j < 6) and loop_done == False :
                                        if kode_full[1] == FoodDrink[i][j][kode] :
                                            type_value = FoodDrink[i][j][value]
                                            loop_done = True
                                        elif i == 1 and j == 3 :
                                            loop_done = True
                                        elif i == 0 and j == 5 :
                                            loop_done = True
                                        j += 1
                                    if type_value == 0 :
                                        kode_invalid = True
                                        

                            for i in range(2) :
                                for j in range(3) :
                                    if kode_full[i + 2] == Temp[i][j][kode] :
                                        temp_value[i] = Temp[i][j][value]
                                    elif (temp_value[i] == None) and j == 2 :
                                        kode_invalid = True
                                    
                            if kode_invalid == False :
                                temp_difference = temp_value[1] - temp_value[0]


                            for j in range(2) :
                                if kode_full[4] == Humidity[j][kode] :
                                    humid_value = Humidity[j][value]
                            if humid_value == 0 :
                                kode_invalid = True
                                
                            for j in range(3) :
                                if kode_full[5] == Mass[j][kode] :
                                    mass_value = Mass[j][value]
                            if mass_value == 0 :
                                kode_invalid = True
                                
                            for j in range(3) :
                                if kode_full[6] == Level[j][kode] :
                                    level_value = Level[j][value]
                            if level_value == 0 :
                                kode_invalid = True
                        
                        if kode_invalid == True :
                            print("Masukkan kode dengan format yang benar!")
                    wakut_raw = (mass_value/type_value) * (1 + ((temp_difference) / 100)) * humid_value * (1 - (level_value/100)) * 300

                    total_waktu = 0
                    while total_waktu < wakut_raw - 1 :
                        total_waktu += 1

                    if (wakut_raw - total_waktu) > 0.5 :
                        total_waktu += 1
                    waktu = total_waktu
                else :
                    input_invalid2 = True
                    print("Input preset tidak valid!")
                    
        else : 
            input_invalid = True
            print("Input tidak valid!")
        if input_preset == 0 or input_preset == no_scan :
            input_invalid = True
            while input_invalid == True :
                input_invalid = False
                save_as_preset = input("Apakah Anda ingin menyimpan pengaturan ini sebagai preset? (iya atau tidak):")

                if save_as_preset == "iya" :
                    input_invalid2 = True 
                    while input_invalid2 == True :
                        input_invalid2 = False
                        nama_preset = input("Nama preset: ")
                        panjang_nama = 0
                        for i in nama_preset :
                            panjang_nama += 1
                        
                        if panjang_nama > 10 :
                            input_invalid2 = True
                            print("Nama terlalu panjang!")
                        
                    Saved_Presets[current_taken_slot][0] = nama_preset
                    Saved_Presets[current_taken_slot][1] = waktu                    #Menyimpan waktu di slot preset terbaru
                    print(f"Preset {Saved_Presets[current_taken_slot][0]} telah disimpan.")
                    current_taken_slot += 1 
                elif save_as_preset != ("iya" and "tidak") :
                    input_invalid = True
                    
    preset4 = ""
    panjang_preset4 = 0    
    if current_taken_slot > 0 :
        preset4 = f"4. {Saved_Presets[0][0]}"
        
        for i in preset4 :
            panjang_preset4 += 1
        
    for i in range(24 - panjang_preset4) :
        preset4 += " "

    while waktu >= 0 and timer_nyala : 
        os.system("cls" if os.name == "nt" else "clear") #Membersihkan terminal output
        
        w_m = waktu // 60
        w_d = waktu % 60
        
        if w_m < 10 :
            w_m = f"0{w_m}"
        
        if w_d < 10 :
            w_d = f"0{w_d}"
        
        tampilan_waktu = f"{w_m}:{w_d}" #Menampilkan dalam bentuk 00:00 dimana menit dan detik
        
        
        waktu -= 1
        
        print(f"""
    ______________________________________________________
    |                                                      |
    |   Smart Microwave                                    |
    |______________________________________________________|
    |                                                      |
    |   ________________________________________________   |
    |  |                                                |  |
    |  |          {tampilan_waktu}    [Scan to Cook]               |  |
    |  |________________________________________________|  |
    |                                                      |
    |                                                      |
    |          ________________________________            |
    |         |  *      *      *      *       |            |
    |         |       ( Kamera   )            |            |
    |         |_______________________________|            |
    |                                                      |
    |     [ Power ] [ Defrost ] [ Timer ] [ Start ]        |
    |     [ Temp+ ] [ Temp- ]  [ Reset ]   [ Stop ]        |
    |                                                      |
    |    ______________________________________________    |
    |   |                                              |   |
    |   |  Select Preset:                              |   |
    |   |   1. Popcorn         3. Preheat              |   |
    |   |   2. Baking          {preset4}|   |
    |   |   ==============                             |   |
    |   |                                              |   |
    |   |  [Auto Adjust]                               |   |
    |   |______________________________________________|   |
    |______________________________________________________|
    """)
        if tampilan_waktu == "00:00":
            pemastian_waktu = True
            while pemastian_waktu :
                tambah_waktu = (input("Apakah perlu ditambahkan waktu? (iya atau tidak): "))
                if tambah_waktu == "iya":
                    waktu += 1 + int(input("Masukan tambahan waktu dalam detik: "))
                    pemastian_waktu = False
                elif tambah_waktu == "tidak":
                    timer_nyala = False
                    pemastian_waktu = False
                    print("Sudah dipanaskan")
                else : 
                    print("Input tidak valid. silakan masukan 'iya' atau 'tidak'.")
                    pemastian_waktu = True
        time.sleep(1)
    #i = 0
    #while i < 14103930 :
        #i += 1
