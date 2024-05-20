# Autorem jest Sebastian Jabłoński
import sys
import os

def check_file_length(filename, n):
    array = []
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            array.append(len(line))
    return all(length == n + 1 for length in array[:-1])

def text_prep(input_file, output_file, n):
    with open(input_file, 'r') as input_file:
        with open(output_file, 'w') as output_file:
            text = input_file.read().translate({ord('\r'): None, ord('\n'): None})
            for i in range(0, len(text), n):
                if i + n >= len(text):
                    output_file.write(text[i:])
                else:
                    output_file.write(text[i:i + n] + '\n')


def decrypt(text):
    binary_text = [bin(ord(char))[2:].zfill(8) for char in text]
    sub_binary_text = [binary_text[i:i + 64] for i in range(0, len(binary_text), 64)]
    key = find_key(sub_binary_text)
    
    print(key)
    decrypted_text = ""
    for i, char in enumerate(binary_text):
        if key[i %64] == "_":
            decrypted_text += "_"
        elif key[i%64].isalpha() or key[i%64].isspace():
            decrypted_text += chr(int(char,2 ) ^ ord(key[i%64]))
        else:
            decrypted_text += "_"
    with open('decrypt.txt', 'w+') as decrypt:
        decrypt.write(decrypted_text)

def encrypt(text, key):
    encrypted_text = ''
    text = text.translate({ord('\r'): None, ord('\n'): None})

    for i in range(len(text)):
        letter = text[i]
        if letter.isalpha() or letter.isspace():
            encrypted_text += chr(ord(letter) ^ ord(key[i]))
        else:
            encrypted_text += letter
    return encrypted_text


def find_key(text):
    key = ['_'] * 64
    for i in range(0, len(text) - 2):
        for j in range(i + 1, len(text) - 1):
            for k in range(j + 1, len(text)):
                key = xor(key, text[i], text[j], text[k])
    return key


def xor(key, w1, w2, w3):
    min_w = min(len(w1), len(w2), len(w3))
    for i in range(min_w):
        m1 = int(w1[i], 2)
        m2 = int(w2[i], 2)
        m3 = int(w3[i], 2)

        if key[i] != '_' or m1 == m2 or m1 == m3 or m2 == m3:
            continue
        if chr(m1 ^ m2).isalpha() and chr(m1 ^ m3).isalpha():
            key[i] = chr(m1 ^ 32)
        elif chr(m2 ^ m1).isalpha() and chr(m2 ^ m3).isalpha():
            key[i] = chr(m2 ^ 32)
        elif chr(m3 ^ m1).isalpha() and chr(m3 ^ m2).isalpha():
            key[i] = chr(m3 ^ 32)
    return key


def main():
    n = 64

    if '-p' == sys.argv[1]:
        text_prep('orig.txt', 'plain.txt', n)

    if '-e' == sys.argv[1]:
        if not check_file_length('plain.txt', n):
            print("Zła długość")

        encrypted_text = ''
        with open('key.txt', 'r') as key_file:
            key = key_file.read().strip()
        with open('plain.txt', 'r') as file:
            for line in file:
                encrypted_text += encrypt(line, key)
        with open('crypto.txt', 'w') as crypto_file:
            crypto_file.write(encrypted_text)

    if '-k' == sys.argv[1]:
        with open('crypto.txt', 'r') as crypto_file:
            encrypted_text = crypto_file.read().strip()
            decrypt(encrypted_text)



main()