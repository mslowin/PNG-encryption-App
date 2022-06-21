import numpy as np
# import sys
import binascii
import png_operations as png
import matplotlib.pyplot as plt
from PIL import Image
from skimage.io import imread

#  import cv2

idat_tmp_start = []
idat_tmp_end = []

IHDR_hex = '0x490x480x440x52'
PLTE_hex = '0x500x4c0x540x45'
IDAT_hex = '0x490x440x410x54'
IEND_hex = '0x490x450x4e0x44'

tEXt_hex = '0x740x450x580x74'
tIME_hex = '0x740x490x4d0x45'
gAMA_hex = '0x670x410x4d0x41'
cHRM_hex = '0x630x480x520x4d'
pHYs_hex = '0x700x480x590x73'
bKGD_hex = '0x620x4b0x470x44'

image = Image.open('.\\PNG_images\\icon.png')  # image to read data from
# image.show()

file_path = '.\\PNG_images\\icon.png'

with open(file_path, 'rb') as file:
    content = [hex(a) for a in file.read()]

# png.print_png_data(content)


i = 0
x = 0
flag = 0
idat_start = []
idat_end = []
idat_data = ""
critical_chunks_space = 0
tmp = ''
tmp_RSA = ''
tmp_encrypted = ''

text_length = 'brak tekstu'
image_info = png.extract_image_info(content)

for i in range(len(content) - 3):
    # print((str(content[i]) + str(content[i + 1]) + str(content[i + 2]) + str(content[i + 3])))
    if (str(content[i]) + str(content[i + 1]) + str(content[i + 2]) + str(content[i + 3])) == IHDR_hex:
        print()
        png.show_ihdr_contents(content)
        ihdr_length = png.print_ihdr_data(content, i)
        ihdr_start = 8
        ihdr_end = ihdr_start + 4 + 4 + ihdr_length + 4
        critical_chunks_space += (ihdr_end - ihdr_start)
        tmp = png.save_critical_chunk_to_tmp(content, ihdr_start, ihdr_end)
        tmp_RSA += png.save_critical_chunk_to_tmp(content, ihdr_start, ihdr_end)
        tmp_encrypted += png.save_critical_chunk_to_tmp(content, ihdr_start, ihdr_end)
        print()
    if (str(content[i]) + str(content[i + 1]) + str(content[i + 2]) + str(content[i + 3])) == PLTE_hex:
        print()
        plte_length = png.print_plte_data(content, i)
        plte_start = i - 4
        plte_end = plte_start + 4 + 4 + plte_length + 4
        critical_chunks_space += (plte_end - plte_start)
        tmp += png.save_critical_chunk_to_tmp(content, plte_start, plte_end)
        tmp_RSA += png.save_critical_chunk_to_tmp(content, plte_start, plte_end)
        tmp_encrypted += png.save_critical_chunk_to_tmp(content, plte_start, plte_end)
        print()
    if (str(content[i]) + str(content[i + 1]) + str(content[i + 2]) + str(content[i + 3])) == IDAT_hex:
        print()
        tmp_i = i
        idat_length = png.print_idat_data(content, i)
        # print(idat_length)
        idat_start.append(i - 4)
        idat_end.append(idat_start[x] + 4 + 4 + idat_length + 4)
        critical_chunks_space += (idat_end[x] - idat_start[x])
        idat_tmp_start.append(len(tmp))
        idat_tmp_end.append(len(tmp) + idat_length)
        tmp += png.save_critical_chunk_to_tmp(content, idat_start[x], idat_end[x])
        idat_data += png.save_critical_chunk_to_tmp(content, idat_start[x], idat_end[x])

        begining = idat_data[0:16:1]
        ending = idat_data[len(idat_data)-8:]

        idat_data = idat_data[16:len(idat_data) - 8:1]
        # ---------------------------------------------
        e, d, n = png.rsa_generate_keys()
        # pubKeyPEM, privKeyPEM, pubKey = png.rsa_algorithm_generate_keys()
        # msg = png.rsa_encryption("test1321", e, n)
        # Dmsg = png.rsa_decryption(msg, d, n)
        cyphered_msg = ""

        bit_num = 50
        # print(len(idat_data))
        idat_data_len = len(idat_data)
        pom = ''
        counter = 0
        for i in range(1, idat_data_len):

            if idat_data_len - counter * bit_num < bit_num:  # jesli zostalo cos na koncu dodaj zera
                pom = ''

                t = idat_data_len - counter * bit_num

                for j in range(0, bit_num - t):
                    pom += '0'
                pom += idat_data[i - 1:idat_data_len:1]
                tmp_cos = png.rsa_encryption(pom, e, n)
                pom = str(tmp_cos)
                if len(str(tmp_cos)) < len(str(n)):
                    pom = ''
                    for j in range(0, len(str(n)) - len(str(tmp_cos))):
                        pom += '0'
                    pom += str(tmp_cos)
                    # print(pom)
                cyphered_msg += pom  # enkrypcja wiadomosci i dodanie jej do stringa
                decrypted_text = png.rsa_decryption(int(pom), d, n)
                counter = counter + 1
                break

            if i % bit_num == 0:
                pom = idat_data[i - bit_num:i:1]  # jesli podzielne przez 50, zrob substring
                tmp_cos = png.rsa_encryption(pom, e, n)
                pom = str(tmp_cos)
                if len(str(tmp_cos)) < len(str(n)):
                    pom = ''
                    for j in range(0, len(str(n)) - len(str(tmp_cos))):
                        pom += '0'
                    pom += str(tmp_cos)

                decrypted_text = png.rsa_decryption(int(pom), d, n)
                cyphered_msg += pom  # enkrypcja wiadomosci i dodanie jej do stringa
                # print(png.rsa_decryption(tmp_cos, d, n))

                counter = counter + 1

        idat2 = ''
        i = 0
        while i < len(cyphered_msg):
            t = i + len(str(n))
            crypted_tmp = cyphered_msg[i:t:1]
            decrypted_text = png.rsa_decryption(int(crypted_tmp), d, n)
            i = i + len(str(n))
            if i == len(cyphered_msg):
                decrypted_text = decrypted_text[bit_num - ((idat_length * 2) % bit_num):]
            idat2 += decrypted_text
        # print("sdjsdfsdsf")
        # print(idat2)
        # ---------------------------------------------

        # print(len(cyphered_msg))
        begining_encrypted = str(hex(len(cyphered_msg)))[2:]
        begining_encrypted = begining_encrypted.zfill(8)
        begining_encrypted = begining_encrypted + '49444154'
        tmp_RSA += begining + idat2 + ending
        # tmp_encrypted += begining_encrypted + str(hex(int(cyphered_msg))) + ending
        if len(cyphered_msg) % 2 != 0:
            cyphered_msg = '0' + cyphered_msg
        tmp_encrypted += begining_encrypted + cyphered_msg + ending
        i = tmp_i
        x += 1

    if (str(content[i]) + str(content[i + 1]) + str(content[i + 2]) + str(content[i + 3])) == IEND_hex:
        print()
        iend_length = png.print_iend_data(content, i)
        iend_start = i - 4
        iend_end = iend_start + 4 + 4 + iend_length + 4
        critical_chunks_space += (iend_end - iend_start)
        tmp += png.save_critical_chunk_to_tmp(content, iend_start, iend_end)
        tmp_RSA += png.save_critical_chunk_to_tmp(content, iend_start, iend_end)
        tmp_encrypted += png.save_critical_chunk_to_tmp(content, iend_start, iend_end)
    # # ancillary chunks:
    if (str(content[i]) + str(content[i + 1]) + str(content[i + 2]) + str(content[i + 3])) == tEXt_hex:
        print()
        text_length = png.print_text_data(content, i)
        text_start = i - 4
        text_end = text_start + 4 + 4 + text_length + 4
        print()
    if (str(content[i]) + str(content[i + 1]) + str(content[i + 2]) + str(content[i + 3])) == tIME_hex:
        print()
        time_length = png.print_time_data(content, i)
        time_start = i - 4
        time_end = time_start + 4 + 4 + time_length + 4
        print()
    if (str(content[i]) + str(content[i + 1]) + str(content[i + 2]) + str(content[i + 3])) == gAMA_hex:
        print()
        gama_start = i - 4
        gama_length = png.print_gama_data(content, i)
        gama_end = gama_start + 4 + 4 + gama_length + 4
        print()
    if (str(content[i]) + str(content[i + 1]) + str(content[i + 2]) + str(content[i + 3])) == cHRM_hex:
        print()
        cHRM_start = i - 4
        cHRM_length = png.print_chrm_data(content, i)
        cHRM_end = cHRM_start + 4 + 4 + cHRM_length + 4
        print()
    if (str(content[i]) + str(content[i + 1]) + str(content[i + 2]) + str(content[i + 3])) == pHYs_hex:
        print()
        pHYS_start = i - 4
        pHYs_length = png.print_phys_data(content, i)
        pHys_end = pHYS_start + 4 + 4 + pHYs_length + 4
        print()
    if (str(content[i]) + str(content[i + 1]) + str(content[i + 2]) + str(content[i + 3])) == bKGD_hex:
        print()
        bKGD_start = i - 4
        bKGD_length = png.print_bkgd_data(content, i)
        bKGD_end = bKGD_start + 4 + 4 + bKGD_length + 4
        print()

file.close()

# tmp_begin = tmp[0:idat_tmp_start[0]]
# tmp_end = tmp[idat_tmp_end[0]:len(tmp)]
# tmp2 = tmp_begin + idat2 + tmp_end
#


#  tu powinien byc string z calym idatem zaszyfrowanym, potem trzeba go podzielic na czesci o wielkosci
#  zwracanej przez png.rsa_encryption(pom, e, n) to gowno i odszyfrowac

# putting together whole PNG file data, (first 8 bytes of png file which are always the same + the rest of the file):
tmp = image_info + tmp
tmp = tmp.strip()
tmp = tmp.replace(' ', '')  # getting rid of all unnecessary spaces and end of lines
tmp = tmp.replace('\n', '')
tmp = binascii.a2b_hex(tmp)  # changing hex data to binascii
with open('.\\PNG_images\\icon-po-anonimizacji.png', 'wb') as file2:  # creation of a new file in which w put tmp data
    file2.write(tmp)

file2.close()


# saving decrypted data to a file
tmp_RSA = image_info + tmp_RSA
tmp_RSA = tmp_RSA.strip()
tmp_RSA = tmp_RSA.replace(' ', '')  # getting rid of all unnecessary spaces and end of lines
tmp_RSA = tmp_RSA.replace('\n', '')
tmp_RSA = binascii.a2b_hex(tmp_RSA)  # changing hex data to binascii
# print(tmp_RSA)
with open('.\\PNG_images\\icon-po-decrypted.png', 'wb') as file3:  # creation of a new file in which w put tmp data
    file3.write(tmp_RSA)

file3.close()


# saving encrypted data to a file
tmp_encrypted = image_info + tmp_encrypted
tmp_encrypted = tmp_encrypted.strip()
tmp_encrypted = tmp_encrypted.replace(' ', '')  # getting rid of all unnecessary spaces and end of lines
tmp_encrypted = tmp_encrypted.replace('\n', '')
tmp_encrypted = binascii.a2b_hex(tmp_encrypted)  # changing hex data to binascii
with open('.\\PNG_images\\icon-po-encrypted.png', 'wb') as file4:  # creation of a new file in which w put tmp data
    file4.write(tmp_encrypted)

file4.close()

print()
# print(tmp_encrypted)

# # png_operations.print_png_data(content)
#
# image2 = imread('.\\PNG_images\\ball.png')  # image to be transformed
#
# plt.figure()
# plt.imshow(image2, cmap='gray')  # displaying original image
#
# image2_fourier = np.fft.fftshift(np.fft.fft2(image2))
# out = np.log(abs(image2_fourier))
#
# # Phase of a transformed image
# imgFloat32 = np.float32(image2)  # Convert image to float32
# dft = cv2.dft(imgFloat32, flags=cv2.DFT_COMPLEX_OUTPUT)  # Fourier transform
# dftShift = np.fft.fftshift(dft)  # Move the low frequency component to the center of the frequency domain image
# dftAmp = cv2.magnitude(dft[:, :, 0], dft[:, :, 1])  # Amplitude spectrum, decentralized
# phase = np.arctan2(dftShift[:, :, 1], dftShift[:, :, 0])  # Calculated phase angle (radian system)
# dftPhi = phase / np.pi * 180  # Convert phase angle to [- 180, 180]
#
# plt.figure(figsize=(9, 6))
# plt.title("DFT Phase"), plt.axis('off')
# plt.imshow(dftPhi)
#
# plt.figure()
# plt.imshow(out, cmap='gray')  # displaying image after fourier transform
# plt.show()