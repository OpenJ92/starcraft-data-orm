from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from database.inject import Injectable
from database.base import Base

class ability(Injectable, Base):
    __tablename__ = "ability"
    __tableschema__ = "datapack"
    __table_args__ = ( UniqueConstraint("id", "release_string", name="ability_id_release_string_unique")
                     , {"schema": __tableschema__})

    __id__ = Column(Integer, primary_key=True)

    release_string = Column(Text, nullable=False)
    id = Column(Integer, nullable=False)
    version = Column(Text)
    name = Column(Text)
    title = Column(Text)
    is_build = Column(Boolean)
    build_time = Column(Integer)

    __unit_type__ = Column(Integer, ForeignKey("datapack.unit_type.__id__"))
    build_unit = relationship("unit_type", back_populates="abilities")

    basic_command_events = relationship("basic_command_event", back_populates="ability")

    @classmethod
    @property
    def __tableschema__(self):
        return "datapack"

    @classmethod
    def process_foreign_relations(cls, obj, session):
        pass

    @classmethod
    def process_existence(cls, replay, session):
        statement = select(cls).where(cls.release_string == replay.release_string)
        result = session.execute(statement)
        return result.first() is not None

    @classmethod
    def extract_data(cls, replay, foreign_relations):
        pass


