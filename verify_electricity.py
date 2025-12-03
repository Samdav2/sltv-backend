from app.schemas.mobilenig import ElectricityPurchaseRequest
from app.services.mobilenig_service import MobileNigService
from unittest.mock import MagicMock
import json

def test_electricity_purchase_request():
    # Simulate the input payload based on the user's example
    input_data = {
        "service_id": "AMA",
        "meterNumber": "04042404048",
        "amount": 100,
        "phoneNumber": "08012345678",
        "email": "ikeja@test.com",
        "customerName": "TESTMETER1",
        "customerAddress": "ABULE - EGBA BU ABULE",
        "customerAccountType": "PRIME",
        "customerDtNumber": "007903312",
        "contactType": "TENANT"
    }

    try:
        request = ElectricityPurchaseRequest(**input_data)
        print("Schema Validation Successful!")
        print(f"Parsed data: {request.model_dump()}")

        # Verify fields
        assert request.meterNumber == "04042404048"
        assert request.email == "ikeja@test.com"
        print("Fields verified successfully.")

        # Test service payload generation
        service = MobileNigService()
        service._make_request = MagicMock(return_value={
            "status": "success",
            "message": "mocked",
            "statusCode": "200",
            "details": {}
        })

        payload = request.model_dump()
        service.purchase_service(payload)

        call_args = service._make_request.call_args
        actual_payload = call_args[1]['data']
        print(f"Service Payload: {actual_payload}")

        if "trans_id" in actual_payload:
            print(f"trans_id generated: {actual_payload['trans_id']}")
        else:
            print("Error: trans_id NOT generated")

    except Exception as e:
        print(f"Validation Failed: {e}")

if __name__ == "__main__":
    test_electricity_purchase_request()
