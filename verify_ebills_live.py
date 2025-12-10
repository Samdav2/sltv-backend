import asyncio
import logging
from app.services.ebills_service import ebills_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_live_auth():
    print("Starting Live eBills Authentication Verification...")

    try:
        # 1. Test Authentication
        print("\n1. Testing Authentication...")
        token = await ebills_service._get_token()
        print(f"Success! Token received: {token[:10]}...")

        # 2. Test Verify Customer (Optional, using a likely invalid number just to check API reachability)
        print("\n2. Testing Verify Customer (Reachability)...")
        # Using a dummy number, expecting failure but valid HTTP response
        try:
            verify_result = await ebills_service.verify_customer("00000000000", "enugu-electric")
            print(f"Verify Result: {verify_result}")
        except Exception as e:
            print(f"Verify call failed as expected (or due to invalid number): {e}")

    except Exception as e:
        print(f"Authentication Failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify_live_auth())
