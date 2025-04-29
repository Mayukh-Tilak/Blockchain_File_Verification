# document_hasher.py

import hashlib


def hash_document(filepath):
    """
    Compute the SHA-256 hash of a file.

    :param filepath: Full path to the file
    :return: SHA-256 hash as a hexadecimal string
    """
    sha256_hash = hashlib.sha256()

    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
    except FileNotFoundError:
        return None

    return sha256_hash.hexdigest()
