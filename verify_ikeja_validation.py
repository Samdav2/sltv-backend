import asyncio
from app.services.mobilenig_service import mobilenig_service

async def verify_ikeja():
    service_id = "AMA"
    meter_number = "1111111111111" # Dummy number, likely to fail validation but test the endpoint

    print(f"Testing validation for Service ID: {service_id}, Meter: {meter_number}")

    try:
        response = await mobilenig_service.validate_customer(service_id, meter_number)
        print("Response:", response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify_ikeja())
