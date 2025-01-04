from starcraft_data_orm.warehouse.config import SessionLocal, SyncSessionLocal
from starcraft_data_orm.warehouse import initialize_warehouse, WarehouseBase

from storage_bridge import LocalStorage

from sqlalchemy.sql import text

import asyncio
import sc2reader
from sc2reader.engine.plugins import (
    SelectionTracker,
    APMTracker,
    ContextLoader,
    GameHeartNormalizer,
)

sc2reader.engine.register_plugin(SelectionTracker())
sc2reader.engine.register_plugin(APMTracker())
sc2reader.engine.register_plugin(ContextLoader())
sc2reader.engine.register_plugin(GameHeartNormalizer())

async def main():
    initialize_warehouse()
    test_sync_connection()
    await test_async_connection()

def test_sync_connection():
    with SyncSessionLocal() as session:
        result = session.execute(text("SELECT 1;"))
        print(result.scalar())  # Should print 1

async def test_async_connection():
    async with SessionLocal() as session:
        result = await session.execute(text("SELECT 1;"))
        print(result.scalar())  # Should print 1


if __name__ == "__main__":
    asyncio.run(main())
