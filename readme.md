# 🔐 Blockchain Document Verifier

A desktop application that uses blockchain principles, SHA256 hashing, and RSA digital signatures to securely manage and verify the integrity of files. Built with Python and a modern Tkinter GUI using `ttkbootstrap`.

---

## 📦 Features

- Add files to a blockchain with SHA256 hashes
- Generate and attach RSA digital signatures for each file
- Detect tampering by verifying file integrity
- View a list of files in the blockchain with their hash and signature
- Save, load, rename, and delete blockchain instances
- Easy-to-use graphical interface

---

## 🖼️ GUI Overview

The app has two main tabs:
- **Manage Blockchain** – Create, select, rename, or delete blockchain instances.
- **Manage Files** – Add, remove, save, and verify files in a selected blockchain.

---

## 📂 Project Structure

```
crypto_project/
│
├── blockchains/              # Stored .pkl blockchain files
├── app.py                    # Main GUI application
├── blockchain.py             # Blockchain and block data structures
├── document_hasher.py        # Utility for hashing files
├── rsa_signer.py             # RSA key generation, signing, and verification
├── view_blockchain_details.py# Optional script to inspect blockchain contents
├── requirements.txt          # Project dependencies
└── readme.md                 # You're here!
```

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/crypto_project.git
   cd crypto_project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

---

## 📑 Dependencies

- `ttkbootstrap`
- `pycryptodome`  
*(See `requirements.txt`)*

---

## 🔐 How It Works

- Each file added is stored in a new block with:
  - Its file path
  - SHA256 hash of its contents
  - RSA signature of the block hash
- Changing the file later results in a different hash/signature, so tampering can be detected.
- Blocks are linked like a traditional blockchain with each one storing the hash of the previous block.

---

## ✅ Blockchain Verification

Click the **"Verify Blockchain"** button in the GUI. This will:
- Check that hashes match the file contents
- Confirm that block hashes are correct
- Validate the RSA signatures

---

## 📎 License

MIT License. Feel free to use and modify this project for learning or building upon.

---

## ✍️ Author

Developed by Mayukh Tilak. Inspired by blockchain principles applied to document integrity and file security.
