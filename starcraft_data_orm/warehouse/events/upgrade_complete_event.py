from sqlalchemy import Column, Integer, Text, ForeignKey, and_
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from collections import defaultdict

from starcraft_data_orm.warehouse.replay.info import info
from starcraft_data_orm.warehouse.replay.player import player
from starcraft_data_orm.inject import Injectable
from starcraft_data_orm.warehouse.base import WarehouseBase


class upgrade_complete_event(Injectable, WarehouseBase):
    __tablename__ = "upgrade_complete_event"
    __table_args__ = {"schema": "events"}

    primary_id = Column(Integer, primary_key=True)

    frame = Column(Integer)
    second = Column(Integer)
    upgrade_type_name = Column(Text)
    count = Column(Integer)

    player_id = Column(Integer, ForeignKey("replay.player.primary_id"))
    player = relationship("player", back_populates="upgrade_complete_events")

    info_id = Column(Integer, ForeignKey("replay.info.primary_id"))
    info = relationship("info", back_populates="upgrade_complete_events")

    @classmethod
    def __tableschema__(self):
        return "events"

    @classmethod
    async def process(cls, replay, session):
        events = replay.events_dictionary["UpgradeCompleteEvent"]

        _events = []
        for event in events:
            data = cls.get_data(event)
            parents = await cls.process_dependancies(event, replay, session)

            _events.append(cls(**data, **parents))

        session.add_all(_events)

    @classmethod
    async def process_dependancies(cls, event, replay, session):
        _player, _info = event.player.pid, replay.filehash
        parents = defaultdict(lambda: None)

        parents["info_id"] = await info.get_primary_id(session, _info)
        parents["player_id"] = await player.get_primary_id(session, _player, parents["info_id"])

        return parents

    columns = {"frame", "second", "upgrade_type_name", "count"}
