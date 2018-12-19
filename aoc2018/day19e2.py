# STEP #1
#  1 seti 1 7 1
#  2 seti 1 7 5
#  3 mulr 1 5 4
#  4 eqrr 4 2 4
#  5 addr 4 3 3
#  6 addi 3 1 3
#  7 addr 1 0 0
#  8 addi 5 1 5
#  9 gtrr 5 2 4
# 10 addr 3 4 3
# 11 seti 2 2 3
# 12 addi 1 1 1
# 13 gtrr 1 2 4
# 14 addr 4 3 3
# 15 seti 1 5 3
# 16 mulr 3 3 3

# STEP #2
#  1 seti 1 - B
#  2 seti 1 - F
#  3 mulr B F E
#  4 eqrr E C E
#  5 addr E D D
#  6 addi D 1 D
#  7 addr B A A
#  8 addi F 1 F
#  9 gtrr F C E
# 10 addr D E D
# 11 seti 2 - D
# 12 addi B 1 B
# 13 gtrr B C E
# 14 addr E D D
# 15 seti 1 - D
# 16 mulr D D D

# STEP #3
#  1 seti 1 - B   B = 1
#  2 seti 1 - F   F = 1
#  3 mulr B F E   E = B * F
#  4 eqrr E C E   if E == C:
#                     E = 1
#                 else:
#                     E = 0
#  5 addr E D D   D += E
#  6 addi D 1 D   D += 1
#  7 addr B A A   A += B
#  8 addi F 1 F   F += 1
#  9 gtrr F C E   if F > C
#                     E = 1
#                 else:
#                     E = 0
# 10 addr D E D   D += E
# 11 seti 2 - D   goto 3
# 12 addi B 1 B   B += 1
# 13 gtrr B C E   if B > C
#                     E = 1
#                 else:
#                     E = 0
# 14 addr E D D   D += E
# 15 seti 1 - D   goto 2
# 16 mulr D D D   D *= D

# STEP #4
# def loop(A, B, C, D, E, F):
#     B = 1
#     while True:
#         F = 1             # 2
#         while True:
#             E = B * F     # 3
#             if E == C:    # 4
#                 A += B    # 7
#             F += 1        # 8
#             if F <= C:    # 9
#                 continue  # 11
#             B += 1        # 12
#             if B > C:     # 13
#                 print(A, B, C, D, E, F)
#                 return
#             print(B, C, A)
#             break

# STEP #5
# def loop(A, B, C, D, E, F):
#     for B in range(1, C + 1):
#         print(B, A)
#         for F in range(1, C + 1):
#             if B * F > C:
#                 break
#             if B * F == C:
#                 A += B
# 
#     print(A, B, C, D, E, F)

# STEP #6
def loop(A, B, C, D, E, F):
    x = 0
    for i in range(1, C + 1):
        if C % i == 0:
            x += i
    print(x)


if __name__ == '__main__':
    #         A     B         C     D         E     F
    #         1,    x,        2,    1,        0,    x
    loop(*[   1,    2,      882,    1,        0,  883])
    loop(*[   0,    1, 10551282,    1, 10550400,    0])

