# autor Sebastian Jabłoński
import sys
import math


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
    
def add_to_file(filename, content):
            with open(filename, 'a') as file:
                file.write(content)

def cezar_encrypt(plain, key):
    code = ""
    key_safe = key % 26
    for i in range(len(plain)):
            if plain[i] == " ":
                code += " "
            elif plain[i].islower():
                char = chr((ord(plain[i]) + key_safe - 97) % 26 + 97)
                code += char
            else:
                char = chr((ord(plain[i]) + key_safe - 65) % 26 + 65)
                code += char
    write_file('crypto.txt', code)
    write_file('extra.txt', plain[0] + '\n')

def cezar_decrypt(crypto, key):
    code = ""
    key_safe = key % 26
    for i in range(len(crypto)):
        if crypto[i] == " ":
            code += " "
        elif crypto[i].islower():
            char = chr((ord(crypto[i]) - key_safe - 97) % 26 + 97)
            code += char
        else:
            char = chr((ord(crypto[i]) - key_safe - 65) % 26 + 65)
            code += char
    write_file('decrypt.txt', code)
    
def kryptoanaliza_sam(crypto):
    for i in range(26):
        code = ''
        for j in range(len(crypto)):
            if crypto[j] == " ":
                code += " "
            elif crypto[j].islower():
                char = chr((ord(crypto[j]) - i - 97) % 26 + 97)
                code += char
            else:
                char = chr((ord(crypto[j]) - i - 65) % 26 + 65)
                code += char
        add_to_file('extra.txt', code + '\n')
        
def kryptoanaliza_pomoc(crypto, key):
    shift = ord(crypto[0]) - ord(key[0]) 
    code = ""
    for i in range(len(crypto)):
        if crypto[i] == " ":
            code += " "
        elif crypto[i].islower():
            char = chr((ord(crypto[i]) - shift - 97) % 26 + 97)
            code += char
        else:
            char = chr((ord(crypto[i]) - shift - 65) % 26 + 65)
            code += char
    write_file('decrypt.txt', code + " " + str(shift) + '\n')
    write_file('key-new.txt', str(shift) + '\n')

def afiniczny_encrypt(plain, a, b):
    print(a,b)
    if math.gcd(a, 26) != 1:
        print(f"{a} i 26 nie są wzglednie pierwsze")
        sys.exit(1)
    if (a * pow(a, -1, 26)) % 26 != 1:
        print(f"Iloczyn {a} i jego odwrotnosc modulo 26 nie dają wyniku 1. (Oznacza to ze a nie moze byc kluczen do szyfrowania)")
        sys.exit(1)
    code = ""
    for i in range(len(plain)):
        if plain[i] == " ":
            code += " "
        elif plain[i].islower():
            char = chr((a * (ord(plain[i]) - 97) + b) % 26 + 97)
            code += char
        else:
            char = chr((a * (ord(plain[i]) - 65) + b) % 26 + 65)
            code += char
    write_file('crypto.txt', code)
    write_file('extra.txt', plain[0] + plain[1] + '\n')

def afiniczny_decrypt(crypto, a, b):
    if math.gcd(a, 26) != 1:
        print(f"{a} i 26 nie są wzglednie pierwsze")
        sys.exit(1)
    if (a * pow(a, -1, 26)) % 26 != 1:
        print(f"Iloczyn {a} i jego odwrotnosc modulo 26 nie dają wyniku 1. (Oznacza to ze a nie moze byc kluczen do szyfrowania)")
        sys.exit(1)
    code = ""
    a_inverse = 0
    for i in range(26):
        if (a * i) % 26 == 1:
            a_inverse = i
            break
    for i in range(len(crypto)):
        if crypto[i] == " ":
            code += " "
        elif crypto[i].islower():
            char = chr((a_inverse * (ord(crypto[i]) - 97 - b)) % 26 + 97)
            code += char
        else:
            char = chr((a_inverse * (ord(crypto[i]) - 65 - b)) % 26 + 65)
            code += char
    write_file('decrypt.txt', code)

def kryptoanaliza_afiniczny_sam(crypto):
    for a in range(26):
        if math.gcd(a, 26) == 1:
            for b in range(26):
                code = ''
                for k in range(len(crypto)):
                    if crypto[k] == " ":
                        code += " "
                    elif crypto[k].islower():
                        char = chr((a * (ord(crypto[k]) - 97) + b) % 26 + 97)
                        code += char
                    else:
                        char = chr((a * (ord(crypto[k]) - 65) + b) % 26 + 65)
                        code += char
                add_to_file('extra.txt', code + '\n')

def kryptoanaliza_afiniczny_pomoc(crypto, key_a, key_b):
    x1, x2 = ord(key_a.lower()) - 97, ord(key_b.lower()) - 97
    y1, y2 = ord(crypto[0].lower()) - 97, ord(crypto[1].lower()) - 97

    for a in range(26):
        for b in range(26):
            if (a * x1 + b) % 26 == y1 and (a * x2 + b) % 26 == y2:
                decrypted = ""
                a_inv = pow(a, -1, 26)
                for char in crypto:
                    if char.isalpha():
                        if char.islower():
                            decrypted += chr((a_inv * (ord(char) - 97 - b)) % 26 + 97)
                        else:
                            decrypted += chr((a_inv * (ord(char) - 65 - b)) % 26 + 65)
                    else:
                        decrypted += char
                write_file('extra.txt', decrypted + '\n')
                write_file('key-new.txt', f'{a} {b}\n')
                return

    return "Nie można znaleźć kluczy"


def main():
    if len(sys.argv) < 3:
        print("Usage: cezar.py -c|-a  -e|-d|-j|-k")
        sys.exit(1)
    choice = sys.argv[1]
    if choice == "-c":
        option = sys.argv[2]
        if option == "-e":
            plain = read_file('plain.txt')
            key = read_file('key.txt')
            if key[0].isdigit():
                key_n = int(key[0])
                cezar_encrypt(plain, key_n)
            else:
                print("Klucz musi być liczbą")
        elif option == "-d":
            crypto = read_file('crypto.txt')
            key = read_file('key.txt')
            if key[0].isdigit():
                key_n = int(key[0])
                cezar_decrypt(crypto, key_n)
            else:
                print("Klucz musi być liczbą")
        elif option == "-j":
            crypto = read_file('crypto.txt')
            key = read_file('extra.txt')
            kryptoanaliza_pomoc(crypto, key)
        elif option == "-k":
            crypto = read_file('crypto.txt')
            kryptoanaliza_sam(crypto)            
    elif choice == "-a":
        option = sys.argv[2]
        if option == "-e":
            plain = read_file('plain.txt')
            key = read_file('key.txt')
            if key[2].isdigit() and key[4].isdigit():
                key_a = int(key[2])
                key_b = int(key[4])
                afiniczny_encrypt(plain, key_a, key_b)
            else:
                print("Klucze muszą być liczbami")
        elif option == "-d":
            crypto = read_file('crypto.txt')
            key = read_file('key.txt')
            if key[2].isdigit() and key[4].isdigit():
                key_a = int(key[2])
                key_b = int(key[4])
                afiniczny_decrypt(crypto, key_a, key_b)
            else:
                print("Klucze muszą być liczbami")
        elif option == "-j":
            crypto = read_file('crypto.txt')
            key = read_file('extra.txt')
            key_a = key[0]
            key_b = key[1]
            kryptoanaliza_afiniczny_pomoc(crypto, key_a, key_b)
        elif option == "-k":
            crypto = read_file('crypto.txt')
            kryptoanaliza_afiniczny_sam(crypto)


main()