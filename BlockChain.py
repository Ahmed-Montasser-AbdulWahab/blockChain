from hashlib import sha256
import json
import string
import time
import random





class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce


    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain: 
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
 
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    
    difficulty = 4
    def proof_of_work(self, block):
            block.nonce = 0
            computed_hash = block.compute_hash()
            while not computed_hash.startswith('0' * Blockchain.difficulty) and block.nonce < (2**64)-1:
                block.nonce += 1
                computed_hash = block.compute_hash()
            return computed_hash

    
    def add_block(self, block, proof):
        # previous_hash = self.last_block.hash
        # if previous_hash != block.previous_hash:
        #     print('F1')
        #     return False
        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True
 
    def is_valid_proof(self, block, block_hash):
            return (block_hash.startswith('0' * Blockchain.difficulty) and
                    block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
                self.unconfirmed_transactions = self.unconfirmed_transactions + transaction
    
    def mine(self):
            if not self.unconfirmed_transactions:
                return False
    
            last_block = self.last_block
    
            new_block = Block(index=last_block.index + 1,
                            transactions=self.unconfirmed_transactions,
                            timestamp=time.time(),
                            previous_hash=last_block.hash)
    
            proof = self.proof_of_work(new_block)
            self.add_block(new_block, proof)
            self.unconfirmed_transactions = []
            return new_block.index


class True_User:
    def mine_addBlock(self, blockchain):
        # block_miner = Block(index=blockchain.chain[-1].index + 1, transactions=blockchain.unconfirmed_transactions, timestamp=time.time(),
        #  previous_hash=blockchain.last_block.hash)
        # proof_of_WORK = blockchain.proof_of_work(block_miner)
        # blockchain.add_block(block_miner, proof_of_WORK)
        blockchain.add_new_transaction(random_transactions())
        blockchain.mine()

class Attacker:
    def attack_BlockChain(self, blockchain):
        blockchain.add_new_transaction(random_transactions())
        print(len(blockchain.unconfirmed_transactions))
        if not blockchain.unconfirmed_transactions:
                return False
        new_block = Block(index=blockchain.chain[-2].index+1,
                            transactions=blockchain.unconfirmed_transactions,
                            timestamp=time.time(),
                            previous_hash=blockchain.chain[-2].hash)
        proof = blockchain.proof_of_work(new_block)
        print(proof)
        blockchain.add_block(new_block, proof)
        blockchain.unconfirmed_transactions = []
        return new_block.index



def random_transactions():
    total_ran = []
    for _ in range(random.randint(3, 5)):
        s = 16
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = s))
        total_ran.append(ran)
    return total_ran


if __name__ == '__main__':
    """Experimenting Difficulty to produce 1 block/sec"""
    blockchain = Blockchain()

    blockchain.create_genesis_block()



    # while(True):
    #     blockchain.add_new_transaction(random_transactions())
    #     n1 = time.time()
    #     index = blockchain.mine()
    #     n2 = time.time() - n1
    #     if 1.5 > n2 > 0.5:
    #         print('Difficulty : ' , blockchain.difficulty)
    #         print('Time :', n2)
    #         print('Index :' , index)
    #         break
    #     elif n2 >= 1.5 :
    #         Blockchain.difficulty-=1
    #     elif n2 <= 0.5:
    #         Blockchain.difficulty+=1

    #     print('************************************')
    #     print('Index :' , index)
    #     print('Time :', n2)
    #     print('Difficulty : ' , blockchain.difficulty)
    #     print('************************************')
    """END OF First Requirement"""

    """Second Requirement"""
    
    tu1 = True_User()
    for i in range(0,3):
        tu1.mine_addBlock(blockchain=blockchain)
    
    # for i in blockchain.chain:
    #     print('Index : ', i.index)
    #     print('Transactions : ', i.transactions)
    #     print('Now Hash : ', i.hash )
    #     print('Previous Hash : ', i.previous_hash)
    
    atck = Attacker()
    atck.attack_BlockChain(blockchain=blockchain)
    for i in blockchain.chain:
        print('Index : ', i.index)
        print('Transactions : ', i.transactions)
        print('Now Hash : ', i.hash )
        print('Previous Hash : ', i.previous_hash)


