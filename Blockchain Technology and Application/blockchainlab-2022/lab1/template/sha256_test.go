package main

import (
	"encoding/hex"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSha256(t *testing.T) {
	data1 := []byte("BlockChain")
	tmp1 := mySha256(data1)
	test_2561 := tmp1[:]

	assert.Equal(
		t,
		"3a6fed5fc11392b3ee9f81caf017b48640d7458766a8eb0382899a605b41f2b9",
		hex.EncodeToString(test_2561),
		"Pass first test",
	)

	data2 := []byte("'blockchain with looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong data'")
	tmp2 := mySha256(data2)
	test_2562 := tmp2[:]

	assert.Equal(
		t,
		"95b96c86facc54de528a1d8956091fe13af19a7f4f59e3b90ff7e7005925e0e7",
		hex.EncodeToString(test_2562),
		"Pass second test",
	)

	data3 := []byte("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
	tmp3 := mySha256(data3)
	test_2563 := tmp3[:]

	assert.Equal(
		t,
		"8f416c797433c47747d12104b1801d96c852a99a9f033bef9056e61292630f8a",
		hex.EncodeToString(test_2563),
		"Pass special test",
	)
}
