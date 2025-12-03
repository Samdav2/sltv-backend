from app.schemas.mobilenig import DataPurchaseRequest
from app.services.mobilenig_service import MobileNigService
from unittest.mock import MagicMock
import json

def test_refactor():
    # 1. Test DataPurchaseRequest schema
    input_data = {
        "service_id": "BCA",
        "service_type": "SME",
        "customerPhoneNumber": "09039636737",
        "productCode": "MBMS500",
        "amount": 428
    }

    try:
        request = DataPurchaseRequest(**input_data)
        print("Schema Validation Successful!")

        # Check default dump (should use field names: phoneNumber, productCode)
        dumped_default = request.model_dump()
        print(f"Dumped (default): {dumped_default}")

        # Check alias dump (should use serialization aliases: beneficiary, code)
        dumped_alias = request.model_dump(by_alias=True)
        print(f"Dumped (by_alias): {dumped_alias}")

        if "beneficiary" in dumped_alias and "code" in dumped_alias:
             print("Serialization aliases correctly applied.")
        else:
             print("Error: Serialization aliases NOT applied.")

    except Exception as e:
        print(f"Schema Validation Failed: {e}")
        return

    # 2. Test Service Logic (trans_id generation)
    service = MobileNigService()
    service._make_request = MagicMock(return_value={
        "status": "success",
        "message": "mocked",
        "statusCode": "200",
        "details": {"trans_id": "123", "service": "data", "status": "success", "details": {}, "wallet_balance": 1000}
    })

    # Simulate payload from endpoint (assuming we fix the dump issue if any)
    # If we use `by_alias=True`, we get `beneficiary`.
    payload = request.model_dump(by_alias=True)

    response = service.purchase_service(payload)

    # Verify trans_id was added
    call_args = service._make_request.call_args
    # call_args is (args, kwargs). args[2] is data (if positional) or kwargs['data']
    # _make_request(method, endpoint, data=..., ...)
    # method="POST", endpoint="/services/"

    actual_payload = call_args[1]['data']
    print(f"Service Payload: {actual_payload}")

    if "trans_id" in actual_payload:
        print(f"trans_id generated: {actual_payload['trans_id']}")
    else:
        print("Error: trans_id NOT generated")

if __name__ == "__main__":
    test_refactor()
