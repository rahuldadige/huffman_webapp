from bitarray import bitarray
import struct

def save_huff_file(path, encoded, codebook, shape):
    with open(path, "wb") as f:
        # Mode: G (1 byte)
        f.write(b'G')

        # Shape: height + width (4 bytes each)
        f.write(struct.pack(">II", shape[0], shape[1]))

        # Codebook
        f.write(struct.pack(">I", len(codebook)))
        for val, code in codebook.items():
            code_bits = code.to01()
            f.write(struct.pack("BB", val, len(code_bits)))
            f.write(bitarray(code_bits).tobytes())

        # Encoded length (bits)
        f.write(struct.pack(">I", len(encoded)))

        # Encoded data
        f.write(encoded.tobytes())

def load_huff_file(path):
    with open(path, "rb") as f:
        mode = f.read(1)
        if mode != b'G':
            raise ValueError("Only grayscale supported.")

        h, w = struct.unpack(">II", f.read(8))

        dict_len = struct.unpack(">I", f.read(4))[0]
        codebook = {}
        for _ in range(dict_len):
            val, code_len = struct.unpack("BB", f.read(2))
            byte_len = (code_len + 7) // 8
            bits = bitarray()
            bits.frombytes(f.read(byte_len))
            bits = bits[:code_len]
            codebook[val] = bits

        bit_len = struct.unpack(">I", f.read(4))[0]
        encoded = bitarray()
        encoded.frombytes(f.read())
        encoded = encoded[:bit_len]

        return encoded, codebook, (h, w)
