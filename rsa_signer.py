# rsa_signer.py

import rsa

class RSASigner:
    def __init__(self):
        # Generate RSA keys (512 bits for demo; for real applications use 2048+)
        self.public_key, self.private_key = rsa.newkeys(512)

    def sign(self, message: bytes) -> bytes:
        """
        Sign a message (hash) using the private key.
        """
        return rsa.sign(message, self.private_key, 'SHA-256')

    def verify(self, message: bytes, signature: bytes) -> bool:
        """
        Verify a signed message using the public key.
        """
        try:
            rsa.verify(message, signature, self.public_key)
            return True
        except rsa.VerificationError:
            return False
