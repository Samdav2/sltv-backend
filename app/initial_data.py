import asyncio
import logging
from app.core.database import init_db
from app.models.user import User
from app.models.wallet import Wallet
from app.models.transaction import Transaction
# Import service models if they are table=True, but they seem to be schemas now?
# Wait, I moved them to schemas. Let me check if any service models are tables.
# Checking task.md, I see "Separate Schemas from Models".
# I should check if I have any other models that are tables.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Creating initial data")
    await init_db()
    logger.info("Initial data created")

if __name__ == "__main__":
    asyncio.run(main())
