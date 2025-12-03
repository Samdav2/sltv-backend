from app.schemas.mobilenig import CustomerValidationDetails
from pydantic import ValidationError

def test_customer_validation_details():
    # Simulate the raw API response from the logs
    api_response = {
        'canVend': True,
        'address': '2 Nojeem Sarata Balogun Street  Royal Estate  Isheri Olofin',
        'meterNumber': '43901960328',
        'name': 'ADEGBITE JOSEPH',
        'minimumAmount': 600,
        'customerAccountType': 'PREPAID',
        'customerDtNumber': None
    }

    try:
        details = CustomerValidationDetails(**api_response)
        print("Validation Successful!")
        print(f"Parsed Details: {details.model_dump()}")

        # Verify mappings
        assert details.customerName == "ADEGBITE JOSEPH"
        assert details.customerNumber == "43901960328"
        assert details.customerType == "PREPAID"
        assert details.address == "2 Nojeem Sarata Balogun Street  Royal Estate  Isheri Olofin"
        print("Field mappings verified successfully.")

    except ValidationError as e:
        print(f"Validation Failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_customer_validation_details()
