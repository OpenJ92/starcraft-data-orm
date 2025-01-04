from sqlalchemy import Column, Integer, BigInteger, Float, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import relationship

from collections import defaultdict

from starcraft_data_orm.warehouse.replay.map import map
from starcraft_data_orm.warehouse.base import WarehouseBase
from starcraft_data_orm.exceptions import ReplayExistsError
from starcraft_data_orm.inject import Injectable

class info(Injectable, WarehouseBase):
    __tablename__ = "info"
    __table_args__ = ( UniqueConstraint("filehash", name="filehash_unique")
                     , { "schema": 'replay' } )

    primary_id = Column(Integer, primary_key=True)

    filename = Column(Text)
    filehash = Column(Text)
    load_level = Column(Integer)
    speed = Column(Text)
    type = Column(Text)
    game_type = Column(Text)
    real_type = Column(Text)
    category = Column(Text)
    is_ladder = Column(Boolean)
    is_private = Column(Boolean)
    region = Column(Text)
    game_fps = Column(Float)
    frames = Column(Integer)
    build = Column(Integer)
    base_build = Column(Integer)
    release_string = Column(Text)
    amm = Column(Integer)
    competitive = Column(Integer)
    practice = Column(Integer)
    cooperative = Column(Integer)
    battle_net = Column(Integer)
    hero_duplicates_allowed = Column(Integer)
    map_name = Column(Text)
    expansion = Column(Text)
    windows_timestamp = Column(BigInteger)
    unix_timestamp = Column(BigInteger)
    end_time = Column(DateTime)
    time_zone = Column(Float)
    start_time = Column(DateTime)
    date = Column(DateTime)

    players = relationship("player", back_populates="replay")
    objects = relationship("object", back_populates="replay")

    map_id = Column(Integer, ForeignKey("replay.map.primary_id"))
    map = relationship("map", back_populates="replays")

    basic_command_events = relationship("basic_command_event", back_populates="info")
    chat_events = relationship("chat_event", back_populates="info")
    player_stats_events = relationship("player_stats_event", back_populates="info")
    player_leave_events = relationship("player_leave_event", back_populates="info")
    upgrade_complete_events = relationship("upgrade_complete_event", back_populates="info")
    unit_born_events = relationship("unit_born_event", back_populates="info")
    unit_done_events = relationship("unit_done_event", back_populates="info")
    unit_init_events = relationship("unit_init_event", back_populates="info")
    unit_died_events = relationship("unit_died_event", back_populates="info")

    @classmethod
    @property
    def __tableschema__(self):
        return "replay"

    @classmethod
    async def process(cls, replay, session):
        if await cls.process_existence(replay, session):
            raise ReplayExistsError(replay.filehash)

        data = cls.get_data(replay)
        parents = await cls.process_dependancies(replay, replay, session)

        session.add(cls(**data, **parents))

    @classmethod
    async def process_existence(cls, replay, session):
       statement = select(cls).where(cls.filehash == replay.filehash)
       result = await session.execute(statement)
       return result.scalar()

    @classmethod
    async def process_dependancies(cls, obj, replay, session):
       _map, parents = obj.map_hash, defaultdict(lambda: None)

       statement = select(map).where(map.filehash == _map)
       result    = await session.execute(statement)
       _map      = result.scalar()

       if not _map:
           return { "map_id" : None }

       parents["map_id"] = _map.primary_id
       return parents

    columns = \
        { "filename"
        , "filehash"
        , "load_level"
        , "speed"
        , "type"
        , "game_type"
        , "real_type"
        , "category"
        , "is_ladder"
        , "is_private"
        , "region"
        , "game_fps"
        , "frames"
        , "build"
        , "base_build"
        , "release_string"
        , "amm"
        , "competitive"
        , "practice"
        , "cooperative"
        , "battle_net"
        , "hero_duplicates_allowed"
        , "map_name"
        , "expansion"
        , "windows_timestamp"
        , "unix_timestamp"
        , "end_time"
        , "time_zone"
        , "start_time"
        , "date"
        }
