from app.core.config import settings

def verify_config():
    print(f"Checking MobileNig Public Key...")
    assert settings.MOBILENIG_PUBLIC_KEY == "pk_test_9lmX+vRmTBM7QtAp81qgTbBaVSX7Bb0aQao1wyBljqA="
    print("Public Key loaded correctly.")

    print(f"Checking MobileNig Secret Key...")
    assert settings.MOBILENIG_SECRET_KEY == "sk_test_je7DZvCFbLNtCSc952UALkUYZOcW/5KN6Qkra7ZVzZ4="
    print("Secret Key loaded correctly.")

if __name__ == "__main__":
    verify_config()
