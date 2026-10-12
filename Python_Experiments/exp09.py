"""Ex. 9
Python: Digital Signature Standard (DSS/DSA)
AIM: To implement the Digital Signature Standard using Python and demonstrate message signing and
verification.

Theory
• DSA (Digital Signature Algorithm) is the basis of DSS (FIPS 186-4).
• DSA uses SHA hash function and public-key cryptography.
• Signing: Uses private key + random k to produce signature (r, s).
• Verification: Uses public key and signature (r, s) to verify authenticity.
• Properties: Authentication, Non-repudiation, Integrity.
• Key sizes: 1024, 2048, or 3072 bits. SHA-256 recommended."""

# ═══════════════════════════════════════════════════════
# DIGITAL SIGNATURE STANDARD (DSS/DSA) using Python
# ═══════════════════════════════════════════════════════
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

# ─── DSA IMPLEMENTATION ──────────────────────────────
class DigitalSignatureSystem:
    def __init__(self, key_size=2048):
        print(f"[*] Generating {key_size}-bit DSA key pair...")
        self.private_key = DSA.generate(key_size)
        self.public_key = self.private_key.publickey()
        print("[+] Key pair generated successfully")

    def sign(self, message: str) -> bytes:
        """Sign a message using private key"""
        msg_bytes = message.encode("utf-8")
        hasher = SHA256.new(msg_bytes)
        signer = DSS.new(self.private_key, "fips-186-3")
        signature = signer.sign(hasher)
        return signature

    def verify(self, message: str, signature: bytes) -> bool:
        """Verify signature using public key"""
        msg_bytes = message.encode("utf-8")
        hasher = SHA256.new(msg_bytes)
        verifier = DSS.new(self.public_key, "fips-186-3")
        try:
            verifier.verify(hasher, signature)
            return True
        except ValueError:
            return False

    def export_keys(self):
        """Export keys in PEM format"""
        priv_pem = self.private_key.export_key().decode()
        pub_pem = self.public_key.export_key().decode()
        return priv_pem, pub_pem

# ─── DEMONSTRATION ───────────────────────────────────
if __name__ == "__main__":
    import binascii

    dss = DigitalSignatureSystem(key_size=1024)
    # Sign original message
    message = "Transfer Rs. 50000 from Account 101 to Account 202"
    signature = dss.sign(message)
    print(f"\nOriginal Message : {message}")
    print(f"Signature (hex) : {binascii.hexlify(signature).decode()[:40]}...")
    
    # Verify original
    valid = dss.verify(message, signature)
    print(f"\n[✓] Signature Valid : {valid}")
    
    # Try with tampered message
    tampered = "Transfer Rs. 50000 from Account 101 to Account 999"
    forged = dss.verify(tampered, signature)
    print(f"[✗] Tampered Valid : {forged}")
    
    # Export keys
    priv, pub = dss.export_keys()
    print(f"\nPrivate Key (PEM):")
    print(priv[:80] + "...")
    print(f"\nPublic Key (PEM):")
    print(pub[:80] + "...")
    
    # ── RSA-based Digital Signature ──────────────────
    from Crypto.PublicKey import RSA as RSA_lib
    from Crypto.Signature import pkcs1_15
    from Crypto.Hash import SHA256 as SHA256h
    
    print("\n=== RSA Digital Signature ===")
    rsa_key = RSA_lib.generate(2048)
    rsa_pub = rsa_key.publickey()
    h = SHA256h.new(message.encode())
    sig = pkcs1_15.new(rsa_key).sign(h)
    print(f"Message : {message[:30]}...")
    print(f"Signature : {binascii.hexlify(sig)[:40].decode()}...")
    try:
        pkcs1_15.new(rsa_pub).verify(SHA256h.new(message.encode()), sig)
        print("Verification: VALID [✓]")
    except: 
        print("Verification: INVALID [✗]")
