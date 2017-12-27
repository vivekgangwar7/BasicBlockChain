import hashlib
import time

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

# Transaction
class Transaction:
    def __init__(self, index, timestamp, senderName, receiverName, money):
        self.index = index
        self.timestamp = timestamp
        self.senderName = senderName
        self.receiverName = receiverName
        self.money = money
        self.hash = self.calculateHash()

    def calculateHash(self):
        return hashlib.sha256(str(self.index) + self.senderName + str(self.timestamp) + self.receiverName + str(self.money)).hexdigest()

    def printTransaction(self):
        print "Index #" + str(self.index)
        print "Sender's Name: " + self.senderName
        print "Receiver's Name: " + self.receiverName
        print "Money: " + str(self.money)
        print "TimeStamp: " + str(self.timestamp)
        print "Hash: " + str(self.hash)
        print "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"


# Transaction List
class TransactionList:
    def __init__(self,index, timestamp, senderN, receiverN, money):
        self.chain = [self.createFirstTransaction(index,timestamp, senderN, receiverN, money)]

    def createFirstTransaction(self,index, timestamp, senderN, receiverN, money):
        return Transaction(index, timestamp, senderN, receiverN, money)

    def getLatestTransaction(self):
        return self.chain[len(self.chain)-1]

    def addTransaction(self, newTransaction):
        self.chain.append(newTransaction)

    def printTransactionList(self):
        for i in range(0, len(self.chain)):
            self.chain[i].printTransaction()

    def returnList(self):
        return self

    def calculateHash(self, a , b):
        return hashlib.sha256(str(a) + str(b)).hexdigest()

    def merkleTree(self):
        q = Queue()
        for i in range(0, len(self.chain)):
            q.enqueue(self.chain[i].hash)

        while q.size()!=1:
            a = q.dequeue()
            b = q.dequeue()
            q.enqueue(self.calculateHash(a,b))

        fin = q.dequeue()
        return fin


# Block
class Block:
    def __init__(self, index, timestamp, TransactionList, merkleTree,  previousHash=' '):
        self.index = index
        self.timestamp = timestamp
        self.data = TransactionList
        self.previousHash = previousHash
        self.merkleTree = merkleTree
        self.hash = self.calculateHash()

    def calculateHash(self):
        return hashlib.sha256(str(self.index) + self.previousHash + str(self.timestamp)).hexdigest()

    def printBlock(self):
        print "Block Index #" + str(self.index)
        print "Block Timestamp: " + str(self.timestamp)
        print "Merkle Tree: " + str(self.merkleTree)
        print "Block Previous Hash: " + str(self.previousHash)
        print "Block Hash: " + str(self.hash)
        print "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
        print str(self.data.printTransactionList())

    def fetchMerkleTree(self):
        merkleValue = self.data.merkleTree()
        return merkleValue


# BlockChain
class BlockChain:
    def __init__(self, transactionList):
        self.chain = [self.createGenesisBlock(transactionList)]

    def createGenesisBlock(self,transactionList):
        return Block(0, time.time(), transactionList, "0")

    def getLatestBlock(self):
        return self.chain[len(self.chain)-1]

    def addBlock(self, newBlock):
        newBlock.previousHash = self.getLatestBlock().hash
        newBlock.hash = newBlock.calculateHash()
        self.chain.append(newBlock)

    def isChainValid(self):
        for i in range (1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i-1]
            if currentBlock.hash != currentBlock.calculateHash():
                return False
            if currentBlock.previousHash != previousBlock.hash:
                return False
        return True

    def printBlockChain(self):
        for i in range(1, len(self.chain)):
            self.chain[i].printBlock()


vivTransaction = TransactionList(1, time.time(), "Vivek", "Ishita", 1001)
vivTransaction.addTransaction(Transaction(1, time.time(), "Vivek", "Ishita", 1001))
vivTransaction.addTransaction(Transaction(3, time.time(), "Vivek", "xyz", 10010))
vivTransaction.addTransaction(Transaction(4, time.time(), "Vivek", "bca", 11000))
vivTransaction.getLatestTransaction()
vivBlock = BlockChain(vivTransaction)
vivBlock.addBlock(Block(1, time.time(), vivTransaction, vivTransaction.merkleTree(), "0"))
vivBlock.printBlockChain()
