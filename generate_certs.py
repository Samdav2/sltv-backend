#!/usr/bin/env python3
"""
RSA Certificate Generator for Local Development

Generates `certs/private.pem` and `certs/public.pem` for JWT authentication.
These certificates are ignored by git (.gitignore) to keep secrets off GitHub.
"""

import os
import sys

def generate_certs():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    certs_dir = os.path.join(base_dir, "certs")
    os.makedirs(certs_dir, exist_ok=True)

    priv_path = os.path.join(certs_dir, "private.pem")
    pub_path = os.path.join(certs_dir, "public.pem")

    print(f"Generating RSA 2048-bit keys in: {certs_dir}")

    try:
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        priv_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        pub_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(priv_path, "wb") as f:
            f.write(priv_pem)

        with open(pub_path, "wb") as f:
            f.write(pub_pem)

        print(f"SUCCESS: Generated local certs:")
        print(f"  - Private Key: {priv_path}")
        print(f"  - Public Key:  {pub_path}")

    except Exception as e:
        print(f"ERROR generating RSA certificates: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    generate_certs()
