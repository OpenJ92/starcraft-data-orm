from sqlalchemy import Column, Integer, Text, Float, ForeignKey, and_
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import insert

from collections import defaultdict

from starcraft_data_orm.warehouse.replay.info import info
from starcraft_data_orm.warehouse.replay.object import object
from starcraft_data_orm.inject import Injectable
from starcraft_data_orm.warehouse.base import WarehouseBase


class unit_born_event(Injectable, WarehouseBase):
    __tablename__ = "unit_born_event"
    __table_args__ = {"schema": "events"}

    primary_id = Column(Integer, primary_key=True)

    frame = Column(Integer)
    second = Column(Integer)
    x = Column(Float)
    y = Column(Float)

    info_id = Column(Integer, ForeignKey("replay.info.primary_id"))
    info = relationship("info", back_populates="unit_born_events")

    unit_id = Column(Integer, ForeignKey("replay.object.primary_id"))
    unit = relationship("object", back_populates="unit_born_events")

    @classmethod
    def __tableschema__(self):
        return "events"

    @classmethod
    async def process(cls, replay, session):
        events = replay.events_dictionary["UnitBornEvent"]

        _events = []
        for event in events:
            data = cls.get_data(event)
            parents = await cls.process_dependancies(event, replay, session)

            _events.append(cls({**data, **parents}))

        session.add_all(_events)

    @classmethod
    async def process_dependancies(cls, event, replay, session):
        _info, _unit = replay.filehash, event.unit_id
        parents = {"info_id":None, "unit_id":None}

        parents["info_id"] = await info.get_primary_id(session, _info)
        parents["unit_id"] = await object.get_primary_id(session, _unit, parents["info_id"])

        return parents

    columns = {"frame", "second", "x", "y"}
