from sqlalchemy import Column, Integer, Text, Boolean, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.exc import  SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from starcraft_data_orm.inject import Injectable
from starcraft_data_orm.warehouse.base import WarehouseBase


class unit_type(WarehouseBase, Injectable):
    __tablename__ = "unit_type"
    __table_args__ = ( UniqueConstraint("id", "release_string", name="unit_type_id_release_string_unique")
                     , { "schema": 'datapack' } )

    primary_id = Column(Integer, primary_key=True)
    release_string = Column(Text)
    id = Column(Integer, nullable=False)
    str_id = Column(Text, nullable=False)
    name = Column(Text)
    title = Column(Text)
    race = Column(Text)
    minerals = Column(Integer)
    vespene = Column(Integer)
    supply = Column(Integer)
    is_building = Column(Boolean)
    is_army = Column(Boolean)
    is_worker = Column(Boolean)

    abilities = relationship("ability", back_populates="build_unit")
    objects = relationship("object", back_populates="unit_type")

    @classmethod
    @property
    def __tableschema__(self):
        return "datapack"

    @classmethod
    async def process(cls, replay, session):
        if await cls.process_existence(replay, session):
            return

        units = []
        for _, unit in unit_type.get_unique(replay).items():
            data = cls.get_data(unit)
            units.append(cls(release_string=replay.release_string, **data))
        session.add_all(units)

    @classmethod
    async def process_existence(cls, replay, session):
        statement = select(cls).where(cls.release_string == replay.release_string)
        result = await session.execute(statement)
        return result.first()

    @classmethod
    def get_unique(cls, replay):
        units = {}
        for _, unit in replay.datapack.units.items():
            units[unit.id] = unit
        return units

    columns = \
        { "id"
        , "str_id"
        , "name"
        , "title"
        , "race"
        , "minerals"
        , "vespene"
        , "supply"
        , "is_building"
        , "is_army"
        , "is_worker"
        }


