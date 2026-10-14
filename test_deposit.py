from decimal import Decimal
import uuid
from database.database import session
from auth.models import User
from wallet.model import Wallet, Transaction, LedgerAccount
from wallet.schema import DepositRequest

# Change this import to your actual service module.
from service.transaction_service import process_deposit, complete_deposit


db = session()

try:
    wallet = db.query(Wallet).first()

    if not wallet:
        raise RuntimeError("No wallet found. Create a wallet first.")

    initial_balance = Decimal(str(wallet.wallet_available_balance))

    # 1. Initiate a deposit using your actual service.
    request = DepositRequest(
        transaction_amount=Decimal("8600.00"),
        currency=wallet.wallet_currency,
    )

    deposit = process_deposit(request, wallet, db)

    transaction_reference = deposit["transaction_reference"]

    print("Deposit initiated:", deposit)

    # 2. Retrieve the pending transaction.
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.transaction_reference == transaction_reference
        )
        .first()
    )

    assert transaction is not None
    assert transaction.transaction_status == "pending"

    print("PASS: pending transaction created")

    # 3. Complete the deposit.
    provider_reference = f"Test_{uuid.uuid4().hex}"
    result = complete_deposit(
        transfer_reference=transaction_reference,
        provider_reference=provider_reference,
        db=db,
    )

    print("Completion result:", result)

    db.refresh(wallet)
    db.refresh(transaction)

    expected_balance = initial_balance + Decimal("8600.00")

    assert transaction.transaction_status == "completed"
    assert Decimal(str(wallet.wallet_available_balance)) == expected_balance

    # 4. Verify the ledger entry.
    ledger_entries = (
        db.query(LedgerAccount)
        .filter(LedgerAccount.transaction_id == transaction.id)
        .all()
    )

    assert len(ledger_entries) == 1
    assert ledger_entries[0].entries_type == "credit"
    assert ledger_entries[0].entries_amount == Decimal("8600.00")

    print("PASS: wallet credited correctly")
    print("PASS: one ledger entry created")

    # 5. Test duplicate completion.
    complete_deposit(
        transfer_reference=transaction_reference,
        provider_reference=provider_reference,
        db=db,
    )

    db.refresh(wallet)

    assert Decimal(str(wallet.wallet_available_balance)) == expected_balance

    print("PASS: duplicate completion did not credit twice")
    print("All tests passed!")

except Exception:
    db.rollback()
    raise

finally:
    db.close()