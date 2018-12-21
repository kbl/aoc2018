package main

import "fmt"

func main() {
	A := 0 // 0
	A = 2525738
	B := 0 // 1
	C := 0 // 2
	D := 0 // 3
	F := 0 // 5
	// l00: seti 123 - 1
	// l00: seti 123 - B
	B = 123

	// l01: bani 1 456 1
	// l01: bani B 456 B
l01:
	B &= 456

	// l02: eqri 1 72 1
	// l02: eqri B 72 B
	if B == 72 {
		B = 1
	} else {
		B = 0
		// l03: addr 1 4 4
		// l03: addr B E E
		goto l01
	}

	// l05: seti 0 - 1
	// l05: seti 0 - B
	B = 0

	// l06: bori 1 65536 3
	// l06: bori B 65536 D
l06:
	D = B | 65536

	// l07: seti 6780005 - 1
	// l07: seti 6780005 - B
	B = 6780005

	// l08: bani 3 255 2
	// l08: bani D 255 C
l08:
	C = D & 255

	// l09: addr 1 2 1
	// l09: addr B C B
	B += C

	// l10: bani 1 16777215 1
	// l10: bani B 16777215 B
	B &= 16777215

	// l11: muli 1 65899 1
	// l11: muli B 65899 B
	B *= 65899

	// l12: bani 1 16777215 1
	// l12: bani B 16777215 B
	B &= 16777215

	// l13: gtir 256 3 2
	// l13: gtir 256 D C
	if 256 > D {
		C = 1
		goto l28
	} else {
		C = 0
	}

	// l17: seti 0 - 2
	// l17: seti 0 - C
	C = 0

	// l18: addi 2 1 5
	// l18: addi C 1 F
l18:
	F = C + 1

	// l19: muli 5 256 5
	// l19: muli F 256 F
	F *= 256

	// l20: gtrr 5 3 5
	// l20: gtrr F D F
	if F > D {
		F = 1
		goto l26
	} else {
		F = 0
	}

	// l24: addi 2 1 2
	// l24: addi C 1 C
	C += 1

	// l25: seti 17 - 4
	// l25: seti 17 - E
	goto l18

	// l26: setr 2 - 3
	// l26: setr C - D
l26:
	D = C

	// l27: seti 7 - 4
	// l27: seti 7 - E
	goto l08

	// l28: eqrr 1 0 2
	// l28: eqrr B A C
l28:
	fmt.Println(B)
	if B == A {
		C = 1
		fmt.Println("fajrant")
	} else {
		C = 0
		goto l06
	}
}
