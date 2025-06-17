# DES (Data Encryption Standard) — Python Educational Implementation

This project provides a Python-based implementation of the classical symmetric-key block cipher, **DES (Data Encryption Standard)**.

It is designed as an educational resource to help you understand the internals of block encryption, key scheduling, S-boxes, ECB/CBC modes, and more through direct code interaction.

> ⚠️ Warning: This implementation is for educational and learning purposes only.
> 
> 
> It is **not secure** for use in any real-world cryptographic application.
> 

---

## Project Structure

```bash
KR

├── DES.py                 # DES 전체 알고리즘 구현 (ECB/CBC 지원)
├── DES_beginner.md        # 초심자를 위한 개념 정리 및 로직 설명 가이드
├── DES_example.py         # ECB 및 CBC 모드 테스트 예제 실행 파일
├── DES_readme.md          # 전체 설명 파일
└── DES_table.py           # DES에서 사용하는 순열/확장/S-box 테이블 정의

EN
├── DES.py                 # Core DES algorithm (includes ECB and CBC modes)
├── DES_beginner.md        # Beginner-friendly guide explaining DES logic step by step
├── DES_example.py         # Sample script to demonstrate encryption and decryption
├── DES_readme.md          # This project description file
└── DES_table.py           # Defines DES permutation and substitution tables
```
