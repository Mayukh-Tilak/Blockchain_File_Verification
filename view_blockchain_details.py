import os
import pickle

BLOCKCHAINS_DIR = "blockchains"


def load_blockchain(file_path):
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Failed to load blockchain {file_path}: {e}")
        return None


def display_blockchain_details(blockchain, name):
    print(f"\n=== Blockchain: {name} ===")
    for i, block in enumerate(blockchain.chain):
        if i == 0:
            print(f"\nGenesis Block:")
        else:
            print(f"\nBlock #{i}:")

        file_name = block.data.get("file_name", "N/A")
        file_hash = block.data.get("file_hash", "N/A")
        signature = block.data.get("signature", "N/A")

        print(f"  File       : {os.path.basename(file_name)}")
        print(f"  File Hash  : {file_hash}")
        print(f"  Signature  : {signature}")


def main():
    if not os.path.exists(BLOCKCHAINS_DIR):
        print("No 'blockchains/' directory found.")
        return

    blockchain_files = [f for f in os.listdir(BLOCKCHAINS_DIR) if f.endswith(".pkl")]

    if not blockchain_files:
        print("No blockchain files found.")
        return

    for filename in blockchain_files:
        path = os.path.join(BLOCKCHAINS_DIR, filename)
        blockchain = load_blockchain(path)
        if blockchain:
            display_blockchain_details(blockchain, filename)


if __name__ == "__main__":
    main()
