package main

import (
	// "fmt"
	// "encoding/hex"
	"encoding/binary"
)

func rightRotate(x uint32, n uint) uint32 {
	return (x >> n) | (x << (32 - n))
}

func Sigma0(x uint32) uint32 {
	return rightRotate(x, 2) ^ rightRotate(x, 13) ^ rightRotate(x, 22)
}

func Sigma1(x uint32) uint32 {
	return rightRotate(x, 6) ^ rightRotate(x, 11) ^ rightRotate(x, 25)
}

func ch(e, f, g uint32) uint32 {
	return (e & f) ^ ((^e) & g)
}

func maj(a, b, c uint32) uint32 {
	return (a & b) ^ (a & c) ^ (b & c)
}

func mySha256(message []byte) [32]byte {
	//前八个素数平方根的小数部分的前面32位
	h0 := uint32(0x6a09e667)
	h1 := uint32(0xbb67ae85)
	h2 := uint32(0x3c6ef372)
	h3 := uint32(0xa54ff53a)
	h4 := uint32(0x510e527f)
	h5 := uint32(0x9b05688c)
	h6 := uint32(0x1f83d9ab)
	h7 := uint32(0x5be0cd19)

	//自然数中前面64个素数的立方根的小数部分的前32位
	k := [64]uint32{
		0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
		0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
		0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
		0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
		0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
		0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
		0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
		0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2}

	sha256data := [32]byte{}

	// l + 1 + m = 448 mod 512
	l := len(message) * 8
	m := (447 - l % 512) % 512
	// fmt.Printf("l: %d, m: %d\n", l, m)
	code := make([]byte, (l + 1 + m + 64) / 8)
	// fmt.Printf("length of code: %d\n", (l + 1 + m + 64) / 8)
	copy(code[0: l / 8], message)
	code[l / 8] = byte(1 << 7)
	// code[l + 1: l + 1 + m] = byte(0)
	// code[(l + 1 + m + 64) / 8 - 1] = uint64(l)
	binary.BigEndian.PutUint64(code[(l + 1 + m + 64) / 8 - 8: (l + 1 + m + 64) / 8], uint64(l))
	// fmt.Println((l + 1 + m + 64) / 8 - 1)
	// fmt.Println(code[(l + 1 + m + 64) / 8 - 1])
	// fmt.Printf("%x\n", message)
	// fmt.Printf("%x\n", code)
	N := (l + 1 + m + 64) / 8 / 64
	// fmt.Printf("N: %v\n", N)
	w := [64]uint32{}
	for n := 0; n < N; n++ {
		for i := 0; i < 16; i++ {
			// fmt.Printf("%x\n", code[i * 4 + n * 64: (i + 1) * 4 + n * 64])
			w[i] = binary.BigEndian.Uint32(code[i * 4 + n * 64: (i + 1) * 4 + n * 64])
		}
		for i := 16; i < 64; i++ {
			s0 := rightRotate(w[i - 15], 7) ^ rightRotate(w[i - 15], 18) ^ (w[i - 15] >> 3)
			s1 := rightRotate(w[i - 2], 17) ^ rightRotate(w[i - 2], 19) ^ (w[i - 2] >> 10)
			w[i] = w[i - 16] + s0 + w[i - 7] + s1
		}

		a := h0
		b := h1
		c := h2
		d := h3
		e := h4
		f := h5
		g := h6
		h := h7
		for i := 0; i < 64; i++ {
			t1 := h + Sigma1(e) + ch(e, f, g) + k[i] + w[i]
			t2 := Sigma0(a) + maj(a, b, c)
			h = g
			g = f
			f = e
			e = d + t1
			d = c
			c = b
			b = a
			a = t1 + t2
		}
		h0 = a + h0
		h1 = b + h1
		h2 = c + h2
		h3 = d + h3
		h4 = e + h4
		h5 = f + h5
		h6 = g + h6
		h7 = h + h7
	}
	h := []uint32{h0, h1, h2, h3, h4, h5, h6, h7}
	for i := 0; i < 8; i++ {
		binary.BigEndian.PutUint32(sha256data[i * 4: (i + 1) * 4], h[i])
	}

	return sha256data
}

// func main() {
// 	// s := "95b96c86facc54de528a1d8956091fe13af19a7f4f59e3b90ff7e7005925e0e7"
// 	s := "95b96c86facc54de528a1d8956091fe1"
// 	// s := "BlockChain"
// 	// s := "'blockchain with looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong data'"
// 	m := []byte(s[:])
// 	fmt.Println(len(m))
// 	a := mySha256(m[:])
// 	fmt.Println(hex.EncodeToString(a[:]))
// }