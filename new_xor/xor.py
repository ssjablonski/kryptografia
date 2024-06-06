import sys
import os

# autorem jest Sebastian Jabłoński 285810

def process_original_text():
    try:
        with open("orig.txt", 'r', encoding="us-ascii") as f:
            text = f.read()
            processed_text = ''.join(char.lower() if char.isalpha() or char.isspace() else '' for char in text)
            processed_text = ' '.join(processed_text.split())
            lines = split_text_into_blocks(processed_text)
            formatted_text = '\n'.join(lines)
            
        with open("plain.txt", 'w') as f:
            f.write(formatted_text)
    except FileNotFoundError:
        print("Nie można znaleźć pliku orig.txt")

def read_key():
    if not os.path.exists('key.txt'):
        raise FileNotFoundError("Plik key.txt nie istnieje.")

    with open('key.txt', 'r', encoding="us-ascii") as f:
        key = f.read()
        if len(key) != 64:
            raise ValueError(f"Niewłaściwa długość klucza {len(key)}. Klucz powinien mieć długość 64.")

    return key

def read_plain_text():
    with open('plain.txt', 'r', encoding="us-ascii") as f:
        return f.read().replace('\r', '').replace('\n', '')

def split_text_into_blocks(text):
    return [text[i:i+64] for i in range(0, len(text), 64)]

def line_encrypt(text, key):
    encrypted_text = ''
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % 64]))
    return encrypted_text

def encrypt():
    key = read_key()
    plain_text = read_plain_text()
    text_blocks = split_text_into_blocks(plain_text)
    encrypted_blocks = [line_encrypt(block, key) for block in text_blocks]
    encrypted_text = ''.join(encrypted_blocks)
    
    with open('crypto.txt', 'w', encoding="us-ascii") as f:
        f.write(encrypted_text)

def decrypt():
    with open('crypto.txt', 'r+', encoding="us-ascii") as f:
        crypto = f.read()

    hex_array = [hex(ord(char))[2:].zfill(2) for char in crypto]
    sub_hex_array = split_text_into_blocks(hex_array)
    
    key = find_decryption_key(sub_hex_array)
    decrypted_text = ""

    for i, char in enumerate(hex_array):
        if key[i % 64] == None:
            decrypted_text += "_"
        else:
            new_char = chr(int(char, 16) ^ ord(key[i % 64]))
            if new_char.isspace() or new_char.isalpha():
                decrypted_text += chr(int(char, 16) ^ ord(key[i % 64]))
            else:
                decrypted_text += "_"

    with open('decrypt.txt', 'w+', encoding="us-ascii") as w:
        for i in range(0, len(decrypted_text), 64):
            w.write(decrypted_text[i:i+64] + '\n')

def find_decryption_key(lines):
    key = [None] * 64
    for i in range(len(lines)-2):
        for j in range(i + 1, len(lines)-1):
            for k in range(j + 1, len(lines)):
                key = update_key(key, lines[i], lines[j], lines[k])
                if all(x is not None for x in key):
                    return key
    return key

def update_key(key, line_1, line_2, line_3):
    for i in range(min(len(line_1), len(line_2), len(line_3))):
        if key[i] is None and line_1[i] != line_2[i] != line_3[i] != line_1[i]:
            if chr(int(line_1[i], 16) ^ int(line_2[i], 16)).isalpha() and chr(int(line_1[i], 16) ^ int(line_3[i], 16)).isalpha():
                key[i] = chr(int(line_1[i], 16) ^ 32)
            elif chr(int(line_1[i], 16) ^ int(line_2[i], 16)).isalpha() and chr(int(line_2[i], 16) ^ int(line_3[i], 16)).isalpha():
                key[i] = chr(int(line_2[i], 16) ^ 32)
            elif chr(int(line_1[i], 16) ^ int(line_3[i], 16)).isalpha() and chr(int(line_2[i], 16) ^ int(line_3[i], 16)).isalpha():
                key[i] = chr(int(line_3[i], 16) ^ 32)
    return key


def main():
    if len(sys.argv) == 2:
        option = sys.argv[1]
        options = {'-p': process_original_text, '-e': encrypt, '-k': decrypt}
        if option in options:
            options[option]()
        else:
            print('Podaj jedną z opcji: -p, -e, -k')
    else:
        print('Podaj jedną z opcji: -p, -e, -k')


if __name__ == "__main__":
    main()