from sqlalchemy import Column, ForeignKey, select
from sqlalchemy import Integer, String, BigInteger, Double, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"

    id = Column("id", Integer, primary_key=True)
    coin = Column("coin", String, nullable=False)
    begin_time = Column("begin_time", BigInteger)
    end_time = Column("end_time", BigInteger)

    @classmethod
    async def get_all(cls, db: AsyncSession):
        return (await db.execute(select(cls))).scalars().all()


class Trade(Base):
    __tablename__ = "trades"

    id = Column("id", BigInteger, primary_key=True)
    session_id = Column("session_id", Integer, ForeignKey(
        "sessions.id"), nullable=False)
    trade_time = Column("trade_time", BigInteger, nullable=False)
    trade_id = Column("trade_id", BigInteger, nullable=False)
    price = Column("price", Double, nullable=False)
    quantity = Column("quantity", Double, nullable=False)
    buyer_order_id = Column("buyer_order_id", Integer)
    seller_order_id = Column("seller_order_id", Integer)
    is_buyer_mm = Column("is_buyer_mm", Boolean, nullable=False)

    @classmethod
    async def get_session_trades(cls, db: AsyncSession, session_id: int):
        return (await db.execute(select(cls).where(
            cls.session_id == session_id))).scalars().all()


class Kline(Base):
    __tablename__ = "klines_1s"

    id = Column("id", BigInteger, primary_key=True)
    session_id = Column("session_id", Integer, ForeignKey(
        "sessions.id"), nullable=False)
    open_time = Column("open_time", BigInteger, nullable=False)
    close_time = Column("close_time", BigInteger, nullable=False)
    first_trade_id = Column("first_trade_id", BigInteger)
    last_trade_id = Column("last_trade_id", BigInteger)
    open_price = Column("open_price", Double, nullable=False)
    close_price = Column("close_price", Double, nullable=False)
    high_price = Column("high_price", Double, nullable=False)
    low_price = Column("low_price", Double, nullable=False)
    base_asset_vol = Column("base_asset_vol", Double, nullable=False)
    num_of_trades = Column("num_of_trades", Integer, nullable=False)
    quote_asset_vol = Column("quote_asset_vol", Double, nullable=False)
    taker_buy_base_vol = Column("taker_buy_base_vol", Double, nullable=False)
    taker_buy_quote_vol = Column("taker_buy_quote_vol", Double, nullable=False)

    @classmethod
    async def get_session_klines(cls, db: AsyncSession, session_id: int):
        return (await db.execute(select(cls).where(
            cls.session_id == session_id))).scalars().all()
