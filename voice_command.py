# input microwave berbasis suara 

masukan_suara = input("Berikan perintah suara : ")
masukan_suara.lower()
list_masukan_suara = [i for i in masukan_suara]
# cari berapa banyak kata yang terdapat dalam masukan_suara dengan jumalh spasi +1
jumlah_kata = 0
if list_masukan_suara[0] != ' ':
        jumlah_kata += 1
for i in list_masukan_suara :
    if i == ' ':
        jumlah_kata += 1
# CATATAN : JANGAN MENAMBAHKAN SPASI DI AKHIR KALIMAT

kata_masukan_suara = ['*' for i in range(jumlah_kata)]
penyimpan_kata = ''
index = 0
for c in masukan_suara:
    if c == ' ':
        kata_masukan_suara[index] = penyimpan_kata
        penyimpan_kata = ''
        index += 1
    else:
        penyimpan_kata += c

if penyimpan_kata:
    kata_masukan_suara[jumlah_kata-1] = penyimpan_kata

# varaiabel menyimpan nilai
waktu_menit = 0
waktu_detik = 0
keluaran = []

# Cocokkan dengan kata kunci 
if kata_masukan_suara[0] == "microwave": 
    for i in range(len(kata_masukan_suara)) :
        if kata_masukan_suara[i] == "daging" :
            keluaran.append("Food M")
        elif kata_masukan_suara[i] == "sayuran" :
            keluaran.append("Food v")
        elif kata_masukan_suara[i] == "pasta" :
            keluaran.append("Food P")
        elif kata_masukan_suara[i] == "beras":
            keluaran.append("Food R")
        elif kata_masukan_suara[i] == "susu":
            keluaran.append("Drink M")    
        elif kata_masukan_suara[i] == "air":
            keluaran.append("Drink A")
        elif kata_masukan_suara[i] == "kopi":
            keluaran.append("Drink C")
        elif kata_masukan_suara[i] == "sup":
            keluaran.append("Drink S")
        elif kata_masukan_suara [i] == "menit":
            waktu_menit = kata_masukan_suara[i-1]
        elif kata_masukan_suara [i] == "detik":
            waktu_detik = kata_masukan_suara[i-1]
        elif kata_masukan_suara[i] == "popcorn":
            waktu_menit = 30
        elif kata_masukan_suara[i] == "baking":
            waktu_menit = 15
        elif kata_masukan_suara[i] == "preheat":
            waktu_menit == 2
            
            
for i in keluaran :
    print(i, end="\n") 
print(str(waktu_menit)+":"+str(waktu_detik))  
            