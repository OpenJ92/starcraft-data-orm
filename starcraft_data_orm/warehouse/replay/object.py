from sqlalchemy import Column, Integer, Text, LargeBinary, ForeignKey, and_ 
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import insert

from collections import defaultdict
from functools import lru_cache

from starcraft_data_orm.inject import Injectable
from starcraft_data_orm.warehouse.base import WarehouseBase

from starcraft_data_orm.warehouse.replay.info import info
from starcraft_data_orm.warehouse.replay.player import player
from starcraft_data_orm.warehouse.replay.user import user
from starcraft_data_orm.warehouse.datapack.unit_type import unit_type


class object(Injectable, WarehouseBase):
    __tablename__ = "object"
    __table_args__ = {"schema": "replay"}
    _cache = {}

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
        back_populates="owned_objects",
    )

    unit_type_id = Column(Integer, ForeignKey("datapack.unit_type.primary_id"))
    unit_type = relationship(
        "unit_type",
        primaryjoin="object.unit_type_id==unit_type.primary_id",
        back_populates="objects",
    )

    unit_born_events = relationship("unit_born_event", back_populates="unit")
    unit_done_events = relationship("unit_done_event", back_populates="unit")
    unit_init_events = relationship("unit_init_event", back_populates="unit")
    unit_died_events = relationship(
        "unit_died_event",
        primaryjoin="unit_died_event.unit_id==object.primary_id",
        back_populates="unit",
    )
    kill_events = relationship(
        "unit_died_event",
        primaryjoin="unit_died_event.killing_unit_id==object.primary_id",
        back_populates="killing_unit",
    )

    @classmethod
    def __tableschema__(self):
        return "replay"

    @classmethod
    async def process(cls, replay, session):
        _objects = []
        for _, obj in replay.objects.items():
            data = cls.get_data(obj)
            parents = await cls.process_dependancies(obj, replay, session)
            _objects.append(cls(**data, **parents))

        session.add_all(_objects)

    @classmethod
    async def process_dependancies(cls, obj, replay, session):
        _unit, _info, _player = obj._type_class, replay.filehash, obj.owner
        parents = {"info_id":None, "unit_type_id":None, "owner_id":None}

        parents["info_id"] = await info.get_primary_id(session, _info)

        if _unit:
            parents["unit_type_id"] = await unit_type.get_primary_id(session, _unit.id, replay.release_string)

        if _player:
            parents["owner_id"] = await player.get_primary_id(session, _player.pid, parents["info_id"])

        return parents

    @classmethod
    async def get_primary_id(cls, session, id, info_id):
        if (id, info_id) in cls._cache:
            return cls._cache[(id, info_id)]

        statement = select(cls.primary_id).where(and_(cls.info_id==info_id, cls.id == id))
        result = await session.execute(statement)

        cls._cache[(id, info_id)] = result.scalar()
        return cls._cache[(id, info_id)]

    @classmethod
    def get_data(cls, obj):
        parameters = defaultdict(lambda: None)
        for variable, value in vars(obj).items():
            if variable in cls.columns:
                parameters[variable] = value
        parameters['name'] = obj.name
        return parameters

    columns = {"id", "started_at", "finished_at", "died_at", "name"}
