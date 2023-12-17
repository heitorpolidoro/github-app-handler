import os
import os
import pathlib

import pytest
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa




@pytest.fixture(scope="session")
def private_key():
    if os.path.exists("private-key.pem"):
        return pathlib.Path("private-key.pem").read_text()
    key = rsa.generate_private_key(
        backend=crypto_default_backend(), public_exponent=65537, key_size=2048
    )

    return key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption(),
    ).decode()



@pytest.fixture(scope="session")
def vcr_cassette_name(request):
    return "github_requests.yaml"
