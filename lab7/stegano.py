# autor Sebastian Jabłoński 285810
import sys

LEN_MAXIMUM = 64
def e1():
    lines = open('cover.html', 'r').readlines()
    msg = open('mess.txt', 'r').read().strip()
    helper = ''
    for num in msg:
        binary = bin(int(num, 16))[2:].zfill(4)
        helper += binary
    if len(helper) > len(lines):
        raise Exception("Za mały nośnik żeby przekazac wiadomość.")
    new_cover_lines = ""
    for i, bit in enumerate(helper):
        stripped_line = lines[i].replace('\n', '')
        if bit == '1':
            stripped_line += ' ' + '\n'
        else:
            stripped_line += '\n'
        new_cover_lines += stripped_line
    new_cover_lines += "".join(lines[LEN_MAXIMUM:-1])
    with open('watermark.html', 'w+') as f:
        f.write(new_cover_lines)


def e2():
    with open("mess.txt", "r", encoding="utf-8") as f:
        msg = f.read().strip()
    with open("cover.html", "r", encoding="utf-8") as cover_file:
        cover = cover_file.readlines()
    b_msg = ""
    for x in msg:
        binary = bin(int(x, 16))[2:].zfill(4)
        b_msg += binary
    cover = "".join(cover).replace("  ", "")
    spc_counter = cover.count(" ")
    if len(b_msg) > spc_counter:
        raise Exception("Za mały nośnik żeby przekazac wiadomość.")
    watermark = ""
    cover = cover.split(" ")
    for i in range(len(b_msg)):
        bit = b_msg[i]
        if bit == "1":
            cover[i] += " "
        watermark += cover[i] + " "
    watermark += " ".join(cover[len(b_msg):])
    with open("watermark.html", "w+", encoding="utf-8") as f:
        f.writelines(watermark)

def e3():
    with open("mess.txt", "r", encoding="utf-8") as f:
        msg = f.read().strip()

    with open("cover.html", "r", encoding="utf-8") as cover_file:
        cover = cover_file.readlines()

    b_msg = ""
    for x in msg:
        binary = bin(int(x, 16))[2:].zfill(4)
        b_msg += binary

    if len(b_msg) > len(cover):
        raise Exception("Za mały nośnik żeby przekazac wiadomość.")

    watermark = ""
    i = 0
    for line in cover:
        watermark_line = line
        if "style" in line:
            if len(b_msg) > i and b_msg[i] == "1":
                watermark_line = line.replace('flex', 'fleks')
            else:
                pass
            watermark += watermark_line
            i += 1
        else:
            watermark += watermark_line

    with open("watermark.html", "w+", encoding="utf-8") as f:
        f.writelines(watermark)


def e4():
    with open("mess.txt", "r", encoding="utf-8") as f:
        msg = f.read().strip()

    with open("cover.html", "r", encoding="utf-8") as cover_file:
        cover = cover_file.readlines()

    cover = [x.replace("<p></p>", "") for x in cover]

    num_fonts = "".join(cover).count("<p>")

    b_msg = ""
    for x in msg:
        binary = bin(int(x, 16))[2:].zfill(4)
        b_msg += binary
    if len(b_msg) > num_fonts:
        raise Exception("Za mały nośnik żeby przekazac wiadomość.")

    watermark = ""
    i = 0
    for line in cover:
        watermark_line = line
        if "<p>" in line:
            if len(b_msg) > i and b_msg[i] == "1":
                watermark_line = line.replace("<p>", "<p></p><p>")
            else:
                watermark_line = line.replace("</p>", "</p><p></p>")
            watermark += watermark_line
            i += 1
        else:
            watermark += watermark_line

    with open("watermark.html", "w+", encoding="utf-8") as f:
        f.write(watermark)


def d1():
    watermark = open('watermark.html').readlines()
    msg = ''
    for line in watermark:
        helper = line.replace('\n', '')
        if helper[-1] == ' ':
            msg += '1'
        else:
            msg += '0'
        if len(msg) == LEN_MAXIMUM:
            break
    h_msg = ''
    for i in range(0, len(msg), 4):
        h_number = hex(int(msg[i:i + 4], 2))[2:].upper()
        h_msg += h_number
    with open('detect.txt', 'w+') as f:
        f.write(h_msg.upper())


def d2():
    with open("watermark.html", "r", encoding="utf-8") as f:
        watermark = f.readlines()
    msg = ""
    watermark = "".join(watermark).split(" ")
    for i in range(len(watermark)):
        if watermark[i] == "":
            msg += "1"
        else:
            msg += "0"
    msg = msg.replace("01", "1")[:LEN_MAXIMUM]
    h_msg = ""
    for i in range(0, len(msg), 4):
        h_msg += hex(int(msg[i:i + 4], 2))[2:]
    with open("detect.txt", "w+") as f:
        f.write(h_msg.upper())



def d3():
    with open("watermark.html", "r", encoding="utf-8") as f:
        watermark = f.readlines()

    message = ""
    for line in watermark:
        if "flex" in line:
            message += "0"
        elif 'fleks' in line:
            message += "1"
        else:
            pass
        if len(message) == LEN_MAXIMUM:
            break

    hex_message = ""
    for i in range(0, len(message), 4):
        hex_message += hex(int(message[i: i + 4], 2))[2:]

    with open("detect.txt", "w+", encoding="utf-8") as f:
        f.write(hex_message.upper())


def d4():

    with open("watermark.html", "r", encoding="utf-8") as f:
        watermark = f.readlines()

    msg = ""
    for i in watermark:
        if "<p></p><p>" in i:
            msg += "1"
        if "</p><p></p>" in i:
            msg += "0"
        if len(msg) == LEN_MAXIMUM:
            break

    h_msg = ""
    for i in range(0, len(msg), 4):
        h_msg += hex(int(msg[i: i + 4], 2))[2:]

    with open("detect.txt", "w+", encoding="utf-8") as f:
        f.write(h_msg.upper())


result = ""
with open("cover.html", "r+") as file:
    for line in file:
        if not line.isspace():
            result += line

    file.seek(0)
    file.write(result)

if sys.argv[1] == "-d":
    if sys.argv[2] == "-1":
        d1()
    elif sys.argv[2] == "-2":
        d2()
    elif sys.argv[2] == "-3":
        d3()
    elif sys.argv[2] == "-4":
        d4()
elif sys.argv[1] == "-e":
    if sys.argv[2] == "-1":
        e1()
    elif sys.argv[2] == "-2":
        e2()
    elif sys.argv[2] == "-3":
        e3()
    elif sys.argv[2] == "-4":
        e4()