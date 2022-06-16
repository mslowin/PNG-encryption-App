def print_png_data(content):
    j = 0
    for i in range(len(content)):
        print(content[i], end=" ")
        j += 1
        if j == 16:
            j = 0
            print()


def image_width(content):
    tmp = ''
    for e in range(16, 20):
        if len(content[e][2:]) < 2:
            tmp += '0' + content[e][2:]
        else:
            tmp += content[e][2:]
    print('Image width:\t\t\t\t', end=" "), print(int(tmp, 16))


def image_height(content):
    tmp = ''
    for e in range(20, 24):
        if len(content[e][2:]) < 2:
            tmp += '0' + content[e][2:]
        else:
            tmp += content[e][2:]
    print('Image width:\t\t\t\t', end=" "), print(int(tmp, 16))


def image_bit_depth(content):
    if len(content[24][2:]) < 2:
        tmp = '0' + content[24][2:]
    else:
        tmp = content[24][2:]
    print('Image bit depth:\t\t\t', end=" "), print(int(tmp, 16))


def image_colour_type(content):
    if len(content[25][2:]) < 2:
        tmp = '0' + content[25][2:]
    else:
        tmp = content[25][2:]
    print('Image colour type:\t\t\t', end=" "), print(int(tmp, 16))


def image_compression_method(content):
    if len(content[26][2:]) < 2:
        tmp = '0' + content[26][2:]
    else:
        tmp = content[26][2:]
    print('Image compression method:\t', end=" "), print(int(tmp, 16))


def image_filter_method(content):
    if len(content[27][2:]) < 2:
        tmp = '0' + content[27][2:]
    else:
        tmp = content[27][2:]
    print('Image filter method:\t\t', end=" "), print(int(tmp, 16))


def image_interlace_method(content):
    if len(content[28][2:]) < 2:
        tmp = '0' + content[28][2:]
    else:
        tmp = content[28][2:]
    print('Image interlace method:\t\t', end=" "), print(int(tmp, 16))


def show_ihdr_contents(content):
    print('Information from image header:')
    image_width(content)
    image_height(content)
    image_bit_depth(content)
    image_colour_type(content)
    image_compression_method(content)
    image_filter_method(content)
    image_interlace_method(content)
    print()


def print_ihdr_data(content, i):
    j = 0
    ihdr_length = content[i - 4][2:] + content[i - 3][2:] + content[i - 2][2:] + content[i - 1][2:]
    ihdr_length = int(ihdr_length, 16)
    print('IHDR chunk length: ', end=" "), print(ihdr_length, end=" "), print(' bytes')
    for a in range(ihdr_length + 4 + 4 + 4):  # metadata_length + 4 bytes length + 4 bytes name + 4 bytes CRC
        print(content[i - 4], end=" ")
        i += 1
        j += 1
        if j == 16:
            j = 0
            print()
    return ihdr_length


def print_idat_data(content, i):
    j = 0
    idat_length = content[i - 4][2:] + content[i - 3][2:] + content[i - 2][2:] + content[i - 1][2:]
    idat_length = int(idat_length, 16)
    print('IDAT chunk length: ', end=" "), print(idat_length, end=" "), print(' bytes')
    for a in range(idat_length + 4 + 4 + 4):  # metadata_length + 4 bytes length + 4 bytes name + 4 bytes CRC
        print(content[i - 4], end=" ")
        i += 1
        j += 1
        if j == 16:
            j = 0
            print()
    return idat_length


def print_plte_data(content, i):
    j = 0
    plte_length = content[i - 4][2:] + content[i - 3][2:] + content[i - 2][2:] + content[i - 1][2:]
    plte_length = int(plte_length, 16)
    print('PLTE chunk length: ', end=" "), print(plte_length, end=" "), print(' bytes')
    for a in range(plte_length + 4 + 4 + 4):  # metadata_length + 4 bytes length + 4 bytes name + 4 bytes CRC
        print(content[i - 4], end=" ")
        i += 1
        j += 1
        if j == 16:
            j = 0
            print()
    return plte_length


def print_iend_data(content, i):
    j = 0
    iend_length = content[i - 4][2:] + content[i - 3][2:] + content[i - 2][2:] + content[i - 1][2:]
    iend_length = int(iend_length, 16)
    print('IEND chunk length: ', end=" "), print(iend_length, end=" "), print(' bytes')
    for a in range(iend_length + 4 + 4 + 4):  # metadata_length + 4 bytes length + 4 bytes name + 4 bytes CRC
        print(content[i - 4], end=" ")
        i += 1
        j += 1
        if j == 16:
            j = 0
            print()
    return iend_length


def print_text_data(content, i):
    j = 0
    # read_text = ""
    text_length = content[i - 4][2:] + content[i - 3][2:] + content[i - 2][2:] + content[i - 1][2:]
    text_length = int(text_length, 16)

    text_begin = i + 4  # begining of text [length]i > [tEXt]here > [text][crc]
    text_end = i + 4 + text_length  # end of text [length][tEXt][text] < here[crc]
    text = ''
    print('tEXt chunk length: ', end=" "), print(text_length, end=" "), print(' bytes')
    for a in range(text_length + 4 + 4 + 4):  # metadata_length + 4 bytes length + 4 bytes name + 4 bytes CRC
        tmp = content[i][2:]
        if text_begin <= i < text_end:
            if content[i][2:] == '0':  # when its 0 bytes.fromhex(tmp).decode('utf-8') crashes
                text += ' '
            else:
                text += bytes.fromhex(tmp).decode('utf-8')  # converts hex to utf-8 characters
        print(content[i - 4], end=" ")
        i += 1
        j += 1
        if j == 16:
            j = 0
            print()
    print()
    print(text, end=" ")
    return text_length


def print_time_data(content, i):
    j = 0
    str_day = str_month = ' '
    year = hour = minute = second = 0
    time_marge_index = 0
    time_length = content[i - 4][2:] + content[i - 3][2:] + content[i - 2][2:] + content[i - 1][2:]
    time_length = int(time_length, 16)
    print('tIME chunk length: ', end=" "), print(time_length, end=" "), print(' bytes')
    for a in range(time_length + 4 + 4 + 4):  # metadata_length + 4 bytes length + 4 bytes name + 4 bytes CRC
        print(content[i - 4], end=" ")
        i += 1
        j += 1
        time_marge_index += 1
        if time_marge_index == 8:  # after 4 bytes of length and 4 bytes of tIME name
            year = int(str(content[i - 4][2:] + content[i - 3][2:]), 16)
            month = int(str(content[i - 2][2:]), 16)
            if month < 10:
                str_month = '0' + str(month)
            else:
                str_month = str(month)
            day = int(str(content[i - 1][2:]), 16)
            if day < 10:
                str_day = '0' + str(day)
            else:
                str_day = str(day)
            hour = int(str(content[i][2:]), 16)
            minute = int(str(content[i + 1][2:]), 16)
            second = int(str(content[i + 2][2:]), 16)
        if j == 16:
            j = 0
            print()
    print(), print('Data extracted from tIME:')
    print('Last image modification:', end=" ")
    print(str_day, end="."), print(str_month, end=".")
    print(year, end=" "), print(hour, end=":")
    print(minute, end=":"), print(second, end=" ")
    return time_length


def save_critical_chunk_to_tmp(content, start, end):
    tmp = ''
    for e in range(start, end):
        if len(content[e][2:]) < 2:         # important for writing to a file and changing text to hex
            tmp += '0' + content[e][2:]
        else:
            tmp += content[e][2:]
    return tmp


def extract_image_info(content):
    tmp = ''
    for e in range(0, 8):
        if len(content[e][2:]) < 2:         # important for writing to a file and changing text to hex
            tmp += '0' + content[e][2:]
        else:
            tmp += content[e][2:]
    return tmp


def print_gama_data(content, i):
    j = 0
    gama_length = content[i - 4][2:] + content[i - 3][2:] + content[i - 2][2:] + content[i - 1][2:]
    gama_length = int(gama_length, 16)
    gama = content[i + 4][2:] + content[i + 5][2:] + content[i + 6][2:] + content[i + 7][2:]
    gama = int(gama, 16)
    gama = gama / 100000
    print("Gamma value: ", end=" "), print(gama)
    print('gAMA chunk length: ', end=" "), print(gama_length, end=" "), print(' bytes')
    for a in range(gama_length + 4 + 4 + 4):  # metadata_length + 4 bytes length + 4 bytes name + 4 bytes CRC
        print(content[i - 4], end=" ")
        i += 1
        j += 1
        if j == 16:
            j = 0
            print()
    return gama_length


def print_chrm_data(content, i):
    j = 0
    chrm_length = content[i - 4][2:] + content[i - 3][2:] + content[i - 2][2:] + content[i - 1][2:]
    chrm_length = int(chrm_length, 16)
    chrm_chunks = ["White point x", "White point y", "Red x", "Red y", "Green x", "Green y", "Blue x", "Blue y"]
    it = 4

    for x in chrm_chunks:
        value = content[i + it][2:] + content[i + it + 1][2:] + content[i + it + 2][2:] + content[i + it + 3][2:]
        value = int(value, 16)
        value = value / 100000
        print(x, end=" "), print("=", end=" "), print(value)
        it = it + 4

    print('cHRM chunk length: ', end=" "), print(chrm_length, end=" "), print(' bytes')
    for a in range(chrm_length + 4 + 4 + 4):  # metadata_length + 4 bytes length + 4 bytes name + 4 bytes CRC
        print(content[i - 4], end=" ")
        i += 1
        j += 1
        if j == 16:
            j = 0
            print()
    return chrm_length


def print_phys_data(content, i):
    j = 0
    phys_length = content[i - 4][2:] + content[i - 3][2:] + content[i - 2][2:] + content[i - 1][2:]
    phys_length = int(phys_length, 16)
    phys_chunks = ['Pixels per unit X', 'Pixels per unit Y']
    it = 4

    for x in phys_chunks:
        value = content[i + it][2:] + content[i + it + 1][2:] + content[i + it + 2][2:] + content[i + it + 3][2:]
        value = int(value, 16)
        print(x, end=" "), print("=", end=" "), print(value)
        it = it + 4
    unit_specifier = int(content[i + it], 16)
    if  unit_specifier == 1:
        print("Per meter")
    else:
        print("No unit specified!")
    print('pHYs chunk length: ', end=" "), print(phys_length, end=" "), print(' bytes')
    for a in range(phys_length + 4 + 4 + 4):  # metadata_length + 4 bytes length + 4 bytes name + 4 bytes CRC
        print(content[i - 4], end=" ")
        i += 1
        j += 1
        if j == 16:
            j = 0
            print()
    return phys_length

def print_bkgd_data(content, i):
    j = 0
    bkgd_length = content[i - 4][2:] + content[i - 3][2:] + content[i - 2][2:] + content[i - 1][2:]
    bkgd_length = int(bkgd_length, 16)
    if bkgd_length == 2:
        colour = content[i + 4] + content[i + 5][2:]
    else:
        if bkgd_length == 1:
            colour = content[i + 4]
        else:
            x = content[i + 4] + content[i + 5][2:]
            y = content[i + 4] + content[i + 5][2:]
            z = content[i + 4] + content[i + 5][2:]
            colour = "X:" + x + " Y:" + y + " Z:" + z

    print("Background colour: ", end=" "), print(colour)
    print('bKGD chunk length: ', end=" "), print(bkgd_length, end=" "), print(' bytes')
    for a in range(bkgd_length + 4 + 4 + 4):  # metadata_length + 4 bytes length + 4 bytes name + 4 bytes CRC
        print(content[i - 4], end=" ")
        i += 1
        j += 1
        if j == 16:
            j = 0
            print()
    return bkgd_length
