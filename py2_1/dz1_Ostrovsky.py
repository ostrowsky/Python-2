#1.	Записать строку символов в текстовый файл и вывести содержимое файла.
chr_str = input("Введите строку символов для записи в текстовый файл \n")
if not chr_str:
    chr_str = "Строка символов для записи в текстовый файл"
    print(chr_str)
txt_file = open("file1.txt", "w")
txt_file.write(chr_str)
txt_file.close()
txt_file = open("file1.txt", "r")
file_chr_str = txt_file.read()
print(file_chr_str)
txt_file.close()
print("\n")

#2.	Записать строку символов в файл, с явным указанием кодировки utf-8, вывести содержимое файла.
chr_str_utf = input("Введите строку символов для записи с кодировкой utf-8\n")
if not chr_str_utf:
    chr_str_utf = "Строка символов для записи с кодировкой utf-8"
    print(chr_str_utf)
txt_file_utf = open("file2.txt", "w", encoding="utf-8")
txt_file_utf.write(chr_str_utf)
txt_file_utf.close()
txt_file_utf = open("file2.txt", "r")
file_chr_str_utf = txt_file_utf.read()
print(file_chr_str_utf)
txt_file_utf.close()

print("\n")
#3.	Декодировать содержимое файла из предыдущего задания.
txt_file_utf = open("file2.txt", "r", encoding='utf-8')
file_chr_str_utf = txt_file_utf.read()
print(file_chr_str_utf)
txt_file_utf.close()
print("\n")

#4.	Записать строку символов в двоичный файл и вывести содержимое файла.
chr_str_bin = input("Введите строку символов для записи в двоичный файл \n", )
if not chr_str_bin:
    chr_str_bin = "Строка символов для записи в двоичный файл"
    print(chr_str_bin)
txt_file_bin = open("file3.txt", "wb")
txt_file_bin.write(bytes(chr_str_bin,'utf-8'))
txt_file_bin.close()
txt_file_bin = open("file3.txt", "rb")
file_bin_str = txt_file_bin.read()
print(file_bin_str)
txt_file_bin.close()
print("\n")

#5.	Записать строку символов в файл, с явным указанием кодировки latin-1, вывести содержимое файла.
chr_str_lat = input("Введите строку символов для записи в двоичный файл с кодировкой latin-1 \n", )
if not chr_str_lat:
    chr_str_lat = "Zeichenfolge in eine Binärdatei codiert latin-1 zu schreiben"
    print(chr_str_lat)

txt_file_lat = open("file4.txt", "wb")
txt_file_lat.write(bytes(chr_str_lat,'latin-1'))
txt_file_lat.close()
txt_file_lat = open("file4.txt", "rb")
file_bin_str = txt_file_lat.read()
print(file_bin_str)
txt_file_lat.close()
print("\n")
#6.	Декодировать содержимое файла из предыдущего задания.
print(file_bin_str.decode(encoding='latin-1'))

#7.	*Определить, какой из jpg-файлов был создан раньше всех.

import exifread
def define_earliest_jpg(*args):
    earliest_jpg = ''
    for i in args:
        jpg_file = open(i, 'rb')
        tags = exifread.process_file(jpg_file)
        print(tags)
        for tag in tags.keys():
            print(tag, tags[tag])

        curr_date = tags["Image DateTime"]
        if cur_date < earliest_jpg:
            earliest_jpg = i
    print(earliest_jpg)

define_earliest_jpg("img7.jpg", "img8.jpg", "img9.jpg")

