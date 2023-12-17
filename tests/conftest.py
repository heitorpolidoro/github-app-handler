import logging
import os
import pathlib

import pytest
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# from .helper import all_webhooks


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


# @pytest.fixture(scope="session", autouse=True)
# def setup_and_teardown(request, private_key):
#     # setup code
#     os.environ["PRIVATE_KEY"] = private_key
#     yield
# teardown code
# if not request.session.testsfailed:
#     not_read_webhooks = sorted(
#         file for file, value in all_webhooks.items() if not value
#     )
#     logging.warning(f"Not read webhooks: {not_read_webhooks}")


@pytest.fixture(scope="session")
def vcr_cassette_name(request):
    return "github_requests.yaml"
