from sqlalchemy import Column, Integer, Text, ForeignKey, and_
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from collections import defaultdict

from starcraft_data_orm.warehouse.replay.info import info
from starcraft_data_orm.warehouse.replay.object import object
from starcraft_data_orm.inject import Injectable
from starcraft_data_orm.warehouse.base import WarehouseBase

class unit_died_event(Injectable, WarehouseBase):
    __tablename__ = "unit_died_event"
    __table_args__ = {"schema": "events"}

    primary_id = Column(Integer, primary_key=True)

    frame = Column(Integer)
    second = Column(Integer)
    name = Column(Text)
    x = Column(Integer)
    y = Column(Integer)

    unit_id = Column(Integer, ForeignKey("replay.object.primary_id"))
    unit = relationship(
        "object",
        primaryjoin="unit_died_event.unit_id==object.primary_id",
        back_populates="unit_died_events",)

    killing_unit_id = Column(Integer, ForeignKey("replay.object.primary_id"))
    killing_unit = relationship(
        "object",
        primaryjoin="unit_died_event.killing_unit_id==object.primary_id",
        back_populates="kill_events",)

    info_id = Column(Integer, ForeignKey("replay.info.primary_id"))
    info = relationship("info", back_populates="unit_died_events")

    @classmethod
    @property
    def __tableschema__(self):
        return "events"

    @classmethod
    async def process(cls, replay, session):
       events = replay.events_dictionary['UnitDiedEvent']

       _events = []
       for event in events:
           data = cls.get_data(event)
           parents = await cls.process_dependancies(event, replay, session)

           _events.append(cls(**data, **parents))

       session.add_all(_events)

    @classmethod
    async def process_dependancies(cls, event, replay, session):
       _info, _unit, _killing_unit = replay.filehash, event.unit_id, event.killing_unit_id
       parents = defaultdict(lambda:None)

       info_statement = select(info).where(info.filehash == _info)
       info_result = await session.execute(info_statement)
       _info = info_result.scalar()
       parents['info_id'] = _info.primary_id

       unit_statement = select(object).where(
               and_(object.info_id == _info.primary_id, object.id == _unit))
       unit_result = await session.execute(unit_statement)
       _unit = unit_result.scalar()
       parents['unit_id'] = _unit.primary_id

       # Not all units have a killer.
       if not _killing_unit:
           return parents

       killing_unit_statement = select(object).where(
               and_(object.info_id == _info.primary_id, object.id == _killing_unit))
       killing_unit_result = await session.execute(killing_unit_statement)
       _killing_unit = killing_unit_result.scalar()

       parents['killing_unit_id'] = _killing_unit.primary_id

       return parents


    columns = \
        { "frame"
        , "second"
        , "x"
        , "y"
        }

