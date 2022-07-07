package main

// MerkleTree represent a Merkle tree
type MerkleTree struct {
	RootNode *MerkleNode
}

// MerkleNode represent a Merkle tree node
type MerkleNode struct {
	Left  *MerkleNode
	Right *MerkleNode
	Data  []byte
}

// NewMerkleTree creates a new Merkle tree from a sequence of data
// implement
func NewMerkleTree(data [][]byte) *MerkleTree {
	// var node = MerkleNode{nil, nil, data[0]}
	// var mTree = MerkleTree{&node}

	// if len(data) == 1 {
	// 	return &mTree
	// }

	var nodes []MerkleNode
	// make merkle node for every data
	for _, dataItem := range data {
		node := NewMerkleNode(nil, nil, dataItem)
		nodes = append(nodes, *node)
	}
	// merge all nodes to a tree, merkle tree
	for len(nodes) > 1 {
		// make the number of nodes even
		if len(nodes) % 2 == 1 {
			nodes = append(nodes, nodes[len(nodes) - 1])
		}
		var tmpNodes []MerkleNode
		for i := 0; i < len(nodes); i += 2 {
			node := NewMerkleNode(&nodes[i], &nodes[i + 1], nil)
			tmpNodes = append(tmpNodes, *node)
		}
		nodes = tmpNodes
	}
	mTree := MerkleTree{&nodes[0]}

	return &mTree
}

// NewMerkleNode creates a new Merkle tree node
// implement
func NewMerkleNode(left, right *MerkleNode, data []byte) *MerkleNode {
	node := MerkleNode{}
	if left == nil && right == nil {
		hash := mySha256(data)
		node.Data = hash[:]
	} else {
		// ... means two params
		prevHashes := append(left.Data, right.Data...)
		hash := mySha256(prevHashes)
		node.Data = hash[:]
	}
	node.Left = left
	node.Right = right

	return &node
}
