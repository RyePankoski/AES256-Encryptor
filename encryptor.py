import secrets
import random
import sys
from tables import *


def gf_mult(a, b):
    """Multiply two bytes in GF(2^8)"""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80  # Check if the high bit is set
        a <<= 1
        if hi_bit_set:
            a ^= 0x1b  # AES irreducible polynomial x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return p & 0xFF


def text_to_ascii_array(text):
    return [ord(char) for char in text]


def ascii_array_to_text(ascii_array):
    return ''.join(chr(byte) for byte in ascii_array)


def create_plaintext(length):
    plaintext = ""

    for _ in range(length):
        plaintext += chr(random.randint(0, 127))

    return plaintext


def s_box(array):
    for i in range(len(array)):
        byte = array[i]
        byte = S_BOX[byte]
        array[i] = byte

    return array


def get_blocks(array, block_size, purpose, row_or_block):
    blocks = []
    block = []
    index = 0
    for i in range(len(array)):
        block.append(array[i])  
        index += 1
        if index == block_size:
            blocks.append(block)
            block = []
            index = 0
    print(f"{purpose}, Number of {row_or_block}: {len(blocks)}")
    return blocks


def shift_rows(blocks):
    for block in blocks:
        rows = get_blocks(block, 4, "Get individual rows from block", "rows")
        for i in range(len(rows)):
            original_row = rows[i]
            modified_row = original_row[i:] + original_row[:i]
            rows[i] = modified_row

        # Flatten rows back into block
        block[:] = [byte for row in rows for byte in row]

    return blocks


def mix_columns(blocks):
    col_indices = [
        [0, 4, 8, 12],  # Column 0
        [1, 5, 9, 13],  # Column 1
        [2, 6, 10, 14],  # Column 2
        [3, 7, 11, 15]  # Column 3
    ]

    for block in blocks:
        new_block = [0] * 16

        # Process each column
        for col_idx, column in enumerate(col_indices):
            # Extract the 4 bytes from this column
            col_values = [block[i] for i in column]

            # Compute 4 new bytes using each row of MIX_MATRIX
            for row in range(4):
                new_byte = 0
                for i in range(4):
                    product = gf_mult(MIX_MATRIX[row][i], col_values[i])
                    new_byte ^= product

                # Store new byte back in the same column position
                new_block[column[row]] = new_byte

        # Replace block with new_block
        block[:] = new_block

    return blocks


class Encryptor:
    def __init__(self):
        # self.plaintext = create_plaintext(31)
        self.plaintext = "Hello claude, thank you for helping me build this. I now understand AES256"
        self.text_set = True
        self.key = 1234
        self.key_len = 32
        self.block_size = 16
        self.key = secrets.token_bytes(self.key_len)

        self.rounds = 14

    def set_plaintext(self, plaintext):
        self.plaintext = plaintext
        self.text_set = True

    def add_padding(self, array):
        print(f"Length without padding: {len(array)}")
        length = len(array)
        distance = self.block_size - (length % self.block_size)

        for _ in range(distance - 1):
            array.append(secrets.token_bytes(1)[0])

        array.append(distance)

        print(f"Length with padding: {len(array)}")
        print(f"Padding length: {array[len(array) - 1]}")
        return array

    def xor_key(self, array):
        absolute_pos = 0
        while True:
            for j in range(len(self.key)):
                array[absolute_pos] ^= self.key[j]
                absolute_pos += 1

                if absolute_pos >= len(array):
                    return array

    def encrypt(self):
        print(f"Plaintext: {self.plaintext}")
        ascii_array = text_to_ascii_array(self.plaintext)

        # We must first ensure that the message is a multiple of 16 bytes. So we add padding.
        array_with_pad = self.add_padding(ascii_array)

        top_message = array_with_pad

        for _ in range(self.rounds):
            # We then xor each byte of the message with the key.
            xor_array = self.xor_key(top_message)
            # We then use the s_box to map each byte to a new value.
            s_box_array = s_box(xor_array)

            # I am simply extracting the blocks to simplify the rest of the operations.
            blocks = get_blocks(s_box_array, self.block_size, "Split array in s=16 blocks", "blocks")

            # We then shift each row some amount in preparation for diffusion.
            shifted_rows_blocks = shift_rows(blocks)

            # We now mix the columns to ensure that any slight change to the starting message creates a large difference here.
            mixed_columns_blocks = mix_columns(shifted_rows_blocks)

            # Flatten blocks back to a single array
            top_message = [byte for block in mixed_columns_blocks for byte in block]

        result_text = ascii_array_to_text(top_message)
        print(f"Encrypted result: {result_text}")

        sys.exit(0)


