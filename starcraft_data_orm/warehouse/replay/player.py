from sqlalchemy import Column, Integer, Text, Boolean, BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import relationship

from collections import defaultdict

from starcraft_data_orm.warehouse.replay.info import info
from starcraft_data_orm.warehouse.replay.user import user
from starcraft_data_orm.warehouse.base import WarehouseBase
from starcraft_data_orm.inject import Injectable

class player(Injectable, WarehouseBase):
    __tablename__ = "player"
    __table_args__ = ( UniqueConstraint("pid", "info_id", name="pid_info_id_unique")
                     , { "schema": 'replay' } )

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

    owned_objects = relationship( "object", primaryjoin="object.owner_id==player.primary_id", back_populates="owner")

    basic_command_events = relationship("basic_command_event", back_populates="player")
    chat_events = relationship("chat_event", back_populates="player")
    player_stats_events = relationship("player_stats_event", back_populates="player")
    player_leave_events = relationship("player_leave_event", back_populates="player")
    upgrade_complete_events = relationship("upgrade_complete_event", back_populates="player")

    @classmethod
    @property
    def __tableschema__(self):
        return "replay"

    @classmethod
    async def process(cls, replay, session):
       players = []
       for player in replay.players:
           data = cls.get_data(player)
           data["scaled_rating"]= player.init_data.get("scaled_rating")
           parents = await cls.process_dependancies(player, replay, session)
           players.append(cls(**data, **parents))

       session.add_all(players)

    @classmethod
    async def process_dependancies(cls, obj, replay, session):
       _uid, _filehash = obj.detail_data.get("bnet").get("uid"), replay.filehash
       parents = defaultdict(lambda:None)

       user_statement = select(user).where(user.uid == _uid)
       user_result = await session.execute(user_statement)
       _user = user_result.scalar()

       info_statement = select(info).where(info.filehash == _filehash)
       info_result = await session.execute(info_statement)
       _info = info_result.scalar()

       parents['user_id'] = _user.primary_id
       parents['info_id'] = _info.primary_id

       return parents

    columns = \
        { "pid"
        , "team_id"
        , "is_human"
        , "is_observer"
        , "is_referee"
        , "toon_id"
        , "clan_tag"
        , "highest_league"
        , "scaled_rating"
        , "result"
        , "pick_race"
        , "play_race"
        }
