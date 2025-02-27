# -*- coding: utf-8 -*-
"""dsp_ca.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BujIuGnGpLk9NgcqKFlYnyjNCJVy_c3z
"""

!pip install cryptography

"""# PS4

## AES CBC
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

def encrypt_text(plain_text: str, key: bytes) -> (bytes, bytes):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()

    return cipher_text, iv

def decrypt_text(cipher_text: bytes, iv: bytes, key: bytes) -> str:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded_plain_text = decryptor.update(cipher_text) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plain_text = unpadder.update(padded_plain_text) + unpadder.finalize()

    return plain_text.decode()

if __name__ == "__main__":
    key = os.urandom(32)
    plain_text = "This is a secret message."
    cipher_text, iv = encrypt_text(plain_text, key)
    print(f"Encrypted: {cipher_text}")
    decrypted_text = decrypt_text(cipher_text, iv, key)
    print(f"Decrypted: {decrypted_text}")

algorithms.AES.block_size



256/8

"""## AES ECB"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

def encrypt_text_ecb(plain_text: str, key: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()

    return cipher_text

def decrypt_text_ecb(cipher_text: bytes, key: bytes) -> str:
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()

    padded_plain_text = decryptor.update(cipher_text) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plain_text = unpadder.update(padded_plain_text) + unpadder.finalize()

    return plain_text.decode()

if __name__ == "__main__":
    key = os.urandom(32)  # 256-bit key for AES
    plain_text = "This is a secret message."
    cipher_text = encrypt_text_ecb(plain_text, key)
    print(f"Encrypted (ECB): {cipher_text}")
    decrypted_text = decrypt_text_ecb(cipher_text, key)
    print(f"Decrypted (ECB): {decrypted_text}")

"""## AES CFB"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def encrypt_text_cfb(plain_text: str, key: bytes) -> (bytes, bytes):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()

    cipher_text = encryptor.update(plain_text.encode()) + encryptor.finalize()

    return cipher_text, iv

def decrypt_text_cfb(cipher_text: bytes, iv: bytes, key: bytes) -> str:
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()

    plain_text = decryptor.update(cipher_text) + decryptor.finalize()

    return plain_text.decode()

if __name__ == "__main__":
    key = os.urandom(32)  # 256-bit key for AES
    plain_text = "XXAABBXXAABB"
    cipher_text, iv = encrypt_text_cfb(plain_text, key)
    print(f"Encrypted (CFB): {cipher_text}")
    decrypted_text = decrypt_text_cfb(cipher_text, iv, key)
    print(f"Decrypted (CFB): {decrypted_text}")

13 ** 27 % 55



"""# PS5

## P1
"""

n = 35
e = 3

plain_text = 8
encrypt_text = 8 ** e % n
print(encrypt_text)

def cycle_attack(n, e, c):
    prev = c
    curr = c

    counter = 100

    while counter > 0:
        print(prev, curr)
        prev = curr
        curr = (curr ** e) % n
        if curr == c:
            return prev

        counter -= 1

    return False

ans = cycle_attack(n, e, 22 ** e % n)

ans

# Given values
C = 22
e = 3
n = 35

# Function to perform RSA encryption
def rsa_encrypt(C, e, n):
    return pow(C, e, n)

# Start with the initial ciphertext
ciphertext = C
cycle = [ciphertext]

# Perform cycling attack
for _ in range(10):  # Limiting to 10 steps to detect a cycle
    ciphertext = rsa_encrypt(ciphertext, e, n)
    if ciphertext in cycle:
        break
    cycle.append(ciphertext)

# Output the cycle and the plaintext
print("Cycle Detected:", cycle)
print("Plaintext (P):", cycle[-1])

def encrypt(plaintext, e, n):
    return pow(plaintext, e, n)

def decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)

def chosen_cipher_attack(intercepted_ciphertext, e, n, bob_decrypt):
    X = random.randint(1, n-1)
    while math.gcd(X, n) != 1:
        X = random.randint(1, n-1)

    Y = (intercepted_ciphertext * pow(X, e, n)) % n
    Z = bob_decrypt(Y)
    plaintext =(Z * pow(X, -1, n)) % n

    return plaintext

def bob_decrypt(ciphertext):
    d = 103
    return decrypt(ciphertext, d, n)

# Given parameters
e = 7
n = 143
intercepted_ciphertext = 57

recovered_plaintext = chosen_cipher_attack(intercepted_ciphertext, e, n, bob_decrypt)
plaintext = 8

if recovered_plaintext == plaintext:
    print("Success..")
else:
    print("Failure..")