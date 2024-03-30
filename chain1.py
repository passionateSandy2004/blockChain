import hashlib
import datetime
import json
import os

class Block:
    def __init__(self, index, data, prev_hash):
        self.index = index
        self.timestamp = datetime.datetime.now().isoformat()
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256((str(self.index) + str(self.timestamp) + str(self.data) + str(self.prev_hash) + str(self.nonce)).encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block mined: ", self.hash)

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain = self.load_chain()  # Load the existing chain if available
        if not self.chain:
            self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Adjust difficulty as needed

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def load_chain(self):
        if os.path.exists("blockchain.json"):
            with open("blockchain.json", "r") as file:
                data = json.load(file)
                return [Block(b["index"], b["data"], b["prev_hash"]) for b in data]
        else:
            return None

    def save_chain(self):
        with open("blockchain.json", "w") as file:
            json.dump([block.to_dict() for block in self.chain], file, indent=4)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.prev_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_chain()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.prev_hash != prev_block.hash:
                return False
        return True

# Add blocks
def add_block(data_input):
    blockchain.add_block(Block(len(blockchain.chain), data_input, blockchain.get_latest_block().hash))

# Streamlit UI
import streamlit as st

st.title("Blockchain Santhosherium")

blockchain = Blockchain()

data_input = st.text_input("Enter Data for the New Block:")
if st.button("Add Block") and data_input:
    add_block(data_input)
    st.success("Block added successfully!")

st.header("Blockchain")
for block in blockchain.chain:
    st.subheader(f"Block {block.index}")
    st.write("Timestamp:", block.timestamp)
    st.write("Data:", block.data)
    st.write("Previous Hash:", block.prev_hash)
    st.write("Nonce:", block.nonce)
    st.write("Hash:", block.hash)
    st.write("")
