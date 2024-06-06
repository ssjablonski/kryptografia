# Autor Sebastian Jabłoński

import hashlib
import os

if os.path.exists("diff.txt"):
    os.remove("diff.txt")

hash_functions = [hashlib.md5, hashlib.sha1, hashlib.sha224, hashlib.sha256, hashlib.sha384, hashlib.sha512, hashlib.blake2b]
hexa = []
hexa_ = []
results = []
results_ = []

with open('personal.txt', 'rb') as f_in1, open('personal_.txt', 'rb') as f_in2, open("hash-.pdf", "rb") as f_in3, open('diff.txt', 'a') as f_out:
    data = f_in1.read()
    data_ = f_in2.read()
    hash_ = f_in3.read()

    for func in hash_functions:
        h = func(hash_ + data).hexdigest()
        h_ = func(hash_ + data_).hexdigest()
        hexa.append(h)
        hexa_.append(h_)
        res = format(int(h,16), '0>42b')
        res_ = format(int(h_,16), '0>42b')

        if (len(res) > len(res_)):
            res_ += "2" * (len(res)-len(res_))
        else:
            res += "2" * (len(res_)-len(res))

        results.append(res)
        results_.append(res_)

    for i in range(len(results)):
        different = 0

        for j in range(len(results[i])):
            if (results[i][j]!=results_[i][j]):
                different += 1
        
        percentage = round(different/len(results[i])*100)

        f_out.write(f"{hash_functions[i].__name__}:\n{hexa[i]}\n{hexa_[i]}\nLiczba rozniacych sie bitow: {different} z {len(results[i])}, procentowo: {str(percentage)}%.\n\n")