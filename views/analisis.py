import streamlit as st

from crypto_utils import (
    prepare_image,
    generate_aes_key,
    evaluate_aes_mode,
)


# ------------------------------------------------------------
# CABECERA
# ------------------------------------------------------------

st.title("Análisis de resultados")

st.markdown(
    """
    <p style="
        font-size:22px;
        color:#475569;
        margin-top:-10px;
        margin-bottom:30px;
    ">
        Comparación experimental de los modos AES
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


modes = [
    "ECB",
    "CBC",
    "CTR",
    "CFB",
    "OCB"
]


# ------------------------------------------------------------
# EVALUACIÓN
# ------------------------------------------------------------

results = []


for mode in modes:

    aes_key = generate_aes_key()

    result = evaluate_aes_mode(
        image_bytes,
        aes_key,
        mode
    )


    recovery_ok = (
        result["decrypted"]
        == image_bytes
    )


    results.append(
        {
            "Modo":
                mode,

            "Cifrado (ms)":
                round(
                    result["encryption_time"]
                    * 1000,
                    3
                ),

            "Descifrado (ms)":
                round(
                    result["decryption_time"]
                    * 1000,
                    3
                ),

            "Throughput (Mbps)":
                round(
                    result[
                        "encryption_throughput"
                    ],
                    2
                ),

            "Entropía":
                round(
                    result["entropy"],
                    4
                ),

            "MSE":
                round(
                    result["mse"],
                    2
                ),

            "PSNR (dB)":
                round(
                    result["psnr"],
                    2
                ),

            "Recuperación":
                "Correcta"
                if recovery_ok
                else "Error"
        }
    )


# ------------------------------------------------------------
# TABLA
# ------------------------------------------------------------

st.dataframe(
    results,
    use_container_width=True,
    hide_index=True
)


# ------------------------------------------------------------
# DATOS PRINCIPALES
# ------------------------------------------------------------

st.divider()


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Imagen",
        "512 × 512 píxeles"
    )


with col2:

    st.metric(
        "Cifrado",
        "AES-128"
    )


with col3:

    st.metric(
        "Modos evaluados",
        "5"
    )


st.caption(
    "Los resultados corresponden a la ejecución local "
    "de la simulación."
)