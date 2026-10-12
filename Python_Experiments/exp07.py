"""Ex. 7
Python: Classical Ciphers – Caesar, Playfair, Hill, Vigenere, Rail-Fence
AIM: To implement classical substitution and transposition techniques in Python.

7a. Caesar Cipher
Caesar Cipher shifts each letter by a fixed key k (0-25). Encryption: C = (P + k) mod 26. Decryption: P = (C - k)
mod 26."""
import math
import numpy as np

# ═══════════════════════════════════════════════════════
# CAESAR CIPHER
# ═══════════════════════════════════════════════════════
def caesar_encrypt(plaintext, key):
    result = ""
    for ch in plaintext.upper():
        if ch.isalpha():
            result += chr((ord(ch) - ord('A') + key) % 26 + ord('A'))
        else:
            result += ch
    return result

def caesar_decrypt(ciphertext, key):
    return caesar_encrypt(ciphertext, 26 - key)

if __name__ == "__main__":
    plaintext = "HELLO WORLD"
    key = 3
    cipher = caesar_encrypt(plaintext, key)
    plain = caesar_decrypt(cipher, key)
    print(f"Plaintext : {plaintext}")
    print(f"Key : {key}")
    print(f"Ciphertext : {cipher}")
    print(f"Decrypted : {plain}")

# 7b. Playfair Cipher
# Playfair encrypts digraphs (pairs of letters) using a 5×5 key matrix. Rules: Same row → shift right; same column
# → shift down; otherwise → rectangle swap.

# ═══════════════════════════════════════════════════════
# PLAYFAIR CIPHER
# ═══════════════════════════════════════════════════════

def create_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    seen, matrix = set(), []
    for ch in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in seen and ch.isalpha():
            seen.add(ch)
            matrix.append(ch)
    return [matrix[i*5:(i+1)*5] for i in range(5)]

def find_pos(matrix, ch):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch: 
                return (r, c)

def prepare_text(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    result, i = "", 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"
        if a == b: 
            b = "X"
            i += 1
        else: 
            i += 2
        result += a + b
    return result if len(result)%2==0 else result+"X"

def playfair_encrypt(plaintext, key):
    matrix = create_playfair_matrix(key)
    text = prepare_text(plaintext)
    cipher = ""
    for i in range(0, len(text), 2):
        r1,c1 = find_pos(matrix, text[i])
        r2,c2 = find_pos(matrix, text[i+1])
        if r1 == r2:
            cipher += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:
            cipher += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            cipher += matrix[r1][c2] + matrix[r2][c1]
    return cipher

def playfair_decrypt(ciphertext, key):
    matrix = create_playfair_matrix(key)
    plain = ""
    for i in range(0, len(ciphertext), 2):
        r1,c1 = find_pos(matrix, ciphertext[i])
        r2,c2 = find_pos(matrix, ciphertext[i+1])
        if r1 == r2:
            plain += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
        elif c1 == c2:
            plain += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
        else:
            plain += matrix[r1][c2] + matrix[r2][c1]
    return plain

key = "MONARCHY"
plaintext = "INSTRUMENTS"
cipher = playfair_encrypt(plaintext, key)
print(f"\nPlayfair Cipher:")
print(f"Plaintext : {plaintext}")
print(f"Key : {key}")
print(f"Ciphertext : {cipher}")
print(f"Decrypted : {playfair_decrypt(cipher, key)}")

# 7c. Hill Cipher
# Hill Cipher encrypts blocks of n letters using an n×n invertible key matrix. C = K × P (mod 26). Requires matrix
# inverse mod 26 for decryption.

# ═══════════════════════════════════════════════════════
# HILL CIPHER (2x2 matrix)
# ═══════════════════════════════════════════════════════

def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1: 
            return i
    return None

def matrix_mod_inverse(matrix, mod):
    det = int(round(np.linalg.det(matrix))) % mod
    det_inv = mod_inverse(det % mod, mod)
    adj = np.array([[matrix[1][1], -matrix[0][1]],
                    [-matrix[1][0], matrix[0][0]]])
    return (det_inv * adj % mod + mod) % mod

def hill_encrypt(plaintext, key_matrix):
    text = plaintext.upper().replace(" ", "")
    if len(text) % 2 != 0: 
        text += "X"
    cipher = ""
    for i in range(0, len(text), 2):
        pair = np.array([[ord(text[i])-65],[ord(text[i+1])-65]])
        result = np.dot(key_matrix, pair) % 26
        cipher += chr(int(result[0][0])+65) + chr(int(result[1][0])+65)
    return cipher

def hill_decrypt(ciphertext, key_matrix):
    inv_key = matrix_mod_inverse(key_matrix, 26)
    return hill_encrypt(ciphertext, inv_key)

# 2x2 Key Matrix (must be invertible mod 26)
key = np.array([[3, 3], [2, 5]])
plaintext = "HELP"
cipher = hill_encrypt(plaintext, key)
decrypted = hill_decrypt(cipher, key)
print(f"\nHill Cipher:")
print(f"Plaintext : {plaintext}")
print(f"Key Matrix : {key.tolist()}")
print(f"Ciphertext : {cipher}")
print(f"Decrypted : {decrypted}")

# 7d. Vigenere Cipher
# Vigenere Cipher uses a keyword repeated to match plaintext length. Each letter shifted by corresponding keyword
# letter. C[i] = (P[i] + K[i]) mod 26.

# ═══════════════════════════════════════════════════════
# VIGENERE CIPHER
# ═══════════════════════════════════════════════════════

def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.upper()
    key = key.upper()
    result, k = "", 0
    for ch in plaintext:
        if ch.isalpha():
            shift = ord(key[k % len(key)]) - ord('A')
            result += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
            k += 1
        else:
            result += ch
    return result

def vigenere_decrypt(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = key.upper()
    result, k = "", 0
    for ch in ciphertext:
        if ch.isalpha():
            shift = ord(key[k % len(key)]) - ord('A')
            result += chr((ord(ch) - ord('A') - shift + 26) % 26 + ord('A'))
            k += 1
        else:
            result += ch
    return result

plaintext = "ATTACK AT DAWN"
key = "LEMON"
cipher = vigenere_encrypt(plaintext, key)
print(f"\nVigenere Cipher:")
print(f"Plaintext : {plaintext}")
print(f"Key : {key}")
print(f"Ciphertext : {cipher}")
print(f"Decrypted : {vigenere_decrypt(cipher, key)}")

# 7e. Rail Fence & Row-Column Transposition

# ═══════════════════════════════════════════════════════
# RAIL FENCE CIPHER (Zig-Zag)
# ═══════════════════════════════════════════════════════

def rail_fence_encrypt(text, rails):
    fence = [[] for _ in range(rails)]
    rail, direction = 0, 1
    for ch in text:
        fence[rail].append(ch)
        if rail == 0: 
            direction = 1
        elif rail == rails - 1: 
            direction = -1
        rail += direction
    return ''.join(''.join(r) for r in fence)

def rail_fence_decrypt(cipher, rails, length=None):
    if length is None: 
        length = len(cipher)
    pattern = []
    rail, direction = 0, 1
    for i in range(length):
        pattern.append(rail)
        if rail == 0: 
            direction = 1
        elif rail == rails - 1: 
            direction = -1
        rail += direction
    indices = sorted(range(length), key=lambda x: (pattern[x], x))
    result = [""] * length
    for pos, idx in zip(indices, cipher):
        result[pos] = idx
    return ''.join(result)

text = "WEAREDISCOVEREDFLEEATONCE"
rails = 3
cipher = rail_fence_encrypt(text, rails)
print(f"\nRail Fence Cipher:")
print(f"Plaintext : {text}")
print(f"Rails : {rails}")
print(f"Ciphertext : {cipher}")
print(f"Decrypted : {rail_fence_decrypt(cipher, rails)}")

# ═══════════════════════════════════════════════════════
# ROW-COLUMN TRANSPOSITION CIPHER
# ═══════════════════════════════════════════════════════

def col_transposition_encrypt(text, key):
    text = text.replace(" ", "").upper()
    cols = len(key)
    rows = math.ceil(len(text) / cols)
    text = text.ljust(rows * cols, 'X') # pad
    order = sorted(range(cols), key=lambda x: key[x])
    # Build grid
    grid = [list(text[r*cols:(r+1)*cols]) for r in range(rows)]
    # Read columns in key order
    return ''.join(''.join(grid[r][c] for r in range(rows)) for c in order)

def col_transposition_decrypt(cipher, key):
    cols = len(key)
    rows = len(cipher) // cols
    order = sorted(range(cols), key=lambda x: key[x])
    col_lens = [rows] * cols
    # Fill grid columns
    grid = [[""] * cols for _ in range(rows)]
    idx = 0
    for c in order:
        for r in range(rows):
            grid[r][c] = cipher[idx]
            idx += 1
    return ''.join(''.join(row) for row in grid)

text = "ATTACKPOSTPONEDUNTILTWOAM"
key = "ZEBRAS" # Keyword determines column order
cipher = col_transposition_encrypt(text, key)
print(f"\nRow-Column Transposition:")
print(f"Plaintext : {text}")
print(f"Key : {key}")
print(f"Ciphertext : {cipher}")
print(f"Decrypted : {col_transposition_decrypt(cipher, key)}")
