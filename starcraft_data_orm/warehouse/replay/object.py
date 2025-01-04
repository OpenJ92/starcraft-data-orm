from sqlalchemy import Column, Integer, Text, LargeBinary, ForeignKey, and_
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from collections import defaultdict

from starcraft_data_orm.inject import Injectable
from starcraft_data_orm.warehouse.base import WarehouseBase

from starcraft_data_orm.warehouse.replay.info import info
from starcraft_data_orm.warehouse.replay.player import player
from starcraft_data_orm.warehouse.replay.user import user
from starcraft_data_orm.warehouse.datapack.unit_type import unit_type


class object(Injectable, WarehouseBase):
    __tablename__ = "object"
    __table_args__ = {"schema": "replay"}

    primary_id = Column(Integer, primary_key=True)

    id = Column(Integer)
    started_at = Column(Integer)
    finished_at = Column(Integer)
    died_at = Column(Integer)
    name = Column(Text)

    info_id = Column(Integer, ForeignKey("replay.info.primary_id"))
    replay = relationship("info", back_populates="objects")

    owner_id = Column(Integer, ForeignKey("replay.player.primary_id"))
    owner = relationship(
        "player",
        primaryjoin="object.owner_id==player.primary_id",
        back_populates="owned_objects",)


    unit_type_id = Column(Integer, ForeignKey("datapack.unit_type.primary_id"))
    unit_type = relationship(
        "unit_type",
        primaryjoin='object.unit_type_id==unit_type.primary_id',
        back_populates="objects")

    unit_born_events = relationship("unit_born_event", back_populates="unit")
    unit_done_events = relationship("unit_done_event", back_populates="unit")
    unit_init_events = relationship("unit_init_event", back_populates="unit")
    unit_died_events = relationship(
        "unit_died_event",
        primaryjoin="unit_died_event.unit_id==object.primary_id",
        back_populates="unit")
    kill_events = relationship(
        "unit_died_event",
        primaryjoin="unit_died_event.killing_unit_id==object.primary_id",
        back_populates="killing_unit",
    )

    @classmethod
    @property
    def __tableschema__(self):
        return "replay"

    @classmethod
    async def process(cls, replay, session):
       _objects = []
       for _, obj in replay.objects.items():
           data = cls.get_data(obj)
           parents = await cls.process_dependancies(obj, replay, session)
           if not parents:
               continue

           _objects.append(cls(**data, **parents))

       session.add_all(_objects)

    @classmethod
    async def process_dependancies(cls, obj, replay, session):
       _unit, _info, _player = obj._type_class, replay.filehash, obj.owner
       parents = defaultdict(lambda:None)

       unit_statement = select(unit_type).where(
               and_(unit_type.release_string == replay.release_string, unit_type.id == _unit.id))
       unit_result = await session.execute(unit_statement)
       _unit = unit_result.scalar()
       parents["unit_type_id"] = _unit.primary_id

       info_statement = select(info).where(info.filehash == _info)
       info_result = await session.execute(info_statement)
       _info = info_result.scalar()
       parents["info_id"] = _info.primary_id

       # Not all objects have an owner. They may have references in events, though.
       if not _player:
           return parents
       player_statement = select(player).where(
                       and_(player.info_id == _info.primary_id, player.pid == _player.pid))
       player_result = await session.execute(player_statement)
       _player = player_result.scalar()

       parents["owner_id"] = _player.primary_id

       return parents

    columns = \
        { "id"
        , "started_at"
        , "finished_at"
        , "died_at"
        , "name"
        }
