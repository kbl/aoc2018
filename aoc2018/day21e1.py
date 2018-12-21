def magic():
    A = B = C = D = F = 0
    D = B | 65536
    B = 6780005
    while True:
        C = D & 255
        B = ((((B + C) & 16777215) * 65899) & 16777215)

        if 256 > D:
            return B
            if B == A:
                break
            C = 0
            D = B | 65536
            B = 6780005
            continue

        C = 0
        while True:
            F = (C + 1) * 256
            if F > D:
                F = 1
                break
            F = 0
            C += 1

        D = C


if __name__ == '__main__':
    print(magic())
