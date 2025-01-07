from factory import Factory, Faker, SubFactory, LazyAttribute
from starcraft_data_orm.warehouse.replay.info import info
from tests.test_warehouse.test_replay.map_factory import MapFactory


class InfoFactory(Factory):
    class Meta:
        model = info

    # Basic fields
    filename = Faker("file_name", extension="sc2replay")
    filehash = Faker("md5")
    load_level = Faker("random_int", min=1, max=10)
    speed = Faker("word")
    type = Faker("word")
    game_type = Faker("word")
    real_type = Faker("word")
    category = Faker("word")
    is_ladder = Faker("boolean")
    is_private = Faker("boolean")
    region = Faker("country_code")
    game_fps = Faker("pyfloat", min_value=30.0, max_value=240.0)
    frames = Faker("random_int", min=0, max=100000)
    build = Faker("random_int", min=10000, max=99999)
    base_build = Faker("random_int", min=10000, max=99999)
    release_string = Faker("numerify", text="1.0.%##")  # Example: 1.0.42
    amm = Faker("random_int", min=0, max=1)
    competitive = Faker("random_int", min=0, max=1)
    practice = Faker("random_int", min=0, max=1)
    cooperative = Faker("random_int", min=0, max=1)
    battle_net = Faker("random_int", min=0, max=1)
    hero_duplicates_allowed = Faker("random_int", min=0, max=1)
    expansion = Faker("word")
    windows_timestamp = Faker("unix_time")
    unix_timestamp = Faker("unix_time")
    end_time = Faker("date_time")
    time_zone = Faker("pyfloat", min_value=-12.0, max_value=14.0)
    start_time = Faker("date_time")
    date = Faker("date_time")

    # Relationships
    map = SubFactory(MapFactory)
    map_id = LazyAttribute(lambda obj: obj.map.primary_id if obj.map else None)
    map_name = LazyAttribute(lambda obj: obj.map.name if obj.map else None)

