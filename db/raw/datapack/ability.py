from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

class ability(Base):
    __tablename__ = "ability"
    __table_args__ = ({"schema": "datapack"},
        UniqueConstraint("id", "release_string", name="ability_id_release_string_unique"),)

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
