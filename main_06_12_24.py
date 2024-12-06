#Judul : Smart Microwave
#Deskripsi : Microwave ini memiliki banyak fitur yang mempermudah menggunakan microwave, salah satunya adalah dapat menginput secara manual atau 
#            secara otomatis berupa beberapa preset atau fitur scan to cook. Ada fitur selain itu juga dapat mendeteksi dengan "suara", dan deteksi 
#            asap pada microwave
             

import time
import os
import math

# Kamus
# Alphabet : Array [0..25] of Array [0..1] of (str)
# asap_terdeteksi : bool
# c : int
# current_taken_slot : int
# custom_preset : Array [0..2] of str
# eco_display : str
# eco_mode : str
# exit_operasi : bool
# fan_efficiency : int
# flash : bool
# FoodDrink : Array [0..1, 0..5] of Array [0..1] of (str, int)
# heat_cap_microwave : int
# heat_cap_value : int
# humid_value : float
# Humidity : Array [0..1] of (str, float)
# i : int
# index : int
# initialtemp : int
# input_invalid : bool
# input_preset : int
# j : int
# jumlah_column : float
# jumlah_kata : int
# jumlah karakter : int
# jumlah_pdisplay : int
# kata_masukan_suara : Array of str
# keluaran : Array [0..0] of str
# kode : int
# kode_full : str
# Level : Array [0..2] of (str, int)
# level_value : float
# list_masukan_suara : Array of str
# lowered : bool
# masukan_suara : str
# masukan_suara_temp : str
# Mass : Array [0..2] of (str, int)
# mass_value : int
# memasukkan_waktu : bool
# microwave_nyala : bool
# nama_preset : str
# no_scan : str
# panjang_cpreset : Array [0..2] of int
# penyimpan_kata : str
# preset_option : Array 
# read_mass : int
# Saved_Presets : Array [0..49] of Array [0..3] of (str, int, float, int)
# scroll_bar : str
# scroll_ratio : float
# tambah_waktu : str
# tampilan_waktu : str
# Temp : Array [0..1, 0..2] of Array [0..1] of (str, int)
# temp_difference : int
# temp_predict : float
# temp_value : Array [0..1] of int
# timer_nyala : bool
# Type : Array [0..1] of str
# ulang : bool
# value : int
# vinput_invalid : bool
# voice_command_on : str
# w_m : str
# w_d : str
# waktu : int
# waktu_detik : int
# waktu_menit : int
# waktu_raw : float
# wattage_microwave : int


#Algoritma

#Spesifikasi kemampuan microwave
wattage_microwave = 1000 #(Watt) 
heat_cap_microwave = 20000 #(Joule)
fan_efficiency = 20 #(Joule)
memasukkan_waktu = True
microwave_nyala = True
no_scan = "4"
eco_display = "OFF"
input_preset = 0


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
[['0',20], ['1',50], ['2,',70]], # Level kegunaan energi dari microwave
]

# Inisiasi alphabet untuk pembacaan perintah suara
Alphabet = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"]

# Inisiasi penyimpanan preset
Saved_Presets = [[None,None,None,None] for i in range(50)] #Tempat menyimpan preset
current_taken_slot = 0 #Jumlah preset yang ada

iya_tidak = ["iya", "tidak"]

# Fungsi
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

# Main loop dari penggunaan microwave
while microwave_nyala == True :
    
    # Keadaan standar microwave
    waktu = 0
    timer_nyala = True
    level_value = 70
    heat_cap_value = 250
    
    # Pemilihan cara input perintah microwave
    
    voice_command_on = inputOption("Apakah Anda ingin menyalakan voice command? (iya atau tidak): ", iya_tidak)
            
    if voice_command_on == "iya": #input microwave berbasis suara
        vinput_invalid = True
        while vinput_invalid :
            masukan_suara = input("Berikan perintah suara : ")
            masukan_suara = masukan_suara.lower()
            print(masukan_suara)
            
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
                        kode_full = "DA01111"
                        heat_cap_value = 420
                    elif kata_masukan_suara[i] == "kopi":
                        kode_full = "DC22100"
                        heat_cap_value = 398
                    elif kata_masukan_suara[i] == "teh":
                        kode_full = "DT22100"
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
                waktu_raw = (mass_value*(heat_cap_value/100) * temp_difference) * humid_value / (wattage_microwave * (level_value/100))

                #Pembulatan nilai waktu
                waktu = math.ceil(waktu_raw)
            else :
                waktu = int(waktu_menit)*60 + int(waktu_detik)  

            # print(waktu)
                
                
    elif voice_command_on == "tidak": #input microwave secara manual/tombol
        print("1. Manual")
        print("2. Preset")

        input_mode = inputOption("Pilih cara input waktu: ", ["1", "2"])

        if input_mode == "1" : #input microwave secara manual
            input_preset = 0
            
            input_invalid = True
            while input_invalid :
                input_invalid = False
                waktu_menit = int(input("Masukan waktu dalam menit: "))
                waktu_detik = int(input("Masukan waktu dalam detik: "))
                if (waktu_detik or waktu_menit < 0) :
                    input_invalid = True
                    print("Masukkan input waktu yang sesuai!")
                
                
            total_waktu = waktu_menit * 60 + waktu_detik
            waktu = total_waktu

        elif input_mode == "2" :  #input microwave menggunakan preset/kode
            print("1. Popcorn")
            print("2. Memasak")
            print("3. Memanaskan")
            
            #Penampilan custom preset
            for i in range(current_taken_slot) :
                print(f"{i + 4}. {Saved_Presets[i][0]} ({Saved_Presets[i][1]} detik, {Saved_Presets[i][2]}%)")
                if i == (current_taken_slot - 1) :
                    no_scan = i + 5
            print(f"{no_scan}. Scan kode")
            
            preset_option =[]
            for i in range(no_scan) :
                preset_option.append(str(i + 1))
        
            input_preset = input("Pilih preset: ", preset_option)
            
            if input_preset == "1" :
                waktu = 180
                heat_cap_value = 165
            elif input_preset == "2" :
                waktu = 900
                heat_cap_value = 289
            elif input_preset == "3" :
                waktu = 120
                heat_cap_value = 200
                
            #Pengambilan nilai dari array dimana data preset disimpan
            elif 3 < int(input_preset) < int(no_scan) :
                waktu = Saved_Presets[int(input_preset) - 4][1]
                level_value = Saved_Presets[int(input_preset) - 4][2]
                heat_cap_value = Saved_Presets[int(input_preset) - 4][3]
                
            # Fitur scan to cook
            elif input_preset == str(no_scan) :
                # Inisiasi awal di dalam loop
                kode_invalid = True
                
                # Penginputan kode dan pemastian panjang kode sesuai dengan format
                while kode_invalid == True :
                    kode_invalid = False
                    kode_full = input("Masukkan Kode: ")
                    
                    if len(kode_full) != 7 :
                        kode_invalid = True
                    else :
                        j, heat_cap_value, initialtemp, finaltemp, humid_value, mass_value, level_value, kode_invalid = scanToCook(kode_full)  #Penentuan nilai variabel untuk menghitung waktu pemanasan microwave berdasarkan kode
                        temp_difference = finaltemp - initialtemp

                    if kode_invalid == True :
                        print("Masukkan kode dengan format yang benar!")
                        
                #Rumus menghitung waktu dengan nilai variabel yang berdasarkan kode
                waktu_raw = (mass_value*(heat_cap_value/100) * temp_difference) * humid_value / (wattage_microwave * (level_value/100))

                #Pembulatan nilai waktu
                waktu_raw = math.ceil(waktu_raw)
        
        #Opsi enyimpanan input manual atau scan to cook ke dalam preset baru
        if input_preset == 0 or input_preset == no_scan :
            save_as_preset = inputOption("Apakah Anda ingin menyimpan pengaturan ini sebagai preset? (iya atau tidak):", iya_tidak)

            if save_as_preset == "iya" :
                input_invalid = True 
                
                #Penginputan nama preset baru
                while input_invalid == True :
                    input_invalid = False
                    nama_preset = input("Nama preset: ")
                    
                    if len(nama_preset) > 10 :
                        input_invalid = True
                        print("Nama terlalu panjang!")
                    
                Saved_Presets[current_taken_slot][0] = nama_preset              #Menyimpan nama di slot preset terbaru
                Saved_Presets[current_taken_slot][1] = waktu                    #Menyimpan waktu di slot preset terbaru
                Saved_Presets[current_taken_slot][2] = level_value              #Menyimpan persentase level microwave di slot preset terbaru
                Saved_Presets[current_taken_slot][3] = heat_cap_value           #Menyimpan kapasitas energi di slot preset terbaru
                print(f"Preset {Saved_Presets[current_taken_slot][0]} telah disimpan.")
                current_taken_slot += 1 
                        
    # Pengaktifan Eco Mode
    eco_mode = inputOption("Apakah anda ingin mengaktifkan Eco Mode ? (iya/tidak) : ", iya_tidak)
    
    if eco_mode == "iya" :
        # os.system("color a")
        print("ECO MODE AKTIF")
        eco_display = "ON "
        print(r"Saat ini anda menggunakan 50% dari daya pada microwave.")
        input("#Tekan tombol apapun untuk melanjutkan.")
        level_value *= 0.5
    elif eco_mode == "tidak" :
        print(r"Saat in anda menggunakan 100% dari daya pada microwave.")
        eco_display = "OFF"        
    
    #Penampilan preset custom di dalam tampilan microwave
    custom_preset = ["" for i in range(3)]
    panjang_cpreset = [0 for i in range(3)]    
    if current_taken_slot > 0:
        if current_taken_slot > 3:
            jumlah_pdisplay = 3
        else :
            jumlah_pdisplay = current_taken_slot
            
        for i in range(jumlah_pdisplay): 
            custom_preset[i] = f"{i + 4}. {Saved_Presets[i][0]}"
            panjang_cpreset[i] = len(custom_preset[i])
    
    for i in range(3) :
        for j in range(13 - panjang_cpreset[i]) :
            custom_preset[i] += " "
    
    
    #Penghitungan besar scroll bar berdasarkan banyaknya preset yang tersimpan
    if current_taken_slot > 3 :
        if ((current_taken_slot - 1) % 2) == 0 :
            jumlah_column = (current_taken_slot - 1)/2
        else :
            jumlah_column = (current_taken_slot)/2
        
        scroll_ratio = 3/(2 + jumlah_column) * 40
        if scroll_ratio % 1 != 0:
            scroll_ratio = scroll_ratio - (scroll_ratio % 1) + 1
    else :
        scroll_ratio = 40
    
    scroll_bar = ""
    for i in range(int(scroll_ratio)) :
        scroll_bar += "="
    for i in range(40 - int(scroll_ratio)) :
        scroll_bar += " "
    
    
    #Membaca massa menggunakan neraca internal microwave (Sebenarnya dilakukan secara otomatis, namun untuk di dalam kode sebagai input)
    input_invalid = True
    while input_invalid :
        input_invalid = False
        read_mass = int(input("Massa yang terbaca (gram): ")) 
        if read_mass <= 0 :
            input_invalid = True
            print("Massa harus lebih besar dari 0!")
        
    input("#Tekan tombol apapun untuk melanjutkan.")
    time.sleep(1)
    
    #Inisiasi sebelum masuk ke loop waktu microwave
    temp_predict = 25
    flash = True
    exit_operasi = False
    asap_terdeteksi = False

    while waktu >= 0 and timer_nyala : 
        
        #Perhitungan untuk prediksi suhu makanan/minuman di dalam microwave (Sebagai prediksi untuk kapan munculnya asap)
        #(Sebenarnya tidak termasuk kode microwave, tetapi untuk mensimulasikan alarm asap)
        if asap_terdeteksi ==  False :
            if ((wattage_microwave * level_value) - fan_efficiency)/(heat_cap_value/100 * read_mass) < 0.5 :
                temp_predict += ((wattage_microwave * level_value) - fan_efficiency)/(heat_cap_value/100 * read_mass) #Perhitungan suhu pemanasan microwave tiap detik
            else :
                temp_predict += 0.5
        else : 
            temp_predict -= (fan_efficiency)/(heat_cap_value/100 * read_mass) #Pendinginan microwave menggunakan kipas internal

        
        os.system("cls" if os.name == "nt" else "clear") #Membersihkan terminal output
            
        w_m = waktu // 60
        w_d = waktu % 60
        
        if w_m < 10 :
            w_m = f"0{w_m}"
        
        if w_d < 10 :
            w_d = f"0{w_d}"
        
        if asap_terdeteksi == False : 
            tampilan_waktu = f"        {w_m}:{w_d}   " #Menampilkan dalam bentuk 00:00 dimana menit dan detik
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
        
        print(f"""
    ______________________________________________________
    |                                                      |
    |   Smart Microwave                                    |
    |______________________________________________________|
    |                                                      |
    |   ________________________________________________   |
    |  |                                                |  |
    |  |  {tampilan_waktu}  [Scan to Cook]              |  |
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
    |   |   1. Popcorn    3. Preheat    {custom_preset[1]}  |   |
    |   |   2. Baking     {custom_preset[0]} {custom_preset[2]}  |   |
    |   |  <{scroll_bar}>  |   |
    |   |                                              |   |
    |   |  EcoMode[ {eco_display} ]                              |   |
    |   |______________________________________________|   |
    |______________________________________________________|
    """)
        if temp_predict > heat_cap_value * 0.5953125 and asap_terdeteksi == False: #Prediksi kapan terjadinya asap
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
        time.sleep(1)