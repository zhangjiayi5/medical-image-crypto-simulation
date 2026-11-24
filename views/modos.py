import streamlit as st

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
        font-size:22px;
        color:#475569;
        margin-top:-10px;
        margin-bottom:30px;
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

st.divider()

col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("Original")

    st.image(
        image,
        caption="MRI original",
        use_container_width=True
    )


with col2:

    st.subheader(f"Cifrada — {selected_mode}")

    st.image(
        encrypted_image,
        caption=f"AES-{selected_mode}",
        use_container_width=True
    )


with col3:

    st.subheader("Recuperada")

    st.image(
        recovered_image,
        caption="MRI descifrada",
        use_container_width=True
    )


# ------------------------------------------------------------
# RESULTADO
# ------------------------------------------------------------

if selected_mode == "ECB":

    st.warning(
        "ECB conserva patrones de la imagen original."
    )

else:

    st.success(
        f"{selected_mode} oculta los patrones visuales "
        "de la imagen original."
    )


if decrypted_bytes == image_bytes:

    st.success(
        "La imagen se recupera exactamente después del descifrado."
    )