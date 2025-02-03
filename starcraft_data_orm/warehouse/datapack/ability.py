from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    and_,
)
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import relationship

from starcraft_data_orm.util.LRUCache import LRUCache
from starcraft_data_orm.warehouse.datapack.unit_type import unit_type
from starcraft_data_orm.warehouse.base import WarehouseBase
from starcraft_data_orm.inject import Injectable


class ability(Injectable, WarehouseBase):
    __tablename__ = "ability"
    __table_args__ = (
        UniqueConstraint(
            "id", "release_string", name="ability_id_release_string_unique"
        ),
        {"schema": "datapack"},
    )
    _cache = LRUCache(maxsize=20000)

    primary_id = Column(Integer, primary_key=True)

    release_string = Column(Text, nullable=False)
    id = Column(Integer, nullable=False)
    version = Column(Text)
    name = Column(Text)
    title = Column(Text)
    is_build = Column(Boolean)
    build_time = Column(Integer)

    unit_type_id = Column(Integer, ForeignKey("datapack.unit_type.primary_id"))
    build_unit = relationship("unit_type", back_populates="abilities")

    basic_command_events = relationship("basic_command_event", back_populates="ability")

    @classmethod
    def __tableschema__(self):
        return "datapack"

    @classmethod
    async def process(cls, replay, session):
        if await cls.process_existence(replay, session):
            return

        abilities = []
        for _, ability in replay.datapack.abilities.items():
            data = cls.get_data(ability)
            parents = await cls.process_dependancies(ability, replay, session)
            abilities.append(
                cls(release_string=replay.release_string, **data, **parents)
            )

        session.add_all(abilities)

    @classmethod
    async def process_existence(cls, replay, session):
        statement = select(cls).where(cls.release_string == replay.release_string)
        result = await session.execute(statement)
        return result.scalar()

    @classmethod
    async def process_dependancies(cls, ability, replay, session):
        unit = ability.build_unit
        parents = {"unit_type_id" : None}

        if not unit:
            return parents

        parents["unit_type_id"] = await unit_type.get_primary_id(session, unit.id, replay.release_string)
        return parents

    @classmethod
    async def get_primary_id(cls, session, id, release_string):
        cached_value = cls._cache.get((id, release_string))
        if cached_value is not None:
            return cached_value

        statement = select(cls.primary_id).where(and_(cls.id==id,cls.release_string==release_string))
        result = await session.execute(statement)

        primary_id = result.scalar()
        cls._cache.set((id, release_string), primary_id)

        return primary_id

    columns = {"id", "version", "name", "title", "is_build", "build_time"}
