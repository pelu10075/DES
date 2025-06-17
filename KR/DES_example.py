from DES import des_encrypt, des_decrypt, des_encrypt_cbc, des_decrypt_cbc

# ECB 모드 테스트
plaintext = "Hello DES example"
key = "mysecret"  # 64비트 키 (8바이트)

# ECB 암호화
cipher_bits = des_encrypt(plaintext, key)
print("[ECB] 암호화된 비트:", cipher_bits)

# ECB 복호화
decrypted = des_decrypt(cipher_bits, key)
print("[ECB] 복호화된 텍스트:", decrypted, '\n')

# CBC 모드 테스트
iv = [0] * 64  # 간단한 IV (모두 0)

# CBC 암호화
cbc_cipher = des_encrypt_cbc(plaintext, key, iv)
print("[CBC] 암호화된 비트:", cbc_cipher)

# CBC 복호화
cbc_plain = des_decrypt_cbc(cbc_cipher, key, iv)
print("[CBC] 복호화된 텍스트:", cbc_plain)