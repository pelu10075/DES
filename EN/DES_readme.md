# DES Implementation Overview

This document summarizes and explains each part of the following Python files:

- `DES_table.py`: Table definitions required for the DES algorithm (**Part 2: Table Definitions**)
- `DES.py`: Full DES algorithm implementation (including ECB and CBC modes)
- `DES_example.py`: Example of encryption/decryption using the `DES.py` module

> ⚠️ Note: This implementation is for educational and learning purposes only. It may differ from the official DES standard and is not suitable for real-world security applications.
> 

---

## DES_table.py: Purpose of Each Table (Part 2)

### 1. `IP` (Initial Permutation)

> Reorders a 64-bit plaintext block to generate L0 and R0 for the Feistel structure.
> 

### 2. `IP_INV` (Inverse Initial Permutation)

> Final permutation applied after the 16 rounds of encryption. Reverses the IP operation and aligns the output.
> 

### 3. `E` (Expansion Permutation)

> Expands the 32-bit R block to 48 bits. Matches key length for XOR and enhances diffusion.
> 

### 4. `S_BOX` (Substitution Boxes)

> Consists of 8 S-Boxes. Each takes a 6-bit input and outputs 4 bits via non-linear substitution, increasing cryptographic strength.
> 

### 5. `P` (Permutation in f-function)

> Reorders the 32-bit output from the S-Boxes to enhance diffusion. Applied before XOR with the L block.
> 

### 6. `PC_1` (Permuted Choice 1)

> Removes 8 parity bits from the 64-bit key, selecting 56 bits. Splits the result into C0 and D0 for the key schedule.
> 

### 7. `PC_2` (Permuted Choice 2)

> After left-shifting C and D, selects 48 bits to generate the round keys.
> 

### 8. `SHIFT_TABLE`

> Specifies how many bits to left-shift C and D in each round. Ensures key variation across rounds.
> 

---

## DES.py: Functional Overview by Part

### Part 1: Bitwise Utility Functions

- `permute(bits, table)`
- `xor(bits1, bits2)`
- `int_to_bitlist(n, bits)` / `bitlist_to_int(bits)`
- `string_to_bitlist(s)` / `bitlist_to_string(bits)`
- `left_shift(bits, n)`

> Utility functions for bit-level transformations and operations used throughout the DES process.
> 

### Part 3: Key Schedule

- `generate_keys(key_64)`

> Reduces the 64-bit key to 56 bits using PC-1, splits into C and D, performs round-based shifts using SHIFT_TABLE, and generates 16 round keys via PC-2.
> 

### Part 4: f-function

- `f_function(R, K)`

> Performs the following steps:
> 
1. Expands R to 48 bits using E table
2. XOR with subkey K
3. Divide into 6-bit segments and apply S-Box substitution (producing 4 bits each)
4. Apply P permutation

> Returns a 32-bit result to be XORed with the L block.
> 

### Part 5: Block Encryption

- `encrypt_block(plaintext_block, keys)`

> Applies IP → 16-round Feistel structure → swap L and R → IP_INV. Returns the final 64-bit ciphertext block.
> 

### Part 6: Block Decryption

- `decrypt_block(ciphertext_block, keys_reversed)`

> Same as encryption, but round keys are used in reverse order.
> 

### Part 7: Padding and String Handling

- `pad_bitlist(bits)` / `unpad_bitlist(bits)`

> Uses PKCS#5-style padding to ensure input can be split into 64-bit blocks.
> 

### Part 8: ECB Mode

- `des_encrypt(plaintext, key_str)`
- `des_decrypt(cipher_bits, key_str)`

> Encrypts/decrypts in block-wise manner. Each block is processed independently (no chaining).
> 

### Part 9: CBC Mode

- `des_encrypt_cbc(plaintext, key_str, iv)`
- `des_decrypt_cbc(ciphertext_bits, key_str, iv)`

> Each plaintext block is XORed with the previous ciphertext block before encryption. In decryption, the decrypted result is XORed with the previous ciphertext block.
> 

---

## DES_example.py: Usage Example

### Main Components

1. **Key and Initialization Vector (IV) Setup**
    - The key is set to 64 bits (8 characters).
    - IV is required for CBC mode.
2. **Plaintext and Key Input**
    - Define the plaintext and key for encryption.
3. **ECB Mode Test**
    - Encrypt using `des_encrypt()` and decrypt with `des_decrypt()`.
4. **CBC Mode Test**
    - Encrypt with `des_encrypt_cbc()` and decrypt with `des_decrypt_cbc()`.

### Execution Output

1. Displays encrypted bitstream and decrypted plaintext for both ECB and CBC modes.
2. CBC mode adds inter-block dependency for enhanced security.

---

This structure implements a full block cipher system based on the standard DES specification, supporting both ECB and CBC modes.

⚠️ To reiterate, this implementation is **simplified for educational purposes only** and is **not recommended for real-world security use**.