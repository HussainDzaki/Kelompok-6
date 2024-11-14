# mode hemat daya dan konservasi energi
eco_mode = input("Apakah anda ingin mengaktifkan Eco Mode ? (ya/tidak) : ")
eco_mode.lower()
ulang = True
while ulang :
    if eco_mode == "ya" :
        print("Saat ini anda menggunakan 50% dari daya pada microwave.")
        ulang = False
    elif eco_mode == "tidak" :
        print("Saat in anda menggunakan 100% dari daya pada microwave.")
        ulang = True
    else :
        print("Masukkkan pilihan dengan benar, ketik antara 'ya' atau 'tidak'")
        eco_mode = input("Apakah anda ingin mengaktifkan Eco Mode ? (ya/tidak) : ")
        eco_mode.lower()   