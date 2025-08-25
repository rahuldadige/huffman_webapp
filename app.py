import streamlit as st
import cv2
import numpy as np
from huffman_utils import compress_image_gray, decompress_image_gray
from binary_io import save_huff_file, load_huff_file
from PIL import Image
from io import BytesIO
import os

st.title("🗜️ Optimized Huffman Image Compressor (Grayscale Only)")

uploaded = st.file_uploader("Upload Grayscale Image", type=["png", "jpg", "jpeg"])
if uploaded:
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

    st.image(image, caption="Original Image", use_column_width=True)

    # Calculate the original size in bytes
    original_size = image.size  # Number of pixels (height * width)
    original_size_bytes = original_size  # For grayscale, 1 byte per pixel

    if st.button("🔐 Compress"):
        encoded, codebook, shape = compress_image_gray(image)
        save_huff_file("compressed.huff", encoded, codebook, shape)

        # Get compressed file size
        compressed_size_bytes = os.path.getsize("compressed.huff")

        # Calculate compression ratio
        compression_ratio = original_size_bytes / compressed_size_bytes
        st.write(f"Compression Ratio: {compression_ratio:.2f}")

        # Provide download link for the .huff file
        with open("compressed.huff", "rb") as f:
            st.download_button("⬇️ Download .huff", f, file_name="compressed.huff")

        st.success("✅ Compressed!")

st.header("🧩 Decompress .huff File")
uploaded_huff = st.file_uploader("Upload .huff File", type=["huff"], key="huff")

if uploaded_huff and st.button("🔓 Decompress"):
    with open("temp.huff", "wb") as f:
        f.write(uploaded_huff.read())

    encoded, codebook, shape = load_huff_file("temp.huff")
    image = decompress_image_gray(encoded, codebook, shape)

    st.image(image, caption="Decompressed Image", use_column_width=True)
    pil_image = Image.fromarray(image)
    buf = BytesIO()
    pil_image.save(buf, format="PNG")
    st.download_button("📥 Download Decompressed Image", buf.getvalue(), file_name="decompressed.png")