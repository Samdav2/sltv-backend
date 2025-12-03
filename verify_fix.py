from app.schemas.mobilenig import DataPurchaseRequest
import json

def test_data_purchase_request_validation():
    # Simulate the input payload that was causing the error
    input_data = {
        "service_id": "BCA",
        "trans_id": "1292988383",
        "amount": 428,
        "customerPhoneNumber": "07064205836",
        "productCode": "MBMS500"
    }

    try:
        # Attempt to validate the data using the Pydantic model
        request = DataPurchaseRequest(**input_data)
        print("Validation successful!")
        print(f"Parsed data: {request.model_dump()}")

        # Verify that phoneNumber is correctly populated
        assert request.phoneNumber == "07064205836"
        print("phoneNumber field correctly populated from customerPhoneNumber alias.")

    except Exception as e:
        print(f"Validation failed: {e}")

if __name__ == "__main__":
    test_data_purchase_request_validation()
