import unittest
from unittest.mock import patch, MagicMock
from app.services.mobilenig_service import MobileNigService
from app.schemas.mobilenig import BalanceResponse, ServicesStatusResponse

class TestMobileNigService(unittest.TestCase):
    @patch('app.services.mobilenig_service.requests.request')
    def test_get_balance(self, mock_request):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "message": "success",
            "statusCode": "200",
            "details": {"balance": "5000.00"}
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        service = MobileNigService()
        balance = service.get_balance()

        self.assertIsInstance(balance, BalanceResponse)
        self.assertEqual(balance.details.balance, "5000.00")
        mock_request.assert_called_once()

    @patch('app.services.mobilenig_service.requests.request')
    def test_purchase_airtime(self, mock_request):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "message": "success",
            "statusCode": "200",
            "details": {
                "trans_id": "12345",
                "service": "MTN",
                "status": "Approved",
                "details": {},
                "wallet_balance": "4900.00"
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        service = MobileNigService()
        payload = {
            "service_id": "MTN",
            "trans_id": "12345",
            "amount": 100,
            "customerPhoneNumber": "08031234567"
        }
        response = service.purchase_service(payload)

        self.assertEqual(response.details.trans_id, "12345")
        self.assertEqual(response.details.service, "MTN")
        mock_request.assert_called_once()

if __name__ == '__main__':
    unittest.main()
