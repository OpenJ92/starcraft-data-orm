from sqlalchemy.sql import text

from starcraft_data_orm.warehouse.datapack import *
from starcraft_data_orm.warehouse.replay import *
from starcraft_data_orm.warehouse.events import *

from starcraft_data_orm.warehouse.base import WarehouseBase
from starcraft_data_orm.warehouse.config import _engine

def initialize_warehouse():
    """Asynchronously initialize the starcraft_data_orm schema."""

    with _engine.begin() as conn:
        # Create schemas if they do not exist
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS datapack;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS events;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS replay;"))
        ## conn.execute(text("CREATE SCHEMA IF NOT EXISTS operations;"))

    # Create all tables
    WarehouseBase.metadata.create_all(bind=_engine)
    _engine.dispose()

