import secrets
import time
import math
from collections import Counter

import numpy as np
from PIL import Image
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


# ============================================================
# PREPARACIÓN DE LA IMAGEN
# ============================================================

def prepare_image(image_path):
    """
    Prepara la imagen para la simulación:
    - escala de grises
    - resolución 512x512
    - conversión a bytes
    """

    image = Image.open(image_path)
    image = image.convert("L")
    image = image.resize((512, 512))

    image_bytes = image.tobytes()

    return image, image_bytes


def bytes_to_image(data, size=(512, 512)):
    """
    Reconstruye una imagen en escala de grises
    a partir de sus bytes.
    """

    return Image.frombytes(
        "L",
        size,
        data
    )


# ============================================================
# GENERACIÓN DE CLAVE AES-128
# ============================================================

def generate_aes_key():
    """
    Genera una clave AES-128 aleatoria.

    AES-128 utiliza una clave de 16 bytes = 128 bits.
    """

    return secrets.token_bytes(16)


# ============================================================
# AES-ECB
# ============================================================

def encrypt_aes_ecb(data, aes_key):
    """
    Cifra los datos utilizando AES-128 en modo ECB.
    """

    cipher = AES.new(
        aes_key,
        AES.MODE_ECB
    )

    return cipher.encrypt(data)


def decrypt_aes_ecb(encrypted_data, aes_key):
    """
    Descifra datos cifrados mediante AES-128 ECB.
    """

    cipher = AES.new(
        aes_key,
        AES.MODE_ECB
    )

    return cipher.decrypt(
        encrypted_data
    )


# ============================================================
# RSA-1024
# ============================================================

def generate_rsa_keys():
    """
    Genera el par de claves RSA-1024 del receptor.
    """

    private_key = RSA.generate(1024)

    public_key = private_key.publickey()

    return public_key, private_key


def encrypt_aes_key_with_rsa(
    aes_key,
    public_key
):
    """
    Protege la clave AES utilizando
    la clave pública RSA del receptor.
    """

    cipher_rsa = PKCS1_OAEP.new(
        public_key
    )

    encrypted_aes_key = cipher_rsa.encrypt(
        aes_key
    )

    return encrypted_aes_key


def decrypt_aes_key_with_rsa(
    encrypted_aes_key,
    private_key
):
    """
    Recupera la clave AES utilizando
    la clave privada RSA del receptor.
    """

    cipher_rsa = PKCS1_OAEP.new(
        private_key
    )

    aes_key = cipher_rsa.decrypt(
        encrypted_aes_key
    )

    return aes_key


# ============================================================
# CIFRADO CON DIFERENTES MODOS AES
# ============================================================

def encrypt_aes_mode(
    data,
    aes_key,
    mode
):
    """
    Cifra los datos utilizando uno de los modos
    estudiados:

    ECB
    CBC
    CTR
    CFB
    OCB
    """

    # --------------------------------------------------------
    # ECB
    # --------------------------------------------------------

    if mode == "ECB":

        cipher = AES.new(
            aes_key,
            AES.MODE_ECB
        )

        ciphertext = cipher.encrypt(
            data
        )

        params = {}


    # --------------------------------------------------------
    # CBC
    # --------------------------------------------------------

    elif mode == "CBC":

        cipher = AES.new(
            aes_key,
            AES.MODE_CBC
        )

        ciphertext = cipher.encrypt(
            data
        )

        params = {
            "iv": cipher.iv
        }


    # --------------------------------------------------------
    # CTR
    # --------------------------------------------------------

    elif mode == "CTR":

        cipher = AES.new(
            aes_key,
            AES.MODE_CTR
        )

        ciphertext = cipher.encrypt(
            data
        )

        params = {
            "nonce": cipher.nonce
        }


    # --------------------------------------------------------
    # CFB
    # --------------------------------------------------------

    elif mode == "CFB":

        cipher = AES.new(
            aes_key,
            AES.MODE_CFB,
            segment_size=128
        )

        ciphertext = cipher.encrypt(
            data
        )

        params = {
            "iv": cipher.iv
        }


    # --------------------------------------------------------
    # OCB
    # --------------------------------------------------------

    elif mode == "OCB":

        cipher = AES.new(
            aes_key,
            AES.MODE_OCB
        )

        ciphertext, tag = (
            cipher.encrypt_and_digest(
                data
            )
        )

        params = {
            "nonce": cipher.nonce,
            "tag": tag
        }


    else:

        raise ValueError(
            f"Modo AES no soportado: {mode}"
        )


    return ciphertext, params


# ============================================================
# DESCIFRADO CON DIFERENTES MODOS AES
# ============================================================

def decrypt_aes_mode(
    ciphertext,
    aes_key,
    mode,
    params
):
    """
    Descifra los datos utilizando el mismo modo AES
    empleado durante el cifrado.
    """

    # --------------------------------------------------------
    # ECB
    # --------------------------------------------------------

    if mode == "ECB":

        cipher = AES.new(
            aes_key,
            AES.MODE_ECB
        )

        plaintext = cipher.decrypt(
            ciphertext
        )


    # --------------------------------------------------------
    # CBC
    # --------------------------------------------------------

    elif mode == "CBC":

        cipher = AES.new(
            aes_key,
            AES.MODE_CBC,
            iv=params["iv"]
        )

        plaintext = cipher.decrypt(
            ciphertext
        )


    # --------------------------------------------------------
    # CTR
    # --------------------------------------------------------

    elif mode == "CTR":

        cipher = AES.new(
            aes_key,
            AES.MODE_CTR,
            nonce=params["nonce"]
        )

        plaintext = cipher.decrypt(
            ciphertext
        )


    # --------------------------------------------------------
    # CFB
    # --------------------------------------------------------

    elif mode == "CFB":

        cipher = AES.new(
            aes_key,
            AES.MODE_CFB,
            iv=params["iv"],
            segment_size=128
        )

        plaintext = cipher.decrypt(
            ciphertext
        )


    # --------------------------------------------------------
    # OCB
    # --------------------------------------------------------

    elif mode == "OCB":

        cipher = AES.new(
            aes_key,
            AES.MODE_OCB,
            nonce=params["nonce"]
        )

        plaintext = cipher.decrypt_and_verify(
            ciphertext,
            params["tag"]
        )


    else:

        raise ValueError(
            f"Modo AES no soportado: {mode}"
        )


    return plaintext


# ============================================================
# ENTROPÍA
# ============================================================

def calculate_entropy(data):
    """
    Calcula la entropía de Shannon.

    En datos de 8 bits, una entropía próxima a 8
    indica una elevada aleatoriedad.
    """

    frequencies = Counter(data)

    total = len(data)

    entropy = 0.0


    for frequency in frequencies.values():

        probability = (
            frequency / total
        )

        entropy -= (
            probability
            * math.log2(probability)
        )


    return entropy


# ============================================================
# MSE
# ============================================================

def calculate_mse(
    original_data,
    encrypted_data
):
    """
    Calcula el Mean Squared Error (MSE)
    entre la imagen original y la cifrada.
    """

    original = np.frombuffer(
        original_data,
        dtype=np.uint8
    ).astype(np.float64)


    encrypted = np.frombuffer(
        encrypted_data,
        dtype=np.uint8
    ).astype(np.float64)


    mse = np.mean(
        (original - encrypted) ** 2
    )


    return mse


# ============================================================
# PSNR
# ============================================================

def calculate_psnr(
    original_data,
    encrypted_data
):
    """
    Calcula el Peak Signal-to-Noise Ratio (PSNR)
    entre la imagen original y la cifrada.
    """

    mse = calculate_mse(
        original_data,
        encrypted_data
    )


    if mse == 0:

        return float("inf")


    psnr = 10 * np.log10(
        (255 ** 2) / mse
    )


    return psnr


# ============================================================
# THROUGHPUT
# ============================================================

def calculate_throughput(
    data,
    processing_time
):
    """
    Calcula la cantidad de información procesada
    por segundo en Mbps.
    """

    if processing_time == 0:

        return 0


    data_megabits = (
        len(data) * 8
    ) / 1_000_000


    throughput = (
        data_megabits
        / processing_time
    )


    return throughput


# ============================================================
# EVALUACIÓN DE UN MODO AES
# ============================================================

def evaluate_aes_mode(
    data,
    aes_key,
    mode
):
    """
    Evalúa un modo AES calculando:

    - tiempo de cifrado
    - tiempo de descifrado
    - throughput
    - entropía
    - MSE
    - PSNR
    - recuperación de los datos
    """

    # ========================================================
    # CIFRADO
    # ========================================================

    start_encrypt = time.perf_counter()


    ciphertext, params = encrypt_aes_mode(
        data,
        aes_key,
        mode
    )


    end_encrypt = time.perf_counter()


    encryption_time = (
        end_encrypt
        - start_encrypt
    )


    # ========================================================
    # DESCIFRADO
    # ========================================================

    start_decrypt = time.perf_counter()


    decrypted = decrypt_aes_mode(
        ciphertext,
        aes_key,
        mode,
        params
    )


    end_decrypt = time.perf_counter()


    decryption_time = (
        end_decrypt
        - start_decrypt
    )


    # ========================================================
    # MÉTRICAS
    # ========================================================

    entropy = calculate_entropy(
        ciphertext
    )


    mse = calculate_mse(
        data,
        ciphertext
    )


    psnr = calculate_psnr(
        data,
        ciphertext
    )


    encryption_throughput = (
        calculate_throughput(
            data,
            encryption_time
        )
    )


    decryption_throughput = (
        calculate_throughput(
            data,
            decryption_time
        )
    )


    # ========================================================
    # RESULTADOS
    # ========================================================

    return {

        "ciphertext":
            ciphertext,

        "decrypted":
            decrypted,

        "params":
            params,

        "encryption_time":
            encryption_time,

        "decryption_time":
            decryption_time,

        "encryption_throughput":
            encryption_throughput,

        "decryption_throughput":
            decryption_throughput,

        "entropy":
            entropy,

        "mse":
            mse,

        "psnr":
            psnr
    }


# ============================================================
# PRUEBA DIRECTA DEL SISTEMA AES-RSA
# ============================================================

if __name__ == "__main__":

    # Preparar MRI
    image, image_bytes = prepare_image(
        "images/MRI_of_Human_Brain.jpg"
    )


    # Generar AES-128
    aes_key = generate_aes_key()


    # Cifrar MRI
    encrypted_image = encrypt_aes_ecb(
        image_bytes,
        aes_key
    )


    # Generar RSA-1024
    public_key, private_key = (
        generate_rsa_keys()
    )


    # Proteger clave AES
    encrypted_aes_key = (
        encrypt_aes_key_with_rsa(
            aes_key,
            public_key
        )
    )


    # Recuperar clave AES
    recovered_aes_key = (
        decrypt_aes_key_with_rsa(
            encrypted_aes_key,
            private_key
        )
    )


    # Recuperar MRI
    decrypted_image = decrypt_aes_ecb(
        encrypted_image,
        recovered_aes_key
    )


    # Comprobaciones
    print(
        "Clave AES correcta:",
        recovered_aes_key == aes_key
    )


    print(
        "MRI correcta:",
        decrypted_image == image_bytes
    )