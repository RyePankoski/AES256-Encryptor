# AES-256 Encryption Implementation

A from-scratch implementation of the AES-256 encryption algorithm in Python, built for educational purposes.

<img width="640" height="960" alt="image" src="https://github.com/user-attachments/assets/173c7bb4-61ce-4c73-ae9b-4ed5fb2a75f2" />


## Features

- **Padding**: PKCS#7-style padding with random bytes
- **Key XOR**: Initial round key addition
- **SubBytes**: S-box substitution for non-linearity
- **ShiftRows**: Row-based diffusion (row-major layout)
- **MixColumns**: Galois Field GF(2^8) column mixing
- **14 rounds**: Full AES-256 round structure

## Usage
```python
from encryptor import Encryptor

enc = Encryptor()
enc.set_plaintext("Your message here")
enc.encrypt()
```

## Implementation Notes

- Uses row-major matrix ordering (not standard AES column-major)
- Key schedule not yet implemented (uses same key each round)
- Decryption not yet implemented
- Built for learning—not production use

## Requirements

- Python 3.x
- `secrets` module (standard library)

## Learning Goals

Understanding core AES concepts:
- Symmetric encryption structure
- Galois Field arithmetic
- Diffusion and confusion principles
- Block cipher operations

---

**Note**: This is an educational implementation. For production use, use established libraries like `cryptography` or `pycryptodome`.
