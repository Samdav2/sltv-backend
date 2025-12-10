import asyncio
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getcwd())

# Mock env vars for config
if not os.getenv("MAIL_FROM"):
    os.environ["MAIL_FROM"] = "test@example.com"
if not os.getenv("MAIL_JET_API"):
    os.environ["MAIL_JET_API"] = "mock"
if not os.getenv("MAIL_JET_SECRET"):
    os.environ["MAIL_JET_SECRET"] = "mock"
if not os.getenv("MOBILENIG_PUBLIC_KEY"):
    os.environ["MOBILENIG_PUBLIC_KEY"] = "mock"
if not os.getenv("MOBILENIG_SECRET_KEY"):
    os.environ["MOBILENIG_SECRET_KEY"] = "mock"
if not os.getenv("PAYSTACK_PUBLIC_KEY"):
    os.environ["PAYSTACK_PUBLIC_KEY"] = "mock"
if not os.getenv("PAYSTACK_SECRET_KEY"):
    os.environ["PAYSTACK_SECRET_KEY"] = "mock"

from app.core.database import init_db
from app.models.user import User # Ensure User model is registered
from app.models.support import Ticket, TicketMessage # Ensure models are registered
from app.models.admin import Admin # Ensure Admin model is registered
from app.models.user_profile import UserProfile # Ensure UserProfile model is registered
from app.models.service_price import ServicePrice # Ensure ServicePrice model is registered
from app.models.transaction import Transaction # Ensure Transaction model is registered
from app.models.wallet import Wallet # Ensure Wallet model is registered

async def main():
    print("Initializing database tables...")
    await init_db()
    print("Tables created.")

if __name__ == "__main__":
    asyncio.run(main())
