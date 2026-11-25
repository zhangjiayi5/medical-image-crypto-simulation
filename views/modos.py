import streamlit as st
import numpy as np

from crypto_utils import (
    prepare_image,
    bytes_to_image,
    generate_aes_key,
    encrypt_aes_mode,
    decrypt_aes_mode,
)


# ------------------------------------------------------------
# CABECERA
# ------------------------------------------------------------

st.title("Modos de cifrado AES")

st.markdown(
    """
    <p style="
        font-size:20px;
        color:#475569;
        margin-top:-12px;
        margin-bottom:15px;
    ">
        Comparación visual de ECB, CBC, CTR, CFB y OCB
    </p>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# PREPARAR MRI
# ------------------------------------------------------------

image, image_bytes = prepare_image(
    "images/MRI_of_Human_Brain.jpg"
)


# ------------------------------------------------------------
# SELECCIÓN DEL MODO
# ------------------------------------------------------------

selected_mode = st.selectbox(
    "Modo AES",
    [
        "ECB",
        "CBC",
        "CTR",
        "CFB",
        "OCB"
    ]
)


# ------------------------------------------------------------
# CIFRADO
# ------------------------------------------------------------

aes_key = generate_aes_key()

ciphertext, params = encrypt_aes_mode(
    image_bytes,
    aes_key,
    selected_mode
)

encrypted_image = bytes_to_image(
    ciphertext
)


# ------------------------------------------------------------
# DESCIFRADO
# ------------------------------------------------------------

decrypted_bytes = decrypt_aes_mode(
    ciphertext,
    aes_key,
    selected_mode,
    params
)

recovered_image = bytes_to_image(
    decrypted_bytes
)


# ------------------------------------------------------------
# IMÁGENES
# ------------------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown("#### Original")

    st.image(
        image,
        caption="MRI original",
        width=300
    )


with col2:

    st.markdown(f"#### Cifrada — {selected_mode}")

    st.image(
        encrypted_image,
        caption=f"AES-{selected_mode}",
        width=300
    )


with col3:

    st.markdown("#### Recuperada")

    st.image(
        recovered_image,
        caption="MRI descifrada",
        width=300
    )


# ------------------------------------------------------------
# HISTOGRAMA
# ------------------------------------------------------------

st.markdown("#### Distribución de píxeles de la imagen cifrada")

encrypted_pixels = np.frombuffer(
    ciphertext,
    dtype=np.uint8
)

histogram, _ = np.histogram(
    encrypted_pixels,
    bins=256,
    range=(0, 256)
)

st.bar_chart(
    histogram,
    height=430,
    x_label="Valor del píxel",
    y_label="Frecuencia"
)


# ------------------------------------------------------------
# CONCLUSIÓN
# ------------------------------------------------------------

if selected_mode == "ECB":

    st.warning(
        "ECB conserva patrones visuales de la imagen y presenta "
        "una distribución menos uniforme."
    )

else:

    st.success(
        f"{selected_mode} oculta los patrones visuales y presenta "
        "una distribución más uniforme."
    )