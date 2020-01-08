from blockchain import BlockChain
from block import Block
from hashlib import sha256
from json import dumps

genesis_prev_hash = sha256((b'\x00' * 32))

genesis_data = 'Hello there!'.encode('utf-8')
data1 = '1!'.encode('utf-8')
data2 = '2!'.encode('utf-8')
data3 = '3!'.encode('utf-8')
data4 = '4!'.encode('utf-8')

genesis_block = Block(genesis_data, genesis_prev_hash.digest())
block1 = Block(data1, genesis_block.hash())
block2 = Block(data2, block1.hash())
block3 = Block(data3, block2.hash())
block4 = Block(data4, block1.hash())

blockchain = BlockChain(genesis_block)

one = blockchain.append(block1)
two = blockchain.append(block2)
three = blockchain.append(block3)
four = blockchain.append(block4)

test_dict = {
    "data": "MyE=",
    "previous": "3b9448477c4dc133872b1029ab8d3e5ca151ad872cf5de636c2e8595dbf67855"
}

test = Block.decode(dumps(test_dict))

print(test)


