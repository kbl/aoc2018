from aoc2018.day16e1 import operations
from aoc2018 import readlines


def solve(lines):
    ip_register, program = parse(lines)
    registers = [0, 0, 0, 0, 0, 0]
    ip_value = 0

    while ip_value < len(program):
        instruction, a, b, c = program[ip_value]

        registers[ip_register] = ip_value

        instruction(registers, a, b, c)

        ip_value = registers[ip_register]
        ip_value += 1

    return registers[0]


def parse(lines):
    program = []
    ops = {o.__name__: o for o in operations}
    ip_register = int(lines[0].split(' ')[1])
    for line in lines[1:]:
        line = line.split(' ')
        program.append((ops[line[0]], *map(int, line[1:])))
    return ip_register, program


lines = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""".split('\n')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    print(solve(readlines()))
