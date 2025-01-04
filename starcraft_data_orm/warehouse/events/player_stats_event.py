from sqlalchemy import Column, Integer, Float, Text, Boolean, ForeignKey, and_
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from collections import defaultdict

from starcraft_data_orm.warehouse.replay.player import player
from starcraft_data_orm.warehouse.replay.info import info
from starcraft_data_orm.inject import Injectable
from starcraft_data_orm.warehouse.base import WarehouseBase

class player_stats_event(Injectable, WarehouseBase):
    __tablename__ = "player_stats_event"
    __table_args__ = {"schema": "events"}

    primary_id = Column(Integer, primary_key=True)

    name = Column(Text)
    second = Column(Float)
    minerals_current = Column(Float)
    vespene_current = Column(Float)
    minerals_collection_rate = Column(Float)
    vespene_collection_rate = Column(Float)
    workers_active_count = Column(Float)
    minerals_used_in_progress_army = Column(Float)
    minerals_used_in_progress_economy = Column(Float)
    minerals_used_in_progress_technology = Column(Float)
    minerals_used_in_progress = Column(Float)
    vespene_used_in_progress_army = Column(Float)
    vespene_used_in_progress_economy = Column(Float)
    vespene_used_in_progress_technology = Column(Float)
    vespene_used_in_progress = Column(Float)
    resources_used_in_progress = Column(Float)
    minerals_used_current_army = Column(Float)
    minerals_used_current_economy = Column(Float)
    minerals_used_current_technology = Column(Float)
    minerals_used_current = Column(Float)
    vespene_used_current_army = Column(Float)
    vespene_used_current_economy = Column(Float)
    vespene_used_current_technology = Column(Float)
    vespene_used_current = Column(Float)
    resources_used_current = Column(Float)
    minerals_lost_army = Column(Float)
    minerals_lost_economy = Column(Float)
    minerals_lost_technology = Column(Float)
    minerals_lost = Column(Float)
    vespene_lost_army = Column(Float)
    vespene_lost_economy = Column(Float)
    vespene_lost_technology = Column(Float)
    vespene_lost = Column(Float)
    resources_lost = Column(Float)
    minerals_killed_army = Column(Float)
    minerals_killed_economy = Column(Float)
    minerals_killed_technology = Column(Float)
    minerals_killed = Column(Float)
    vespene_killed_army = Column(Float)
    vespene_killed_economy = Column(Float)
    vespene_killed_technology = Column(Float)
    vespene_killed = Column(Float)
    resources_killed = Column(Float)
    food_used = Column(Float)
    food_made = Column(Float)
    minerals_used_active_forces = Column(Float)
    vespene_used_active_forces = Column(Float)
    ff_minerals_lost_army = Column(Float)
    ff_minerals_lost_economy = Column(Float)
    ff_minerals_lost_technology = Column(Float)
    ff_vespene_lost_army = Column(Float)
    ff_vespene_lost_economy = Column(Float)
    ff_vespene_lost_technology = Column(Float)

    player_id = Column(Integer, ForeignKey("replay.player.primary_id"))
    player = relationship("player", back_populates="player_stats_events")

    info_id = Column(Integer, ForeignKey("replay.info.primary_id"))
    info = relationship("info", back_populates="player_stats_events")

    @classmethod
    @property
    def __tableschema__(self):
        return "events"

    @classmethod
    async def process(cls, replay, session):
       events = replay.events_dictionary['PlayerStatsEvent']

       _events = []
       for event in events:
           data = cls.get_data(event)
           parents = await cls.process_dependancies(event, replay, session)

           _events.append(cls(**data, **parents))

       session.add_all(_events)

    @classmethod
    async def process_dependancies(cls, event, replay, session):
       _player, _info = event.player.pid, replay.filehash
       parents = defaultdict(lambda:None)

       info_statement = select(info).where(info.filehash == _info)
       info_result = await session.execute(info_statement)
       _info = info_result.scalar()
       parents['info_id'] = _info.primary_id

       player_statement = select(player).where(and_(player.pid == _player, player.info_id == _info.primary_id))
       player_result = await session.execute(player_statement)
       _player = player_result.scalar()
       parents['player_id'] = _player.primary_id

       return parents

    columns = \
        { "second"
        , "minerals_current"
        , "vespene_current"
        , "minerals_collection_rate"
        , "vespene_collection_rate"
        , "workers_active_count"
        , "minerals_used_in_progress_army"
        , "minerals_used_in_progress_economy"
        , "minerals_used_in_progress_technology"
        , "minerals_used_in_progress"
        , "vespene_used_in_progress_army"
        , "vespene_used_in_progress_economy"
        , "vespene_used_in_progress_technology"
        , "vespene_used_in_progress"
        , "resources_used_in_progress"
        , "minerals_used_current_army"
        , "minerals_used_current_economy"
        , "minerals_used_current_technology"
        , "minerals_used_current"
        , "vespene_used_current_army"
        , "vespene_used_current_economy"
        , "vespene_used_current_technology"
        , "vespene_used_current"
        , "resources_used_current"
        , "minerals_lost_army"
        , "minerals_lost_economy"
        , "minerals_lost_technology"
        , "minerals_lost"
        , "vespene_lost_army"
        , "vespene_lost_economy"
        , "vespene_lost_technology"
        , "vespene_lost"
        , "resources_lost"
        , "minerals_killed_army"
        , "minerals_killed_economy"
        , "minerals_killed_technology"
        , "minerals_killed"
        , "vespene_killed_army"
        , "vespene_killed_economy"
        , "vespene_killed_technology"
        , "vespene_killed"
        , "resources_killed"
        , "food_used"
        , "food_made"
        , "minerals_used_active_forces"
        , "vespene_used_active_forces"
        , "ff_minerals_lost_army"
        , "ff_minerals_lost_economy"
        , "ff_minerals_lost_technology"
        , "ff_vespene_lost_army"
        , "ff_vespene_lost_economy"
        , "ff_vespene_lost_technology"
        }
