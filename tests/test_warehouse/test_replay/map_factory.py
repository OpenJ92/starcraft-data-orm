from factory import Factory, Sequence, Faker
from starcraft_data_orm.warehouse.replay.map import map


class MapFactory(Factory):
    class Meta:
        model = map

    filename = Faker("file_name", extension="sc2map")
    filehash = Faker("md5")
    name = Faker("word")
    author = Faker("name")
    description = Faker("sentence")
    website = Faker("url")

