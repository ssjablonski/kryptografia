import hashlib

personal_content = "Sebastian Jablonski"

with open("personal.txt", "w") as personal_file:
    personal_file.write(personal_content)


def calculate_hashes(filename):
    hash_functions = {
        "md5": hashlib.md5(),
        "sha1": hashlib.sha1(),
        "sha224": hashlib.sha224(),
        "sha256": hashlib.sha256(),
        "sha384": hashlib.sha384(),
        "sha512": hashlib.sha512(),
        "blake2b": hashlib.blake2b(),
    }

    with open(filename, "rb") as file:
        content = file.read()
        results = {}
        for name, hash_func in hash_functions.items():
            hash_func.update(content)
            results[name] = hash_func.hexdigest()

    return results


hashes = calculate_hashes("personal.txt")

with open("hash.txt", "w") as hash_file:
    for name in sorted(hashes, key=lambda x: len(hashes[x])):
        hash_file.write(f"{name}: {hashes[name]}\n")

print("Skróty zostały obliczone i zapisane do pliku hash.txt")