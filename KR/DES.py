# === 구성 ===
# [1] 비트 처리 함수 구현
# [2] 테이블 정의
# [3] 키 스케줄 생성
# [4] f 함수 구현
# [5] 암호화 라운드 구현
# [6] 복호화 라운드 구현
# [7] 패딩 및 문자열 처리
# [8] EBC 인코딩, 디코딩
# [9] CBC 모드
# ============

import DES_table as t # part 2

# part 1
def permute(bits: list[int], table: list[int]) -> list[int]:
    return [bits[i - 1] for i in table]

def xor(bits1: list[int], bits2: list[int]) -> list[int]:
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def int_to_bitlist(n: int, bits: int) -> list[int]:
    return [int(b) for b in format(n, f'0{bits}b')]

def bitlist_to_int(bits: list[int]) -> int:
    return int(''.join(str(b) for b in bits), 2)

def string_to_bitlist(s: str) -> list[int]:
    return [int(b) for c in s.encode('utf-8') for b in format(c, '08b')]

def bitlist_to_string(bits: list[int]) -> str:
    bytes_list = [int(''.join(str(b) for b in bits[i:i+8]), 2) for i in range(0, len(bits), 8)]
    return bytes(bytearray(bytes_list)).decode('utf-8', errors='ignore')

def left_shift(bits: list[int], n: int) -> list[int]:
    return bits[n:] + bits[:n]

# part 3
def generate_keys(key_64):
    key_56 = permute(key_64, t.PC_1)
    C = key_56[:28]
    D = key_56[28:]

    round_keys = []

    for i in range(16):
        C = left_shift(C, t.SHIFT_TABLE[i])
        D = left_shift(D, t.SHIFT_TABLE[i])
        combined = C + D
        round_key = permute(combined, t.PC_2)
        round_keys.append(round_key)

    return round_keys

# part 4
def f_function(R: list[int], K: list[int]) -> list[int]:
    R_expanded = permute(R, t.E)
    X = xor(R_expanded, K)
    
    S_output = []
    for i in range(8):
        block = X[i*6:(i+1)*6]
        row = (block[0] << 1) | block[5]
        col = (block[1] << 3) | (block[2] << 2) | (block[3] << 1) | block[4]
        val = t.S_BOX[i][row][col]
        S_output.extend(int_to_bitlist(val, 4))

    return permute(S_output, t.P)

# part 5
def encrypt_block(plaintext_block: list[int], keys: list[list[int]]) -> list[int]:
    block = permute(plaintext_block, t.IP)
    L, R = block[:32], block[32:]

    for i in range(16):
        temp = R
        R = xor(L, f_function(R, keys[i]))
        L = temp

    combined = R + L

    return permute(combined, t.IP_INV)

# part 6
def decrypt_block(ciphertext_block: list[int], keys_reversed: list[list[int]]) -> list[int]:
    block = permute(ciphertext_block, t.IP)
    L, R = block[:32], block[32:]

    for i in range(16):
        temp = R
        R = xor(L, f_function(R, keys_reversed[i]))
        L = temp

    combined = R + L

    return permute(combined, t.IP_INV)

# part 7
def pad_bitlist(bits: list[int], block_size: int = 64) -> list[int]: #PKCS#5-style padding
    pad_len = block_size - (len(bits) % block_size)
    pad_byte = format(pad_len // 8, '08b') * (pad_len // 8)
    return bits + [int(b) for b in pad_byte]

def unpad_bitlist(bits: list[int]) -> list[int]:
    last_byte = bits[-8:]
    pad_len = int(''.join(str(b) for b in last_byte), 2)
    if pad_len < 1 or pad_len > 8:
        return bits
    return bits[:-pad_len * 8]

# part 8
def des_encrypt(plaintext: str, key_str: str) -> list[int]: #EBC
    plaintext_bits = string_to_bitlist(plaintext)
    key_bits = string_to_bitlist(key_str)[:64]  # 64비트 키 사용

    plaintext_bits = pad_bitlist(plaintext_bits)
    round_keys = generate_keys(key_bits)

    ciphertext_bits = []
    for i in range(0, len(plaintext_bits), 64):
        block = plaintext_bits[i:i+64]
        encrypted_block = encrypt_block(block, round_keys)
        ciphertext_bits.extend(encrypted_block)

    return ciphertext_bits

def des_decrypt(cipher_bits: list[int], key_str: str) -> str:
    key_bits = string_to_bitlist(key_str)[:64]
    round_keys = generate_keys(key_bits)[::-1]  # 키 역순

    plain_bits = []
    for i in range(0, len(cipher_bits), 64):
        block = cipher_bits[i:i+64]
        decrypted_block = decrypt_block(block, round_keys)
        plain_bits.extend(decrypted_block)

    plain_bits = unpad_bitlist(plain_bits)
    return bitlist_to_string(plain_bits)

# part 9
def des_encrypt_cbc(plaintext: str, key_str: str, iv: list[int]) -> list[int]:
    plaintext_bits = string_to_bitlist(plaintext)
    key_bits = string_to_bitlist(key_str)[:64]
    plaintext_bits = pad_bitlist(plaintext_bits)

    round_keys = generate_keys(key_bits)

    ciphertext_bits = []
    previous_block = iv

    for i in range(0, len(plaintext_bits), 64):
        block = plaintext_bits[i:i+64]
        block_xored = xor(block, previous_block)
        encrypted_block = encrypt_block(block_xored, round_keys)
        ciphertext_bits.extend(encrypted_block)
        previous_block = encrypted_block

    return ciphertext_bits

def des_decrypt_cbc(ciphertext_bits: list[int], key_str: str, iv: list[int]) -> str:
    key_bits = string_to_bitlist(key_str)[:64]
    round_keys = generate_keys(key_bits)[::-1]

    plain_bits = []
    previous_block = iv

    for i in range(0, len(ciphertext_bits), 64):
        block = ciphertext_bits[i:i+64]
        decrypted_block = decrypt_block(block, round_keys)
        plain_block = xor(decrypted_block, previous_block)
        plain_bits.extend(plain_block)
        previous_block = block

    plain_bits = unpad_bitlist(plain_bits)
    return bitlist_to_string(plain_bits)