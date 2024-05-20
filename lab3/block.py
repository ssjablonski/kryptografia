# Autor Sebastian Jabłoński

from PIL import Image
import hashlib
import random
from datetime import datetime



def ecb(block_size, image_size, image_data, key):
    encrypt = bytearray(image_size[0] * image_size[1])

    for x in range(0, image_size[0], block_size):
        for y in range(0, image_size[1], block_size):
            block_help = bytearray([x ^ y for x, y in zip(block_taker(x, y, block_size, image_size, image_data), bytearray(key))])
            block_builder(encrypt, block_help, x, y, block_size, image_size)

    return encrypt


def cbc(block_size, image_size, image_data, key):
    byte_helper = bytearray([random.randint(0, 255) for _ in range(block_size * block_size)])
    hash_obj = hashlib.shake_256()
    encrypted_image = bytearray(image_size[0] * image_size[1])

    for x in range(0, image_size[0], block_size):
        for y in range(0, image_size[1], block_size):
            hash_obj.update(bytearray([x ^ y for x, y in zip(block_taker(x, y, block_size, image_size, image_data), byte_helper)]) + bytearray(key))
            byte_helper = hash_obj.digest(block_size * block_size)
            block_builder(encrypted_image, byte_helper, x, y, block_size, image_size)

    return encrypted_image


def key_generator(block_size):
    random.seed(datetime.now())
    return bytearray([random.randint(0, 255) for _ in range(block_size * block_size)])


def block_taker(x, y, block_size, size, image_data):
    block = bytearray(block_size * block_size)
    for i in range(block_size):
        for j in range(block_size):
            pos = (x + i) * size[1] + y + j
            if pos < size[0] * size[1]:
                block[i * block_size + j] = image_data[pos]

    return block


def block_builder(new_image, encrypted, x, y, block_size, size):
    for i in range(block_size):
        for j in range(block_size):
            elem = encrypted[i * block_size + j]
            pos = (x + i) * size[1] + y + j
            if pos < size[0] * size[1]:
                new_image[pos] = elem


def save_image(encrypted_image, input_image, path):
    input_image.frombytes(bytes(encrypted_image))
    input_image.save(path)



def main():
    input_image = Image.open("lab3/plain.bmp")
    input_image = input_image.convert('L')

    block = 8
    key = key_generator(block)

    image_data = input_image.tobytes()
    size = input_image.size

    encrypted_image_ecb = ecb(block, size, image_data, key)
    save_image(encrypted_image_ecb, input_image, 'lab3/ecb_crypto.bmp')

    encrypted_image_cbc = cbc(block, size, image_data, key)
    save_image(encrypted_image_cbc, input_image, 'lab3/cbc_crypto.bmp')

main()