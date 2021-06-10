import hashlib as hasher
import datetime as date
import json

from flask import Flask
from flask import request


class Block:
    def __init__(
        self, index: int, timestamp: date.datetime, data: json, previous_hash: int
    ) -> None:
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self) -> str:
        """Generate the hash for the current block"""

        sha = hasher.sha256()
        sha.update(
            #
            str(self.index).encode()
            + str(self.timestamp).encode()
            + str(self.data).encode()
            + str(self.previous_hash).encode()
        )

        return sha.hexdigest()


def create_genesis_block() -> Block:
    """
    Create the starting block for the chain.
    Starting at index 0 with an arbitrary previous hash.
    """

    return Block(
        0,
        date.datetime.now(),
        {
            "pow": 1,
            "transactions": [],
        },
        0,
    )


# Create the blockchain
blockchain = [create_genesis_block()]
last_block = blockchain[0]


def next_block(last_block: Block) -> Block:
    """Generate a new block"""

    index = last_block.index + 1
    timestamp = date.datetime.now()
    data = f"This is block number {index}"
    previous_hash = last_block.hash

    return Block(index, timestamp, data, previous_hash)


def proof_of_work(last_proof):
    """
    Simple proof of work algorithm. Returns the number that is
    divisble by 9 and the proof number of the last block.
    """

    proof = last_proof + 1
    while not (proof % 9 == 0 and proof % last_proof == 0):
        proof += 1

    return proof


app = Flask(__name__)

# Store the transactions
transactions = []
# Hardcode random miner address
miner_address = "imaminer!"


@app.route("/tx", methods=["POST"])
def transaction() -> str:
    if request.method == "POST":
        # Extract the transaction data
        tx = request.get_json()
        transactions.append(tx)
        # Log to the user
        print(json.dumps(tx, indent=4))
        return "Transaction submission successful\n"


@app.route("/mine", methods=["GET"])
def mine():
    # Mine a block
    last_block = blockchain[-1]
    last_proof = last_block.data["pow"]
    proof = proof_of_work(last_proof)
    # Miner reward
    transactions.append(
        {
            "sender": "network",
            "recipient": miner_address,
            "amount": 3,
        }
    )
    # Create the new block
    index = last_block.index + 1
    timestamp = date.datetime.now()
    data = {
        "pow": proof,
        "transactions": list(transactions),
    }
    previous_hash = last_block.hash
    mined_block = Block(index, timestamp, data, previous_hash)

    # Clear transaction list
    transactions.clear()
    blockchain.append(mined_block)

    return json.dumps(mined_block.data, indent=4)


app.run()
