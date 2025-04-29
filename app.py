import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import ttkbootstrap as ttk
from blockchain import Blockchain
from rsa_signer import RSASigner
from document_hasher import hash_document
import os
import pickle



class BlockchainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Project - Blockchain Document Verifier")
        self.root.geometry("900x600")
        self.root.config(bg="#f0f0f0")

        self.selected_blockchain = None
        self.blockchain_list = []
        self.rsa_signer = RSASigner()

        self.setup_gui()
        self.load_blockchains()

    def setup_gui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ttk.Frame(self.main_frame, width=200, relief="solid")
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        self.main_content = ttk.Frame(self.main_frame)
        self.main_content.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.manage_blockchain_btn = ttk.Button(self.sidebar, text="Manage Blockchain", command=self.show_manage_blockchain)
        self.manage_blockchain_btn.pack(fill="x", pady=10)

        self.manage_files_btn = ttk.Button(self.sidebar, text="Manage Files", command=self.show_manage_files)
        self.manage_files_btn.pack(fill="x", pady=10)

        self.tab_control = ttk.Notebook(self.main_content)
        self.tab_manage = ttk.Frame(self.tab_control)
        self.tab_home = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_manage, text="")
        self.tab_control.add(self.tab_home, text="")
        self.tab_control.pack(fill="both", expand=True)

        # Remove the tab headers
        style = ttk.Style()
        style.layout("TNotebook.Tab", [])  # Totally remove tabs
        style.configure("TNotebook", padding=0)

        self.setup_manage_blockchain_tab()
        self.setup_manage_files_tab()
        self.setup_manage_files_tab()

    def setup_manage_blockchain_tab(self):
        # Header
        header_frame = ttk.Frame(self.tab_manage)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 5))
        header_label = ttk.Label(header_frame, text="Manage Blockchain", font=("Arial", 16, "bold"))
        header_label.pack()

        separator = ttk.Separator(self.tab_manage, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.create_blockchain_btn = ttk.Button(self.tab_manage, text="Create Blockchain", command=self.create_blockchain)
        self.create_blockchain_btn.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        self.blockchain_listbox = ttk.Treeview(self.tab_manage, columns=("Blockchains"), show="headings", height=20)
        self.blockchain_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.blockchain_listbox.heading("Blockchains", text="Blockchains")
        self.blockchain_listbox.column("Blockchains", width=200, anchor="center", stretch=False)
        self.blockchain_listbox.bind("<ButtonRelease-3>", self.show_context_menu)
        self.blockchain_listbox.bind("<Double-1>", self.select_blockchain)

        self.tab_manage.grid_rowconfigure(3, weight=1)
        self.tab_manage.grid_columnconfigure(0, weight=1)

    def setup_manage_files_tab(self):
        # Header
        header_frame = ttk.Frame(self.tab_home)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(10, 5))

        self.selected_blockchain_label = ttk.Label(header_frame, text="Selected blockchain: None", font=("Arial", 12, "bold"))
        self.selected_blockchain_label.pack(side="left", padx=(10, 20))

        self.status_label = ttk.Label(header_frame, text="Status: Not Verified", font=("Arial", 12, "bold"))
        self.status_label.pack(side="left")

        separator = ttk.Separator(self.tab_home, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=4, sticky="ew")

        # Buttons
        self.add_file_btn = ttk.Button(self.tab_home, text="Add File(s)", command=self.add_files)
        self.add_file_btn.grid(row=2, column=0, padx=10, pady=10)

        self.remove_file_btn = ttk.Button(self.tab_home, text="Remove File", command=self.remove_file)
        self.remove_file_btn.grid(row=2, column=1, padx=10, pady=10)

        self.save_blockchain_btn = ttk.Button(self.tab_home, text="Save Blockchain", command=self.save_blockchain)
        self.save_blockchain_btn.grid(row=2, column=2, padx=10, pady=10)

        self.verify_blockchain_btn = ttk.Button(self.tab_home, text="Verify Blockchain", command=self.verify_blockchain)
        self.verify_blockchain_btn.grid(row=2, column=3, padx=10, pady=10)

        # Files Table
        self.file_listbox = ttk.Treeview(self.tab_home, columns=("Files", "Hash", "Signature"), show="headings")
        self.file_listbox.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.file_listbox.heading("Files", text="Files")
        self.file_listbox.heading("Hash", text="Hash")
        self.file_listbox.heading("Signature", text="Signature")

        self.tab_home.grid_rowconfigure(3, weight=1)
        self.tab_home.grid_columnconfigure(0, weight=1)

    def show_manage_blockchain(self):
        self.tab_control.select(self.tab_manage)

    def show_manage_files(self):
        self.tab_control.select(self.tab_home)

    def load_blockchains(self):
        if not os.path.exists("blockchains"):
            os.makedirs("blockchains")
        self.blockchain_list = [f for f in os.listdir("blockchains") if f.endswith(".pkl")]
        self.update_blockchain_list()

    def update_blockchain_list(self):
        for item in self.blockchain_listbox.get_children():
            self.blockchain_listbox.delete(item)
        for blockchain in self.blockchain_list:
            self.blockchain_listbox.insert("", "end", values=(blockchain,))

    def update_file_list(self):
        for item in self.file_listbox.get_children():
            self.file_listbox.delete(item)
        if self.selected_blockchain:
            for block in self.selected_blockchain.chain[1:]:
                file_name = os.path.basename(block.data["file_name"])
                file_hash = block.data["file_hash"]
                file_signature = block.data["signature"]
                self.file_listbox.insert("", "end", values=(file_name, file_hash, file_signature))

    def show_context_menu(self, event):
        selected_item = self.blockchain_listbox.identify_row(event.y)
        if selected_item:
            self.blockchain_listbox.selection_set(selected_item)
            menu = ttk.Menu(self.root, tearoff=0)
            menu.add_command(label="Select", command=self.select_blockchain)
            menu.add_command(label="Rename", command=self.rename_blockchain)
            menu.add_command(label="Delete", command=self.delete_blockchain)
            menu.post(event.x_root, event.y_root)

    def create_blockchain(self):
        blockchain_name = simpledialog.askstring("Blockchain Name", "Enter the blockchain name:")
        if blockchain_name:
            blockchain_path = os.path.join("blockchains", f"{blockchain_name}.pkl")
            new_blockchain = Blockchain(blockchain_name)
            with open(blockchain_path, "wb") as f:
                pickle.dump(new_blockchain, f)
            self.blockchain_list.append(f"{blockchain_name}.pkl")
            self.update_blockchain_list()

    def select_blockchain(self, event=None):
        selected_item = self.blockchain_listbox.selection()
        if selected_item:
            blockchain_name = self.blockchain_listbox.item(selected_item[0], "values")[0]
            blockchain_path = os.path.join("blockchains", blockchain_name)
            with open(blockchain_path, "rb") as f:
                self.selected_blockchain = pickle.load(f)
            self.selected_blockchain_label.config(text=f"Selected blockchain: {self.selected_blockchain.name}")
            self.status_label.config(text="Status: Not Verified")
            self.update_file_list()
            self.tab_control.select(self.tab_home)

    def rename_blockchain(self):
        selected_item = self.blockchain_listbox.selection()
        if selected_item:
            old_name = self.blockchain_listbox.item(selected_item[0], "values")[0]
            new_name = simpledialog.askstring("Rename Blockchain", f"Enter a new name for {old_name}:")
            if new_name:
                os.rename(os.path.join("blockchains", old_name), os.path.join("blockchains", f"{new_name}.pkl"))
                self.load_blockchains()

    def delete_blockchain(self):
        selected_item = self.blockchain_listbox.selection()
        if selected_item:
            blockchain_name = self.blockchain_listbox.item(selected_item[0], "values")[0]
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {blockchain_name}?"):
                os.remove(os.path.join("blockchains", blockchain_name))
                self.load_blockchains()

    def add_files(self):
        if self.selected_blockchain:
            files = filedialog.askopenfilenames(title="Select Files")
            for file in files:
                file_hash = hash_document(file)
                if file_hash:
                    new_block = self.selected_blockchain.add_block(file, file_hash)
                    # Sign the block after adding
                    new_block.data["signature"] = self.rsa_signer.sign(new_block.hash.encode())
            self.selected_blockchain.refresh()
            self.save_blockchain()
            self.update_file_list()
            self.status_label.config(text="Added and saved files successfully.")

    def remove_file(self):
        if self.selected_blockchain:
            top = tk.Toplevel(self.root)
            top.title("Remove File")
            top.geometry("300x150")
            tk.Label(top, text="Select file to remove:").pack(pady=10)

            file_names = [os.path.basename(block.data["file_name"]) for block in self.selected_blockchain.chain[1:]]

            selected_file = tk.StringVar()
            file_dropdown = ttk.Combobox(top, textvariable=selected_file, values=file_names, state="readonly")
            file_dropdown.pack(pady=5)

            def confirm_removal():
                file_to_remove = selected_file.get()
                if file_to_remove:
                    for block in self.selected_blockchain.chain[1:]:
                        if os.path.basename(block.data["file_name"]) == file_to_remove:
                            self.selected_blockchain.chain.remove(block)
                            break
                    self.selected_blockchain.refresh()
                    self.save_blockchain()
                    self.update_file_list()
                    self.status_label.config(text=f"Removed and saved file: {file_to_remove}")
                    top.destroy()

            ttk.Button(top, text="Remove", command=confirm_removal).pack(pady=10)

    def save_blockchain(self):
        if self.selected_blockchain:
            # Recalculate the hash for modified files
            for block in self.selected_blockchain.chain[1:]:
                # Check if file has changed and recalculate its hash
                new_hash = hash_document(block.data["file_name"])
                if new_hash != block.data["file_hash"]:  # If the hash has changed
                    block.data["file_hash"] = new_hash
                    block.data["signature"] = self.rsa_signer.sign(block.hash.encode())  # Re-sign the block

            # Refresh the blockchain to reflect any changes
            self.selected_blockchain.refresh()

            # Save the blockchain to file
            with open(os.path.join("blockchains", f"{self.selected_blockchain.name}.pkl"), "wb") as f:
                pickle.dump(self.selected_blockchain, f)

            # Update the file list in the GUI to show changes
            self.update_file_list()

            # Update status message
            self.status_label.config(text="Blockchain saved successfully.")

            self.selected_blockchain.refresh()
            with open(os.path.join("blockchains", f"{self.selected_blockchain.name}.pkl"), "wb") as f:
                pickle.dump(self.selected_blockchain, f)
            self.status_label.config(text="Blockchain saved successfully.")

    def verify_blockchain(self):
        if self.selected_blockchain:
            valid = self.selected_blockchain.is_chain_valid()
            if valid:
                self.status_label.config(text="Blockchain is valid!")
            else:
                self.status_label.config(text="Blockchain is invalid!")

# Running the app
root = ttk.Window(themename="superhero")
app = BlockchainApp(root)
root.mainloop()
