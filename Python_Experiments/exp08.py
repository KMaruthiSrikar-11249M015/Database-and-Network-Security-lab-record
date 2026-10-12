"""Ex. 8
Python: DES, RSA, Diffie-Hellman, MD5, SHA-1
AIM: To implement symmetric (DES), asymmetric (RSA, Diffie-Hellman) encryption algorithms and hash
functions (MD5, SHA-1) using Python.
Installation: pip install pycryptodome
8a. DES (Data Encryption Standard)
DES is a symmetric block cipher using a 64-bit key (56-bit effective) operating on 64-bit blocks. Uses 16 rounds
of Feistel network.
"""
# pip install pycryptodome
# ═══════════════════════════════════════════════════════
# DES ENCRYPTION / DECRYPTION
# ═══════════════════════════════════════════════════════
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii

def des_encrypt(plaintext: str, key: bytes) -> bytes:
    cipher = DES.new(key, DES.MODE_CBC)
    ct = cipher.encrypt(pad(plaintext.encode(), DES.block_size))
    return cipher.iv + ct # Prepend IV

def des_decrypt(ciphertext: bytes, key: bytes) -> str:
    iv = ciphertext[:8]
    ct = ciphertext[8:]
    cipher = DES.new(key, DES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(ct), DES.block_size).decode()

if __name__ == "__main__":
    key = b"8BYTEKEY" # DES key must be exactly 8 bytes
    plaintext = "Hello DES Algorithm!"
    encrypted = des_encrypt(plaintext, key)
    decrypted = des_decrypt(encrypted, key)
    print("DES Encryption Demo")
    print(f"Plaintext : {plaintext}")
    print(f"Key : {key}")
    print(f"Ciphertext : {binascii.hexlify(encrypted).decode()}")
    print(f"Decrypted : {decrypted}")

"""8b. RSA Algorithm
RSA is an asymmetric algorithm. Key generation: choose primes p, q; n = p×q; φ(n) = (p-1)(q-1); choose e with
gcd(e,φ)=1; find d = e−1 mod φ. Encryption: C = Me mod n. Decryption: M = Cd mod n."""

# ═══════════════════════════════════════════════════════
# RSA ALGORITHM - Manual Implementation + pycryptodome
# ═══════════════════════════════════════════════════════
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

# ── Manual RSA for educational understanding ──

def gcd(a, b):
    while b: 
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    def extended_gcd(a, b):
        if b == 0: 
            return a, 1, 0
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (a // b) * y
    _, x, _ = extended_gcd(e, phi)
    return x % phi

def rsa_manual(p=61, q=53):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17 # Public exponent (gcd(e,phi)=1)
    assert gcd(e, phi) == 1
    d = mod_inverse(e, phi) # Fixed: d must be calculated mod phi, not n
    msg = 65 # Encrypt number 65
    C = pow(msg, e, n)
    M = pow(C, d, n)
    print(f" p={p}, q={q}, n={n}, phi={phi}")
    print(f" Public Key (e={e}, n={n})")
    print(f" Private Key (d={d}, n={n})")
    print(f" Message={msg} Ciphertext={C} Decrypted={M}")

# ── Library-based RSA (secure, 2048-bit) ──
def rsa_library():
    key = RSA.generate(2048)
    pub_key = key.publickey()
    cipher = PKCS1_OAEP.new(pub_key)
    msg = b"RSA Encryption Test - SCSVMV"
    ct = cipher.encrypt(msg)
    dec_cipher = PKCS1_OAEP.new(key)
    pt = dec_cipher.decrypt(ct)
    print(f" Original : {msg.decode()}")
    print(f" Encrypted : {binascii.hexlify(ct)[:40]}...")
    print(f" Decrypted : {pt.decode()}")

print("=== Manual RSA (p=61, q=53) ===")
rsa_manual()
print("\n=== RSA with 2048-bit keys (Library) ===")
rsa_library()

"""8c. Diffie-Hellman Key Exchange
Diffie-Hellman allows two parties to establish a shared secret over a public channel. Public: prime p and base g.
Private keys: a (Alice), b (Bob). Shared: A = ga mod p; B = gb mod p; Secret = Ba mod p = Ab mod p."""

# ═══════════════════════════════════════════════════════
# DIFFIE-HELLMAN KEY EXCHANGE
# ═══════════════════════════════════════════════════════
import random

def diffie_hellman():
    # Public parameters (agreed publicly)
    p = 23 # Small prime for demo (use 2048-bit in real)
    g = 5 # Primitive root (generator)
    # Alice chooses private key a
    a = random.randint(2, p - 2) # Private
    A = pow(g, a, p) # Public value A = g^a mod p
    # Bob chooses private key b
    b = random.randint(2, p - 2) # Private
    B = pow(g, b, p) # Public value B = g^b mod p
    # Exchange public values A and B (sent over network)
    # Alice computes shared secret
    secret_A = pow(B, a, p) # B^a mod p
    # Bob computes shared secret
    secret_B = pow(A, b, p) # A^b mod p
    print("\nDiffie-Hellman Key Exchange")
    print(f" Public prime (p) : {p}")
    print(f" Generator (g) : {g}")
    print(f" Alice private (a): {a} Public A: {A}")
    print(f" Bob private (b): {b} Public B: {B}")
    print(f" Alice shared key : {secret_A}")
    print(f" Bob shared key : {secret_B}")
    print(f" Keys Match : {secret_A == secret_B}")

diffie_hellman()

"""8d. MD5 and 8e. SHA-1
MD5 produces a 128-bit hash. SHA-1 produces a 160-bit hash. Both are one-way functions — output cannot be
reversed to input. Used for integrity verification."""

# ═══════════════════════════════════════════════════════
# MD5 and SHA-1 HASH FUNCTIONS
# ═══════════════════════════════════════════════════════
import hashlib

def hash_demo(message: str):
    data = message.encode("utf-8")
    md5 = hashlib.md5(data).hexdigest()
    sha1 = hashlib.sha1(data).hexdigest()
    sha256 = hashlib.sha256(data).hexdigest()
    print(f"\nMessage : {message}")
    print(f"MD5 : {md5} ({len(md5)*4} bits)")
    print(f"SHA-1 : {sha1} ({len(sha1)*4} bits)")
    print(f"SHA-256 : {sha256} ({len(sha256)*4} bits)")

def verify_integrity(file_content: str):
    original_hash = hashlib.md5(file_content.encode()).hexdigest()
    print(f"\nFile integrity check:")
    print(f"Original MD5 : {original_hash}")
    # Tamper with content
    tampered = file_content + " (modified)"
    tampered_hash = hashlib.md5(tampered.encode()).hexdigest()
    print(f"Tampered MD5 : {tampered_hash}")
    print(f"Integrity OK : {original_hash == tampered_hash}")

# Demonstrate avalanche effect
def avalanche_effect():
    print("\nAvalanche Effect (tiny change → huge hash change):")
    m1 = "Hello"
    m2 = "hello" # Only case changed
    print(f"SHA1('{m1}') = {hashlib.sha1(m1.encode()).hexdigest()}")
    print(f"SHA1('{m2}') = {hashlib.sha1(m2.encode()).hexdigest()}")

hash_demo("SCSVMV University")
verify_integrity("Sensitive Document Content")
avalanche_effect()
