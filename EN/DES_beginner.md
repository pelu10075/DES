# DES Beginner’s Guide (Detailed Version)

This document is a step-by-step guide that explains the entire DES encryption logic and concepts in detail, designed for those new to DES implementation. The base files are:

- `DES_table.py`: Table definitions
- `DES.py`: Full DES algorithm implementation
- `DES_example.py`: Example usage code

> ⚠️ This implementation is for learning and practice purposes only. Do not use it in real-world secure environments.
> 

---

## 0. Prerequisite Concepts

### What is a “table” in DES?

In DES, a “table” is a **fixed array used to select or rearrange bits**. For example, to extract 56 bits from a 64-bit input or to reorder bits in a predefined pattern. These tables define the structure of encryption, guiding **confusion and diffusion** effects.

### What is symmetric-key encryption?

Symmetric-key encryption uses **the same key for both encryption and decryption**. That is, the same key used to encrypt the data is also used to decrypt it. DES is a classic example of symmetric encryption.

### What is a parity bit?

A parity bit is an **extra bit added for error detection**. In DES, a 64-bit key is accepted, but only 56 bits are used for encryption. The remaining 8 bits are parity bits—one per byte.

### What is XOR?

XOR (exclusive OR) is a logical operation with the following behavior:

| A | B | A XOR B |
| --- | --- | --- |
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

XOR is a fundamental operation in encryption, used to **mix bits**.

---

## 1. Overview of DES

- Operates on **64-bit blocks**
- Uses **symmetric key encryption**
- Consists of a **16-round Feistel network**

---

## 2. Table Definitions (`DES_table.py`)

| Table Name | Purpose |
| --- | --- |
| `IP` | Applies the initial permutation to the plaintext (reorders 64-bit input) |
| `IP_INV` | Final inverse permutation to restore bit order |
| `E` | Expands 32-bit R to 48 bits |
| `S_BOX` | Non-linear substitution: 6-bit input → 4-bit output |
| `P` | Permutes the output of S-boxes to increase diffusion |
| `PC_1` | Removes parity + reorders key bits (64 → 56 bits) |
| `PC_2` | Combines C, D and selects 48 bits for subkey |
| `SHIFT_TABLE` | Specifies how many bits to left-shift C and D in each round |

---

## 3. Bitwise Operation Functions (`DES.py`)

### ▶ `permute(bits, table)`

- Reorders a given bit list according to the positions in `table`
- Example: `table = [3, 1, 2]` → returns bits in 3rd, 1st, 2nd order

### ▶ `xor(bits1, bits2)`

- Performs element-wise XOR on two bit lists of the same length
- Used in encryption for `L ⊕ f(R, K)`

### ▶ `left_shift(bits, n)`

- Circularly left-shifts a bit list by `n` bits
- Used in key scheduling for C and D

### ▶ `pad_bitlist(bits)` / `unpad_bitlist(bits)`

- Adds/removes padding using the PKCS#5 method
- Ensures data length aligns to 64-bit block size

---

## 4. Key Schedule: `generate_keys(key_64)`

1. Apply `PC_1` to reduce 64-bit key → 56 bits
2. Split into two 28-bit halves: C and D
3. For 16 rounds, left-shift C and D using `SHIFT_TABLE`
4. Use `PC_2` to generate 48-bit subkeys for each round

Final result: `round_keys[0~15]` = 16 round keys

---

## 5. f-function: `f_function(R, K)`

The core function used in each Feistel round:

1. Expand R to 48 bits using `E` table
2. XOR the result with round key K
3. Divide into 8 groups of 6 bits → apply corresponding S-Box (6 → 4 bits each)
4. Permute the 32-bit output using `P`

Final output: 32-bit result to be XORed with L

---

## 6. Block Encryption/Decryption: `encrypt_block()` / `decrypt_block()`

- Apply `IP` permutation → split into L0, R0
- Repeat 16 rounds of Feistel operations:
    - Update: `L_next = R`, `R_next = L ⊕ f(R, K)`
- Swap L and R, apply `IP_INV`
- Decryption is identical except round keys are used in reverse order

---

## 7. Full Message Encryption (ECB Mode)

- Split the string into 64-bit blocks and encrypt each block
- Use `des_encrypt()` / `des_decrypt()`
- Each block is processed independently (parallelizable)

---

## 8. CBC Mode Encryption

- Requires an `IV` (initialization vector)
- Each plaintext block is **XORed with the previous ciphertext block before encryption**
- During decryption, **XOR the decrypted result with the previous ciphertext block**

Functions:

- `des_encrypt_cbc(plaintext, key, iv)`
- `des_decrypt_cbc(ciphertext, key, iv)`

---

> This guide is based on an educational implementation and is not suitable for real-world security use.
> 

---

Let me know if you’d like this turned into a PDF, Markdown document, or need visual diagrams to accompany it.