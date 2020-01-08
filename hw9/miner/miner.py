import sys
import argparse
import websockets
import asyncio
import select
from multiprocessing import Process, Pool
from collections import namedtuple
from hashlib import sha256
from typing import List
from block import Block
from blockchain import BlockChain

Address = namedtuple('Address', 'host port')


class Miner:

    def __init__(self, addr: Address, miners: List[Address], genesis: bool):
        self._addr = addr
        self._miners = miners

        if genesis:
            genesis_data = 'Hello, world!'.encode('utf-8')
            genesis_block = Block.genesis_block(genesis_data)
            self._blockchain = BlockChain(genesis_block)

    def broadcast(self, block: Block):
        map(lambda miner: send_block(block, miner), self._miners)

    async def send_block(self, block: Block, miner: Address):
        uri = 'ws://' + miner.host + ':' + miner.port
        async with websockets.connect(uri) as websocket:
            await websocket.send(block.encode())

    def listen(self):
        with Pool(len(self._miners)) as p:
            p.map(self.listen_miner, self._miners)
            

    async def listen_miner(self, miner):
        uri = f'ws://{miner.host}:{str(miner.port)}/'
        print(f'Listening from {uri}')
        with websockets.connect(uri) as websocket:
            while True:
                block = await websocket.recv()
                print(block)

    def add_block(self, block: Block):
        self.broadcast(block)

    def validate(self, block: Block):
        pass

    def _printable_miners(self):
        return list(map(lambda addr: addr.host + ':' + str(addr.port), self._miners))

    def run(self):
        print('-------- Running Miner --------')
        print(f'Address of the miner: {self._addr.host}:{self._addr.port}')
        print(f'Other miners: {self._printable_miners()}')
        print(f'Created genesis: {genesis}')
        print('-------------------------------')

        listen = self.listen()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'addr', help='Address of the miner in the format "host:port".')
    parser.add_argument(
        'others', help='Comma-separated list of the other miners\' addresses in the format "host:port, host:port, ...".')
    parser.add_argument(
        'genesis', help='Optional, if the miner must generate the genesis block.', nargs='?', default=False)
    args = parser.parse_args()

    raw_addr = args.addr.split(':')
    addr = Address(raw_addr[0], raw_addr[1])
    others = args.others.split(',')
    others_split = map(lambda addr: addr.split(':'), others)
    others_tuples = list(map(lambda addr: Address(
        addr[0], int(addr[1])), others_split))
    genesis = True if args.genesis else False

    miner = Miner(addr, others_tuples, genesis)

    miner.run()
