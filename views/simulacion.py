import streamlit as st

from crypto_utils import (
    prepare_image,
    bytes_to_image,
    generate_aes_key,
    encrypt_aes_mode,
    decrypt_aes_mode,
    generate_rsa_keys,
    encrypt_aes_key_with_rsa,
    decrypt_aes_key_with_rsa,
)


# ============================================================
# PREPARAR IMAGEN
# ============================================================

image, image_bytes = prepare_image(
    "images/MRI_of_Human_Brain.jpg"
)


# ============================================================
# CABECERA
# ============================================================

st.title("Protección de imágenes médicas")

st.markdown(
    """
    <p style="
        font-size:25px;
        color:#475569;
        margin-top:-10px;
        margin-bottom:35px;
    ">
        Transmisión segura mediante AES-128 y RSA-1024
    </p>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ESCENARIO
# ============================================================

st.header("Escenario de transmisión")

modo_envio = st.radio(
    "Tipo de transmisión",
    [
        "Sin protección",
        "Protegido con AES-RSA"
    ],
    horizontal=True
)

enviar = st.button(
    "Iniciar transmisión",
    type="primary"
)

st.divider()


# ============================================================
# ESTADO INICIAL
# ============================================================

if not enviar:

    col1, col2, col3 = st.columns(3)


    with col1:

        st.subheader("Hospital A — Emisor")

        st.image(
            image,
            caption="MRI original",
            use_container_width=True
        )


    with col2:

        st.subheader("Canal de transmisión")

        st.info(
            "Esperando transmisión..."
        )


    with col3:

        st.subheader("Hospital B — Receptor")

        st.info(
            "Esperando imagen..."
        )


# ============================================================
# TRANSMISIÓN SIN PROTECCIÓN
# ============================================================

elif modo_envio == "Sin protección":

    st.error(
        "La imagen médica se transmite sin cifrar."
    )

    col1, col2, col3 = st.columns(3)


    # --------------------------------------------------------
    # HOSPITAL A
    # --------------------------------------------------------

    with col1:

        st.subheader("Hospital A — Emisor")

        st.image(
            image,
            caption="MRI original",
            use_container_width=True
        )


    # --------------------------------------------------------
    # ATACANTE
    # --------------------------------------------------------

    with col2:

        st.subheader("Atacante")

        st.image(
            image,
            caption="MRI interceptada",
            use_container_width=True
        )

        st.error(
            "La información médica puede visualizarse."
        )


    # --------------------------------------------------------
    # HOSPITAL B
    # --------------------------------------------------------

    with col3:

        st.subheader("Hospital B — Receptor")

        st.image(
            image,
            caption="MRI recibida",
            use_container_width=True
        )

        st.success(
            "Imagen recibida."
        )


# ============================================================
# TRANSMISIÓN PROTEGIDA AES-RSA
# ============================================================

else:

    # --------------------------------------------------------
    # 1. GENERAR CLAVE AES-128
    # --------------------------------------------------------

    aes_key = generate_aes_key()


    # --------------------------------------------------------
    # 2. CIFRAR LA MRI MEDIANTE AES-OCB
    # --------------------------------------------------------

    encrypted_image_bytes, aes_params = (
        encrypt_aes_mode(
            image_bytes,
            aes_key,
            "OCB"
        )
    )


    encrypted_image = bytes_to_image(
        encrypted_image_bytes
    )


    # --------------------------------------------------------
    # 3. GENERAR PAR DE CLAVES RSA-1024 DEL RECEPTOR
    # --------------------------------------------------------

    public_key, private_key = (
        generate_rsa_keys()
    )


    # --------------------------------------------------------
    # 4. PROTEGER LA CLAVE AES CON LA CLAVE PÚBLICA RSA
    # --------------------------------------------------------

    encrypted_aes_key = (
        encrypt_aes_key_with_rsa(
            aes_key,
            public_key
        )
    )


    # --------------------------------------------------------
    # 5. RECUPERAR LA CLAVE AES CON LA CLAVE PRIVADA RSA
    # --------------------------------------------------------

    recovered_aes_key = (
        decrypt_aes_key_with_rsa(
            encrypted_aes_key,
            private_key
        )
    )


    # --------------------------------------------------------
    # 6. DESCIFRAR LA MRI MEDIANTE AES-OCB
    # --------------------------------------------------------

    decrypted_image_bytes = (
        decrypt_aes_mode(
            encrypted_image_bytes,
            recovered_aes_key,
            "OCB",
            aes_params
        )
    )


    recovered_image = bytes_to_image(
        decrypted_image_bytes
    )


    # ========================================================
    # RESULTADO
    # ========================================================

    st.success(
        "Transmisión protegida mediante AES-128 y RSA-1024."
    )


    col1, col2, col3 = st.columns(3)


    # --------------------------------------------------------
    # HOSPITAL A
    # --------------------------------------------------------

    with col1:

        st.subheader("Hospital A — Emisor")

        st.image(
            image,
            caption="MRI original",
            use_container_width=True
        )

        st.markdown(
            "**Clave AES-128 generada**"
        )

        st.code(
            aes_key.hex(),
            language=None
        )

        st.write(
            "La MRI se cifra mediante AES-OCB."
        )


    # --------------------------------------------------------
    # ATACANTE
    # --------------------------------------------------------

    with col2:

        st.subheader("Atacante")

        st.image(
            encrypted_image,
            caption="MRI cifrada interceptada",
            use_container_width=True
        )

        st.markdown(
            "**Clave AES protegida con RSA**"
        )

        st.code(
            encrypted_aes_key.hex()[:100]
            + "...",
            language=None
        )

        st.error(
            "Sin la clave privada RSA, el atacante "
            "no puede recuperar la clave AES."
        )


    # --------------------------------------------------------
    # HOSPITAL B
    # --------------------------------------------------------

    with col3:

        st.subheader("Hospital B — Receptor")

        st.image(
            recovered_image,
            caption="MRI recuperada",
            use_container_width=True
        )

        if (
            recovered_aes_key == aes_key
            and decrypted_image_bytes == image_bytes
        ):

            st.success(
                "Clave AES e imagen recuperadas correctamente."
            )

        else:

            st.error(
                "Error durante la recuperación de los datos."
            )