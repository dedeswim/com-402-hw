from block import Block

class BlockChain:

    def __init__(self, genesis_block: Block):
        self.root = genesis_block
        self._last = genesis_block

    def append(self, new_block: Block):
        if new_block.previous_hash == self._last.hash():
            self._last = self._last.append_next(new_block)
            return new_block
        
        return None
        