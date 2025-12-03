from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, wallet, services, mobilenig, profile, price

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(wallet.router, prefix="/wallet", tags=["wallet"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(mobilenig.router, prefix="/mobilenig", tags=["mobilenig"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(price.router, prefix="/price", tags=["price"])
