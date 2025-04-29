import hashlib
import time
import os
from document_hasher import hash_document  # Correct import
from rsa_signer import RSASigner

signer = RSASigner()  # RSA signer instance

class Block:
    def __init__(self, index, previous_hash, timestamp, data, signature=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data  # Dictionary: {file_name, file_hash}
        self.hash = self.calculate_hash()
        self.signature = signature if signature else signer.sign(self.hash.encode())

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{str(self.data)}"
        return hashlib.sha256(block_string.encode("utf-8")).hexdigest()

class Blockchain:
    def __init__(self, name):
        self.name = name
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        timestamp = time.time()
        genesis_data = {"info": "Genesis Block"}
        genesis_block = Block(0, "0", timestamp, genesis_data)
        self.chain.append(genesis_block)

    def add_block(self, file_name, file_hash):
        if not file_name or not file_hash:
            raise ValueError("File name and hash must be provided.")

        last_block = self.chain[-1]
        new_index = last_block.index + 1
        new_timestamp = time.time()
        block_data = {"file_name": file_name, "file_hash": file_hash}
        new_block = Block(new_index, last_block.hash, new_timestamp, block_data)
        self.chain.append(new_block)
        return new_block

    def remove_file(self, file_name):
        """
        Removes a file block from the blockchain if found.
        """
        for block in self.chain[1:]:  # Skip Genesis Block
            if isinstance(block.data, dict) and block.data.get('file_name') == file_name:
                self.chain.remove(block)
                self.refresh()  # Recalculate and refresh blockchain
                return block  # Returning the removed block
        return None

    def refresh(self):
        """
        Refreshes the blockchain: reindexes, relinks hashes, and recalculates hashes and signatures.
        """
        for i in range(len(self.chain)):
            if i == 0:
                self.chain[i].index = 0
                self.chain[i].previous_hash = "0"
            else:
                self.chain[i].index = i
                self.chain[i].previous_hash = self.chain[i-1].hash
            self.chain[i].hash = self.chain[i].calculate_hash()
            self.chain[i].signature = signer.sign(self.chain[i].hash.encode())

    def is_chain_valid(self):
        """
        Verifies the blockchain:
        - Correct linkage between blocks
        - Correct file hash on disk
        - Correct block hashes
        - Valid digital signatures
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Check previous hash link
            if current_block.previous_hash != previous_block.hash:
                return False

            # Check block's own hash
            if current_block.hash != current_block.calculate_hash():
                return False

            # Verify the digital signature
            if not signer.verify(current_block.hash.encode(), current_block.signature):
                return False

            # Check file integrity
            if isinstance(current_block.data, dict):
                file_path = current_block.data.get('file_name')
                expected_file_hash = current_block.data.get('file_hash')

                if not file_path or not expected_file_hash:
                    return False

                if not os.path.exists(file_path):
                    return False  # File missing

                current_file_hash = hash_document(file_path)
                if current_file_hash != expected_file_hash:
                    return False  # File contents modified

        return True
