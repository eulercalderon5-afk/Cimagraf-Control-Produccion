"""Hash de contraseñas con PBKDF2; nunca se guarda la contraseña original."""
import hashlib
import hmac
import secrets

ITERACIONES = 310_000


def generar_hash(clave):
    sal = secrets.token_bytes(16)
    derivada = hashlib.pbkdf2_hmac("sha256", clave.encode("utf-8"), sal, ITERACIONES)
    return f"pbkdf2_sha256${ITERACIONES}${sal.hex()}${derivada.hex()}"


def verificar_clave(clave, almacenado):
    try:
        algoritmo, iteraciones, sal_hex, hash_hex = almacenado.split("$")
        if algoritmo != "pbkdf2_sha256":
            return False
        calculado = hashlib.pbkdf2_hmac("sha256", clave.encode("utf-8"),
                                         bytes.fromhex(sal_hex), int(iteraciones)).hex()
        return hmac.compare_digest(calculado, hash_hex)
    except (ValueError, TypeError):
        return False
