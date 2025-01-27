from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, and_
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from collections import defaultdict

from starcraft_data_orm.warehouse.replay.player import player
from starcraft_data_orm.warehouse.replay.info import info
from starcraft_data_orm.inject import Injectable
from starcraft_data_orm.warehouse.base import WarehouseBase


class chat_event(Injectable, WarehouseBase):
    __tablename__ = "chat_event"
    __table_args__ = {"schema": "events"}

    primary_id = Column(Integer, primary_key=True)

    frame = Column(Integer)
    second = Column(Integer)
    target = Column(Integer)
    text = Column(Text)
    to_all = Column(Boolean)
    to_allies = Column(Boolean)
    to_observers = Column(Boolean)

    player_id = Column(Integer, ForeignKey("replay.player.primary_id"))
    player = relationship("player", back_populates="chat_events")

    info_id = Column(Integer, ForeignKey("replay.info.primary_id"))
    info = relationship("info", back_populates="chat_events")

    @classmethod
    def __tableschema__(self):
        return "events"

    @classmethod
    async def process(cls, replay, session):
        events = replay.events_dictionary["ChatEvent"]

        _events = []
        for event in events:
            data = cls.get_data(event)
            parents = await cls.process_dependancies(event, replay, session)

            _events.append(cls(**data, **parents))

        session.add_all(_events)

    @classmethod
    async def process_dependancies(cls, event, replay, session):
        _player, _info = event.player, replay.filehash
        parents = defaultdict(lambda: None)

        parents["info_id"] = await info.get_primary_id(session, _info)
        parents["player_id"] = await player.get_primary_id(session, _player.pid, parents["info_id"])

        return parents

    columns = {
        "frame",
        "second",
        "target",
        "text",
        "to_all",
        "to_allies",
        "to_observers",
    }
