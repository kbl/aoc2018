def magic():
    previous = 0
    seen = set()
    A = B = D = 0

    while True:
        D = B | 65536
        B = 6780005

        while True:
            B = (B + (D & 255)) & 16777215
            B = B * 65899 & 16777215

            if D < 256:
                break

            D //= 256

        if B in seen:
            return previous
        previous = B
        seen.add(B)

        if B == A:
            break


if __name__ == '__main__':
    print(magic())
