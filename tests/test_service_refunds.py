from app.api.v1.endpoints.services import should_refund_on_failure
from app.models.transaction import Transaction


def test_should_refund_only_for_incomplete_transactions():
    processing_tx = Transaction(status="processing")
    assert should_refund_on_failure(processing_tx) is True

    success_tx = Transaction(status="success")
    assert should_refund_on_failure(success_tx) is False

    failed_tx = Transaction(status="failed")
    assert should_refund_on_failure(failed_tx) is True
