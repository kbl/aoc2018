import re
from aoc2018 import readlines


def addr(r, a, b, c):
    """
    addr (add register) stores into register C the result of adding register A and register B.
    >>> addr([1, 2, 3, 4], 0, 1, 3)
    [1, 2, 3, 3]
    """
    r[c] = r[a] + r[b]
    return r


def addi(r, a, b, c):
    """
    addi (add immediate) stores into register C the result of adding register A and value B.
    >>> addi([1, 2, 3, 4], 2, 7, 0)
    [10, 2, 3, 4]
    """
    r[c] = r[a] + b
    return r


def mulr(r, a, b, c):
    """
    mulr (multiply register) stores into register C the result of multiplying register A and register B.
    >>> mulr([1, 2, 3, 4], 0, 1, 3)
    [1, 2, 3, 2]
    """
    r[c] = r[a] * r[b]
    return r


def muli(r, a, b, c):
    """
    muli (multiply immediate) stores into register C the result of multiplying register A and value B.
    >>> muli([1, 2, 3, 4], 2, 7, 0)
    [21, 2, 3, 4]
    """
    r[c] = r[a] * b
    return r


def banr(r, a, b, c):
    """
    banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
    >>> banr([1, 2, 3, 4], 0, 1, 3)
    [1, 2, 3, 0]
    """
    r[c] = r[a] & r[b]
    return r


def bani(r, a, b, c):
    """
    bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
    >>> bani([1, 2, 3, 4], 2, 7, 0)
    [3, 2, 3, 4]
    """
    r[c] = r[a] & b
    return r


def borr(r, a, b, c):
    """
    borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
    >>> borr([1, 2, 3, 4], 0, 1, 3)
    [1, 2, 3, 3]
    """
    r[c] = r[a] | r[b]
    return r


def bori(r, a, b, c):
    """
    bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
    >>> bori([1, 2, 3, 4], 2, 7, 0)
    [7, 2, 3, 4]
    """
    r[c] = r[a] | b
    return r


def setr(r, a, b, c):
    """
    setr (set register) copies the contents of register A into register C. (Input B is ignored.)
    >>> setr([1, 2, 3, 4], 0, 1, 3)
    [1, 2, 3, 1]
    """
    r[c] = r[a]
    return r


def seti(r, a, b, c):
    """
    seti (set immediate) stores value A into register C. (Input B is ignored.)
    >>> seti([1, 2, 3, 4], 2, 7, 0)
    [2, 2, 3, 4]
    """
    r[c] = a
    return r


def gtir(r, a, b, c):
    """
    gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    >>> gtir([1, 2, 3, 4], 0, 1, 3)
    [1, 2, 3, 0]
    """
    if a > r[b]:
        r[c] = 1
    else:
        r[c] = 0
    return r


def gtri(r, a, b, c):
    """
    gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    >>> gtri([1, 2, 3, 4], 2, 7, 3)
    [1, 2, 3, 0]
    """
    if r[a] > b:
        r[c] = 1
    else:
        r[c] = 0
    return r


def gtrr(r, a, b, c):
    """
    gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
    >>> gtrr([1, 2, 3, 4], 2, 1, 3)
    [1, 2, 3, 1]
    """
    if r[a] > r[b]:
        r[c] = 1
    else:
        r[c] = 0
    return r


def eqir(r, a, b, c):
    """
    eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    >>> gtir([1, 2, 3, 4], 0, 1, 3)
    [1, 2, 3, 0]
    """
    if a == r[b]:
        r[c] = 1
    else:
        r[c] = 0
    return r


def eqri(r, a, b, c):
    """
    eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    >>> gtri([1, 2, 3, 4], 2, 7, 3)
    [1, 2, 3, 0]
    """
    if r[a] == b:
        r[c] = 1
    else:
        r[c] = 0
    return r


def eqrr(r, a, b, c):
    """
    eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
    >>> gtrr([1, 2, 3, 4], 2, 1, 3)
    [1, 2, 3, 1]
    """
    if r[a] == r[b]:
        r[c] = 1
    else:
        r[c] = 0
    return r


operations = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]


BEFORE_RE = re.compile(r'Before: \[(\d+), (\d+), (\d+), (\d+)\]')
AFTER_RE = re.compile(r'After:  \[(\d+), (\d+), (\d+), (\d+)\]')


def parse(lines):
    triples = []
    program = []
    for line in lines:
        if not line:
            continue
        match = BEFORE_RE.match(line)
        if match:
            before = [int(token) for token in match.groups()]
            continue
        match = AFTER_RE.match(line)
        if match:
            after = [int(token) for token in match.groups()]
            triples.append((before, instruction, after))
            program = []
            continue
        instruction = [int(token) for token in line.split(' ')]
        program.append(instruction)
    return triples, program


def solve(triples):
    how_many = 0
    for before, instruction, after in triples:
        works = 0
        for o in operations:
            if after == o(list(before), *instruction[1:]):
                works += 1
        if works >= 3:
            how_many += 1
    return how_many


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
    
    triples, _ = parse(readlines())
    print(solve(triples))
