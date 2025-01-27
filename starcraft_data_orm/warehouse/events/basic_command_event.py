from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, and_
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from collections import defaultdict

from starcraft_data_orm.warehouse.datapack.ability import ability
from starcraft_data_orm.warehouse.replay.info import info
from starcraft_data_orm.warehouse.replay.player import player
from starcraft_data_orm.inject import Injectable
from starcraft_data_orm.warehouse.base import WarehouseBase


class basic_command_event(Injectable, WarehouseBase):
    __tablename__ = "basic_command_event"
    __table_args__ = {"schema": "events"}

    primary_id = Column(Integer, primary_key=True)

    frame = Column(Integer)
    second = Column(Integer)
    is_local = Column(Boolean)
    has_ability = Column(Boolean)
    ability_name = Column(Text)

    player_id = Column(Integer, ForeignKey("replay.player.primary_id"))
    player = relationship("player", back_populates="basic_command_events")

    info_id = Column(Integer, ForeignKey("replay.info.primary_id"))
    info = relationship("info", back_populates="basic_command_events")

    ability_id = Column(Integer, ForeignKey("datapack.ability.primary_id"))
    ability = relationship("ability", back_populates="basic_command_events")

    @classmethod
    def __tableschema__(self):
        return "events"

    @classmethod
    async def process(cls, replay, session):
        events = replay.events_dictionary["BasicCommandEvent"]

        _events = []
        for event in events:
            data = cls.get_data(event)
            parents = await cls.process_dependancies(event, replay, session)

            _events.append(cls(**data, **parents))

        session.add_all(_events)

    @classmethod
    async def process_dependancies(cls, event, replay, session):
        _player, _info, _ability = event.player, replay.filehash, event.ability
        parents = defaultdict(lambda: None)

        parents["info_id"] = await info.get_primary_id(session, _info)
        parents["player_id"] = await player.get_primary_id(session, _player.pid, parents["info_id"])

        if not event.ability:
            return parents

        ability_statement = select(ability).where(
            and_(
                ability.id == _ability.id,
                ability.release_string == replay.release_string,
            )
        )
        ability_result = await session.execute(ability_statement)
        _ability = ability_result.scalar()
        parents["ability_id"] = _ability.primary_id

        return parents

    columns = {"frame", "second", "is_local", "has_ability", "ability_name"}
