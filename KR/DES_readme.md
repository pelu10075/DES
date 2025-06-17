# DES 구현 개요

이 문서는 다음 Python 파일들의 각 부분을 요약하고 설명합니다:

- `DES_table.py`: DES 알고리즘에 필요한 테이블 정의 파일 (**Part 2: 테이블 정의**)
- `DES.py`: DES 알고리즘 전체 구현 (ECB 및 CBC 모드 포함)
- `DES_example.py`: `DES.py` 모듈을 사용한 암호화/복호화 예제

> ⚠️ 주의: 이 구현은 교육 및 학습 목적으로 만든 것으로, 실제 DES 표준 구현과 다를 수 있으며 보안 목적의 실사용에는 적합하지 않습니다.
> 

---

## DES_table.py: 각 테이블의 용도 설명 (Part 2)

### 1. `IP` (초기 순열)

> 64비트 평문 블록을 재배열하여 Feistel 구조에 사용할 L0, R0를 생성함.
> 

### 2. `IP_INV` (역 초기 순열)

> 16라운드 암호화가 끝난 후 적용되는 최종 순열. IP의 반대 역할을 하며, 출력 결과를 정렬함.
> 

### 3. `E` (확장 순열)

> 32비트 R 블록을 48비트로 확장. 라운드 키와 XOR을 수행하기 위해 길이를 맞추고 확산을 증가시킴.
> 

### 4. `S_BOX` (대치 박스)

> 총 8개의 S-Box로 구성됨. 각 6비트 입력을 4비트 출력으로 비선형 치환하여 암호 강도를 높임.
> 

### 5. `P` (f 함수 내 순열)

> S-Box를 거친 32비트를 다시 섞어 확산을 강화함. 이후 L 블록과 XOR하기 전에 적용됨.
> 

### 6. `PC_1` (선택 순열 1)

> 64비트 키에서 패리티 비트(8개)를 제거하고 56비트를 선택. 이후 C0, D0로 분리되어 키 스케줄에 사용됨.
> 

### 7. `PC_2` (선택 순열 2)

> C, D를 왼쪽 순환시킨 후 56비트에서 48비트를 선택하여 각 라운드 키를 생성함.
> 

### 8. `SHIFT_TABLE`

> 각 라운드마다 C, D를 얼마나 왼쪽으로 순환할지를 지정함. 키 다양성을 확보함.
> 

---

## DES.py: 파트별 기능 설명

### Part 1: 비트 연산 유틸리티

- `permute(bits, table)`
- `xor(bits1, bits2)`
- `int_to_bitlist(n, bits)` / `bitlist_to_int(bits)`
- `string_to_bitlist(s)` / `bitlist_to_string(bits)`
- `left_shift(bits, n)`

> DES 전체 과정에서 필요한 비트 단위 변환 및 연산 함수들.
> 

### Part 3: 키 스케줄

- `generate_keys(key_64)`

> PC-1로 64비트 키를 56비트로 줄이고, C와 D로 나눈 뒤 SHIFT_TABLE에 따라 순환. PC-2로 48비트 라운드 키를 16개 생성함.
> 

### Part 4: f 함수

- `f_function(R, K)`

> 다음과 같은 단계 수행:
> 
1. R을 E 테이블로 48비트 확장
2. 서브키 K와 XOR
3. 6비트씩 나눠서 S-Box 치환 (4비트 출력)
4. P 테이블로 순열

> 최종 32비트 결과 반환, L과 XOR됨.
> 

### Part 5: 블록 단위 암호화

- `encrypt_block(plaintext_block, keys)`

> IP 수행 → 16 라운드 Feistel 구조 수행 → L/R 스왑 → IP_INV 수행. 최종 64비트 암호문 블록 반환.
> 

### Part 6: 블록 단위 복호화

- `decrypt_block(ciphertext_block, keys_reversed)`

> 암호화와 동일하지만 라운드 키 순서만 반대로 적용.
> 

### Part 7: 패딩 및 문자열 처리

- `pad_bitlist(bits)` / `unpad_bitlist(bits)`

> PKCS#5 방식의 패딩 처리. 입력 문자열이 64비트 블록으로 나누어지지 않을 경우 사용.
> 

### Part 8: ECB 모드

- `des_encrypt(plaintext, key_str)`
- `des_decrypt(cipher_bits, key_str)`

> 블록 단위로 암호화/복호화 수행. 각 블록은 독립적으로 처리됨 (연결 없음).
> 

### Part 9: CBC 모드

- `des_encrypt_cbc(plaintext, key_str, iv)`
- `des_decrypt_cbc(ciphertext_bits, key_str, iv)`

> 각 평문 블록을 이전 암호문 블록과 XOR 후 암호화. 복호화 시에는 복호화 결과를 이전 암호문 블록과 XOR.
> 

---

## DES_example.py: 사용 예시

### 주요 구성

1. **키와 초기화 벡터(IV) 설정**
    - 키는 64비트 길이(8문자)로 설정됩니다.
    - CBC 모드에서는 추가적으로 IV(초기화 벡터)가 필요합니다.
2. **평문 및 키 입력**
    - 암호화할 평문과 키를 설정합니다.
3. **ECB 모드 테스트**
    - `des_encrypt()`로 평문을 암호화하고, `des_decrypt()`로 복호화.
4. **CBC 모드 테스트**
    - `des_encrypt_cbc()`로 암호화하고, `des_decrypt_cbc()`로 복호화.

### 실행 결과

1. ECB 모드와 CBC 모드에서 암호화된 비트와 복호화된 평문을 확인할 수 있습니다.
2. CBC 모드는 블록 간의 연결성을 추가하여 보안을 강화합니다.

---

이 구조는 표준 DES 사양에 기반하여 구현된 전체 블록 암호 체계로, ECB와 CBC 모드 모두 지원합니다.

⚠️ 다시 강조하자면, 이 구현은 **학습 목적용**으로 간소화되어 있으며, **실제 보안 환경에서의 사용은 권장되지 않습니다.**