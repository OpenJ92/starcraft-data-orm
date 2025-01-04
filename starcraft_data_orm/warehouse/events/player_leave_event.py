from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, and_
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from collections import defaultdict

from starcraft_data_orm.warehouse.replay.player import player
from starcraft_data_orm.warehouse.replay.info import info
from starcraft_data_orm.inject import Injectable
from starcraft_data_orm.warehouse.base import WarehouseBase


class player_leave_event(Injectable, WarehouseBase):
    __tablename__ = "player_leave_event"
    __table_args__ = {"schema": "events"}

    primary_id = Column(Integer, primary_key=True)

    frame = Column(Integer)
    second = Column(Integer)
    is_local = Column(Boolean)
    leave_reason = Column(Integer)

    player_id = Column(Integer, ForeignKey("replay.player.primary_id"))
    player = relationship("player", back_populates="player_leave_events")

    info_id = Column(Integer, ForeignKey("replay.info.primary_id"))
    info = relationship("info", back_populates="player_leave_events")

    @classmethod
    @property
    def __tableschema__(self):
        return "events"

    @classmethod
    async def process(cls, replay, session):
       events = replay.events_dictionary['ChatEvent']

       _events = []
       for event in events:
           data = cls.get_data(event)
           parents = await cls.process_dependancies(event, replay, session)

           _events.append(cls(**data, **parents))

       session.add_all(_events)

    @classmethod
    async def process_dependancies(cls, event, replay, session):
       _player, _info = event.player.pid, replay.filehash
       parents = defaultdict(lambda:None)

       info_statement = select(info).where(info.filehash == _info)
       info_result = await session.execute(info_statement)
       _info = info_result.scalar()
       parents['info_id'] = _info.primary_id

       player_statement = select(player).where(and_(player.pid == _player, player.info_id == _info.primary_id))
       player_result = await session.execute(player_statement)
       _player = player_result.scalar()
       parents['player_id'] = _player.primary_id

       return parents

    columns = \
        { "frame"
        , "second"
        , "is_local"
        , "leave_reason"
        }
