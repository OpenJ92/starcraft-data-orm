from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import relationship

from starcraft_data_orm.inject import Injectable
from starcraft_data_orm.warehouse.base import WarehouseBase

class user(Injectable, WarehouseBase):
    __tablename__ = "user"
    __table_args__ = ( UniqueConstraint("uid", name="uid_unique")
                     , { "schema": 'replay' } )

    primary_id = Column(Integer, primary_key=True)

    name = Column(Text)
    uid = Column(Integer)
    region = Column(Integer)
    subregion = Column(Integer)

    players = relationship("player", back_populates="user")

    @classmethod
    @property
    def __tableschema__(self):
        return "replay"

    @classmethod
    async def process(cls, replay, session):
        users = []
        for player in replay.players:
            if await cls.process_existence(player, session):
                continue

            data = cls.get_data(player)
            users.append(cls(**data))

        session.add_all(users)


    @classmethod
    async def process_existence(cls, obj, session):
        statement = select(cls).where(cls.uid == obj.detail_data['bnet']['uid'])
        result = await session.execute(statement)
        return result.scalar()

    @classmethod
    def get_data(cls, obj):
        return { "name"      : obj.name
               , "uid"       : obj.detail_data.get("bnet").get("uid")
               , "region"    : obj.detail_data.get("bnet").get("region")
               , "subregion" : obj.detail_data.get("bnet").get("subregion")
               }

    columns = \
        { "name"
        , "uid"
        , "region"
        , "subregion"
        }

