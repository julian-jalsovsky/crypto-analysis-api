from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Session as SessionModel, Trade as TradeModel, Kline as KlineModel

router = APIRouter(prefix="/sessions", tags=["sessions"])


class SessionSchema(BaseModel):
    id: int
    coin: str
    begin_time: int | None
    end_time: int | None

    class Config:
        orm_mode = True


class TradeSchema(BaseModel):
    id: int
    session_id: int
    trade_time: int
    trade_id: int
    price: float
    quantity: float
    buyer_order_id: int | None
    seller_order_id: int | None
    is_buyer_mm: bool

    class Config:
        orm_mode = True


class KlineSchema(BaseModel):
    id: int
    session_id: int
    open_time: int
    close_time: int
    first_trade_id: int | None
    last_trade_id: int | None
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    base_asset_vol: float
    num_of_trades: int
    quote_asset_vol: float
    taker_buy_base_vol: float
    taker_buy_quote_vol: float

    class Config:
        orm_mode = True


@router.get("/", response_model=list[SessionSchema])
async def get_sessions(db: AsyncSession = Depends(get_db)):
    return await SessionModel.get_all(db)


@router.get("/{session_id}/trades", response_model=list[TradeSchema])
async def get_trades(session_id: int, db: AsyncSession = Depends(get_db)):
    return await TradeModel.get_session_trades(db, session_id)


@router.get("/{session_id}/klines", response_model=list[KlineSchema])
async def get_klines(session_id: int, db: AsyncSession = Depends(get_db)):
    return await KlineModel.get_session_klines(db, session_id)
