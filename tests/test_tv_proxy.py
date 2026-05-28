import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from app.api.v1.endpoints.services import purchase_tv
from app.schemas.service import TVRequest

@pytest.mark.asyncio
async def test_purchase_tv_success_deduction():
    # Mock Dependencies
    mock_request = MagicMock()
    mock_request.headers.get.return_value = "Bearer token"

    mock_bg_tasks = MagicMock()

    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.full_name = "Test User"

    mock_wallet = MagicMock()
    mock_wallet.id = 1
    mock_wallet.balance = 5000.0

    mock_wallet_repo = AsyncMock()
    mock_wallet_repo.get_by_user_id.return_value = mock_wallet

    tv_request = TVRequest(
        provider="sltv",
        smart_card_number="1234567890",
        amount=1000.0,
        phone_number="08012345678"
    )

    # Mock Requests Response (Success)
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Purchase Successful"}

    # Patch run_in_threadpool to return our mock response
    with patch("app.api.v1.endpoints.services.run_in_threadpool", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = mock_response

        # Patch EmailService to avoid actual emails
        with patch("app.services.email_service.EmailService") as mock_email:

            # Execute
            result = await purchase_tv(
                request=tv_request,
                req=mock_request,
                background_tasks=mock_bg_tasks,
                current_user=mock_user,
                wallet_repo=mock_wallet_repo
            )

            # Assertions

            # 1. Verify Remote Call was made (via run_in_threadpool)
            mock_run.assert_called_once()

            # 2. Verify Wallet Deduction happened
            assert mock_wallet.balance == 4000.0 # 5000 - 1000
            mock_wallet_repo.update.assert_called_once()

            # 3. Verify Transaction Created
            mock_wallet_repo.create_transaction.assert_called_once()
            created_trans = mock_wallet_repo.create_transaction.call_args[0][0]
            assert created_trans.amount == 1000.0
            assert created_trans.status == "success"
            assert "Remote Result: Purchase Successful" in created_trans.meta_data

            # 4. Verify Success Email Sent
            mock_email.send_purchase_success_email.assert_called_once()

            assert result["status"] == "success"

@pytest.mark.asyncio
async def test_purchase_tv_failure_no_deduction():
    # Mock Dependencies
    mock_request = MagicMock()
    mock_bg_tasks = MagicMock()

    mock_user = MagicMock()
    mock_user.id = 1

    mock_wallet = MagicMock()
    mock_wallet.id = 1
    mock_wallet.balance = 5000.0

    mock_wallet_repo = AsyncMock()
    mock_wallet_repo.get_by_user_id.return_value = mock_wallet

    tv_request = TVRequest(
        provider="sltv",
        smart_card_number="1234567890",
        amount=1000.0,
        phone_number="08012345678"
    )

    # Mock Requests Response (Failure)
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"detail": "Invalid Smart Card"}
    mock_response.text = '{"detail": "Invalid Smart Card"}'

    with patch("app.api.v1.endpoints.services.run_in_threadpool", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = mock_response

        # Execute & Expect Error
        try:
            await purchase_tv(
                request=tv_request,
                req=mock_request,
                background_tasks=mock_bg_tasks,
                current_user=mock_user,
                wallet_repo=mock_wallet_repo
            )
        except HTTPException as e:
            assert e.status_code == 400
            assert e.detail == "Invalid Smart Card"

        # Assertions

        # 1. Verify Wallet Deduction did NOT happen
        assert mock_wallet.balance == 5000.0
        mock_wallet_repo.update.assert_not_called()

        # 2. Verify Transaction NOT Created (or at least not success)
        mock_wallet_repo.create_transaction.assert_not_called()

if __name__ == "__main__":
    # Manual run helper
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_purchase_tv_success_deduction())
    loop.run_until_complete(test_purchase_tv_failure_no_deduction())
    print("All tests passed!")
