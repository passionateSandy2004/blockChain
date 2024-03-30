import hashlib
import datetime
import streamlit as st
from streamlit import session_state as state

class Block:
    def __init__(self, index, data, prev_hash):
        self.index = index
        self.timestamp = datetime.datetime.now()
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


class Blockchain:
    def __init__(self):
        self.chain = self.load_chain()  # Load the existing chain if available
        if not self.chain:
            self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Adjust difficulty as needed

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def load_chain(self):
        return state.chain if "chain" in state else None

    def save_chain(self):
        state.chain = self.chain

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

# Streamlit UI
st.title("Simple Blockchain")

if "blockchain" not in state:
    state.blockchain = Blockchain()

# Add blocks
data_input = st.text_input("Enter Data for the New Block:")
if st.button("Add Block") and data_input:
    index = len(state.blockchain.chain)
    state.blockchain.add_block(Block(index, data_input, state.blockchain.get_latest_block().hash))
    st.success("Block added successfully!")

# Display blockchain
st.header("Blockchain")
for block in state.blockchain.chain:
    st.write("---")
    st.subheader(f"Block {block.index}")
    st.write("Timestamp:", block.timestamp)
    st.write("Data:", block.data)
    st.write("Previous Hash:", block.prev_hash)
    st.write("Nonce:", block.nonce)
    st.write("Hash:", block.hash)
    st.write("")
