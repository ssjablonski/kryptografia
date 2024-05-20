import sys
import random
from math import gcd

def main():
    try:
        with open("wejscie.txt", "r") as input_file, open("wyjscie.txt", "w") as output_file:
            number1 = input_file.readline().strip()
            number2 = input_file.readline().strip()
            number3 = input_file.readline().strip()

            if number1:
                number1 = int(number1)
            if number2:
                number2 = int(number2)
            if number3:
                number3 = int(number3)

            if len(sys.argv) > 1:
                if sys.argv[1] == "-f":
                    k = 0
                    b_before = 0
                    a = random.randint(2, number1 - 1)
                    m = number1 - 1
                    bj = pow(a, m, number1)
                    if bj != 1:
                        output_file.write("prawdopodobnie zlozona")
                        return
                    output_file.write("brak pewnosci, dla a = " + str(a))
                else:
                    print("Nieprawidlowy parametr.", file=sys.stderr)
            else:
                if number3:
                    number2 = (number2 * number3) - 1
                    for _ in range(40):
                        k = 0
                        b_before = 0
                        first = True
                        a = random.randint(2, number1 - 1)
                        if gcd(a, number1) != 1:
                            ret = gcd(a, number1)
                            output_file.write(str(ret))
                            return
                        m = number2
                        while m % 2 == 0:
                            k += 1
                            m //= 2
                        bj = pow(a, m, number1)
                        if bj == 1 or bj == number1 - 1:
                            continue
                        for _ in range(k):
                            bj_before = bj
                            bj = pow(bj, 2, number1)
                            if bj == 1 and first:
                                b_before = bj_before
                                first = False
                                break
                        ret = gcd(b_before - 1, number1)
                        if ret != 1:
                            output_file.write(str(ret))
                            return
                    output_file.write("prawdopodobnie pierwsza")
                elif number2:
                    for _ in range(40):
                        k = 0
                        b_before = 0
                        first = True
                        a = random.randint(2, number1 - 1)
                        if gcd(a, number1) != 1:
                            ret = gcd(a, number1)
                            output_file.write(str(ret))
                            return
                        m = number2
                        while m % 2 == 0:
                            k += 1
                            m //= 2
                        bj = pow(a, m, number1)
                        if bj != 1:
                            output_file.write(
                                "liczba r: "
                                + str(number2)
                                + " nie jest wykladnikiem uniwersalnym: ("
                                + str(a)
                                + "^"
                                + str(number2)
                                + ") mod "
                                + str(number1)
                                + " = "
                                + str(bj)
                            )
                            return
                        if bj == 1 or bj == number1 - 1:
                            continue
                        for _ in range(k):
                            bj_before = bj
                            bj = pow(bj, 2, number1)
                            if bj == 1 and first:
                                b_before = bj_before
                                first = False
                                break
                        ret = gcd(b_before - 1, number1)
                        if ret != 1:
                            output_file.write(str(ret))
                            return
                    output_file.write("prawdopodobnie pierwsza")
                elif number1:
                    for _ in range(40):
                        k = 0
                        b_before = 0
                        first = True
                        a = random.randint(2, number1 - 1)
                        if gcd(a, number1) != 1:
                            ret = gcd(a, number1)
                            output_file.write(str(ret))
                            return
                        m = number1 - 1
                        while m % 2 == 0:
                            k += 1
                            m //= 2
                        bj = pow(a, m, number1)
                        if bj == 1 or bj == number1 - 1:
                            continue
                        for _ in range(k):
                            bj_before = bj
                            bj = pow(bj, 2, number1)
                            if bj == 1 and first:
                                b_before = bj_before
                                first = False
                                break
                        if bj != 1:
                            output_file.write("na pewno zlozona")
                            return
                        else:
                            if (b_before - number1) != -1:
                                ret = gcd(b_before - 1, number1)
                                output_file.write(str(ret))
                                return
                    output_file.write("prawdopodobnie pierwsza")
                else:
                    print("Brak danych wejściowych", file=sys.stderr)
    except FileNotFoundError:
        print("Plik wejscie.txt nie istnieje.", file=sys.stderr)
        return

if __name__ == "__main__":
    main()
