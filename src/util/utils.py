from cryptography import x509
from cryptography.hazmat.backends import default_backend
from passlib.context import CryptContext


def get_hashed_password(password: str) -> str:
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(
        plain_password, hashed_password
    )


def is_self_signed(cert_data: bytes) -> bool:
    cert = x509.load_pem_x509_certificate(cert_data, default_backend())
    issuer = cert.issuer.rfc4514_string()
    subject = cert.subject.rfc4514_string()
    return issuer == subject
