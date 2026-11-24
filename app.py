import streamlit as st


st.set_page_config(
    page_title="Protección de imágenes médicas",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------------------------------
# ESTILO GENERAL
# ------------------------------------------------------------

st.markdown(
    """
    <style>

    /* Tamaño general del contenido */
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Texto general */
    html, body, [class*="css"] {
        font-size: 18px;
    }

    /* Títulos */
    h1 {
        font-size: 44px !important;
        font-weight: 700 !important;
        color: #172033 !important;
    }

    h2 {
        font-size: 30px !important;
        font-weight: 650 !important;
        color: #172033 !important;
    }

    h3 {
        font-size: 23px !important;
        font-weight: 600 !important;
        color: #172033 !important;
    }

    /* Menú lateral */
    [data-testid="stSidebar"] {
        min-width: 260px;
    }

    [data-testid="stSidebar"] a {
        font-size: 18px !important;
    }

    /* Botones */
    .stButton > button {
        font-size: 18px;
        font-weight: 600;
        padding: 0.55rem 1.2rem;
    }

    /* Radio buttons */
    div[role="radiogroup"] label {
        font-size: 18px !important;
    }

    /* Selectbox */
    [data-testid="stSelectbox"] {
        font-size: 18px;
    }

    /* Tablas */
    [data-testid="stDataFrame"] {
        font-size: 17px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# NAVEGACIÓN
# ------------------------------------------------------------

pages = [
    st.Page(
        "views/simulacion.py",
        title="Simulación AES-RSA",
        default=True
    ),

    st.Page(
        "views/modos.py",
        title="Modos de cifrado"
    ),

]


navigation = st.navigation(pages)

navigation.run()