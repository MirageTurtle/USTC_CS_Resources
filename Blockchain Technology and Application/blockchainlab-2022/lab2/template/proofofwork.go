package main

import (
	"math"
	"math/big"
	"crypto/sha256"
	"bytes"
)

var (
	maxNonce = math.MaxInt64
)

// ProofOfWork represents a proof-of-work
type ProofOfWork struct {
	block *Block
}

// NewProofOfWork builds and returns a ProofOfWork
func NewProofOfWork(b *Block) *ProofOfWork {
	pow := &ProofOfWork{b}

	return pow
}

// Run performs a proof-of-work
// implement
func (pow *ProofOfWork) Run() (int, []byte) {
	nonce := 0
	var hash_int big.Int
	var hash [32]byte

	for nonce < maxNonce {
		// data waiting for hash
		data := bytes.Join(
			[][]byte{
				pow.block.PrevBlockHash,
				pow.block.HashData(),
				IntToHex(pow.block.Timestamp),
				IntToHex(int64(pow.block.Bits)),
				IntToHex(int64(nonce)),
			},
			[]byte{},
		)
		// compute hash and the corrsponding big int
		hash = sha256.Sum256(data)
		hash_int.SetBytes(hash[:])
		// compute the target int (a number begin with pow.block.Bits zero in binary)
		target := big.NewInt(1)
		target.Lsh(target, uint(256 - pow.block.Bits))
		// validate
		if hash_int.Cmp(target) == -1 {
			break
		} else {
			nonce += 1
		}
	}
	// return nonce, pow.block.Hash
	return nonce, hash[:]
}

// Validate validates block's PoW
// implement
func (pow *ProofOfWork) Validate() bool {
	var hash_int big.Int
	// compute the big int corresponding block hash
	hash_int.SetBytes(pow.block.Hash[:])
	// compute the target int
	target := big.NewInt(1)
	target.Lsh(target, uint(256 - pow.block.Bits))	
	// validate
	return (hash_int.Cmp(target) == -1)
}
