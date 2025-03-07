from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    BigInteger,
    ForeignKey,
    UniqueConstraint,
    and_,
)
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import relationship

from collections import defaultdict
from functools import lru_cache

from starcraft_data_orm.util.LRUCache import LRUCache
from starcraft_data_orm.warehouse.replay.info import info
from starcraft_data_orm.warehouse.replay.user import user
from starcraft_data_orm.warehouse.base import WarehouseBase
from starcraft_data_orm.inject import Injectable


class player(Injectable, WarehouseBase):
    __tablename__ = "player"
    __table_args__ = (
        UniqueConstraint("pid", "info_id", name="pid_info_id_unique"),
        {"schema": "replay"},
    )
    _cache = LRUCache(maxsize=600)

    primary_id = Column(Integer, primary_key=True)

    pid = Column(Integer)
    team_id = Column(Integer)
    is_human = Column(Boolean)
    is_observer = Column(Boolean)
    is_referee = Column(Boolean)
    toon_id = Column(BigInteger)
    clan_tag = Column(Text)
    highest_league = Column(Integer)
    scaled_rating = Column(Integer)
    result = Column(Text)
    pick_race = Column(Text)
    play_race = Column(Text)

    info_id = Column(Integer, ForeignKey("replay.info.primary_id"))
    replay = relationship("info", back_populates="players")

    user_id = Column(Integer, ForeignKey("replay.user.primary_id"))
    user = relationship("user", back_populates="players")

    owned_objects = relationship(
        "object",
        primaryjoin="object.owner_id==player.primary_id",
        back_populates="owner",
    )

    basic_command_events = relationship("basic_command_event", back_populates="player")
    chat_events = relationship("chat_event", back_populates="player")
    player_stats_events = relationship("player_stats_event", back_populates="player")
    player_leave_events = relationship("player_leave_event", back_populates="player")
    upgrade_complete_events = relationship(
        "upgrade_complete_event", back_populates="player"
    )

    @classmethod
    def __tableschema__(self):
        return "replay"

    @classmethod
    async def process(cls, replay, session):
        players = []
        for player in replay.players:
            data = cls.get_data(player)

            if player.is_human:
                data["scaled_rating"] = player.init_data.get("scaled_rating")

            parents = await cls.process_dependancies(player, replay, session)
            players.append(cls(**data, **parents))

        session.add_all(players)

    @classmethod
    async def process_dependancies(cls, obj, replay, session):
        _uid, _filehash = obj.detail_data.get("bnet").get("uid"), replay.filehash
        parents = defaultdict(lambda: None)

        parents["info_id"] = await info.get_primary_id(session, _filehash)
        parents["user_id"] = await user.get_primary_id(session, _uid)

        return parents

    @classmethod
    async def get_primary_id(cls, session, pid, info_id):
        cached_value = cls._cache.get((pid, info_id))
        if cached_value is not None:
            return cached_value

        statement = select(cls.primary_id).where(and_(cls.info_id==info_id, cls.pid == pid))
        result = await session.execute(statement)

        primary_id = result.scalar()
        cls._cache.set((pid, info_id), primary_id)

        return primary_id

    columns = {
        "pid",
        "team_id",
        "is_human",
        "is_observer",
        "is_referee",
        "toon_id",
        "clan_tag",
        "highest_league",
        "scaled_rating",
        "result",
        "pick_race",
        "play_race",
    }
