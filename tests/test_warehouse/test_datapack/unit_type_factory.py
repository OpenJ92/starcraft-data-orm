from factory import Factory, Sequence, Faker, Iterator
from factory.alchemy import SQLAlchemyModelFactory

from starcraft_data_orm.warehouse.config import SyncSessionLocal
from starcraft_data_orm.warehouse.datapack.unit_type import unit_type

class UnitTypeFactory(Factory):
    class Meta:
        model = unit_type

    release_string = "1.0.0"
    id = Sequence(lambda n: n)
    str_id = Faker("word")
    name = Faker("name")
    title = Faker("name")
    race = Iterator(["Terran", "Protoss", "Zerg"])
    minerals = Faker("random_int", min=50, max=500)
    vespene = Faker("random_int", min=0, max=500)
    supply = Faker("random_int", min=0, max=10)
    is_building = Faker("boolean")
    is_army   = Faker("boolean")
    is_worker = Faker("boolean")
