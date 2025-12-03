from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app.models.user import User
from app.models.service_price import ServicePrice
from sqlmodel import select

router = APIRouter()

@router.post("/", response_model=ServicePrice)
async def create_service_price(
    service_price_in: ServicePrice,
    current_user: User = Depends(deps.get_current_active_user), # Should be admin
    session: deps.AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    Create or update a service price configuration.
    """
    # Check if exists
    statement = select(ServicePrice).where(ServicePrice.service_identifier == service_price_in.service_identifier)
    result = await session.exec(statement)
    existing_price = result.first()

    if existing_price:
        existing_price.profit_type = service_price_in.profit_type
        existing_price.profit_value = service_price_in.profit_value
        session.add(existing_price)
        await session.commit()
        await session.refresh(existing_price)
        return existing_price
    else:
        session.add(service_price_in)
        await session.commit()
        await session.refresh(service_price_in)
        return service_price_in

@router.get("/", response_model=List[ServicePrice])
async def get_service_prices(
    current_user: User = Depends(deps.get_current_active_user),
    session: deps.AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    Get all service prices.
    """
    statement = select(ServicePrice)
    result = await session.exec(statement)
    return result.all()
