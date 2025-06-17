from DES import des_encrypt, des_decrypt, des_encrypt_cbc, des_decrypt_cbc

# Test for ECB mode
plaintext = "Hello DES example"
key = "mysecret"  # 64-bit key (8 bytes)

# ECB Encryption
cipher_bits = des_encrypt(plaintext, key)
print("[ECB] Encrypted bits:", cipher_bits)

# ECB Decryption
decrypted = des_decrypt(cipher_bits, key)
print("[ECB] Decrypted text:", decrypted, '\n')

# Test for CBC mode
iv = [0] * 64  # Simple IV (all zeros)

# CBC Encryption
cbc_cipher = des_encrypt_cbc(plaintext, key, iv)
print("[CBC] Encrypted bits:", cbc_cipher)

# CBC Decryption
cbc_plain = des_decrypt_cbc(cbc_cipher, key, iv)
print("[CBC] Decrypted text:", cbc_plain)