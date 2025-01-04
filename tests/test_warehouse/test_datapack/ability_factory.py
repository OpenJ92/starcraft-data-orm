from factory import Factory, Sequence, Faker, SubFactory, LazyAttribute

from starcraft_data_orm.warehouse.datapack.ability import ability
from tests.test_warehouse.test_datapack.unit_type_factory import UnitTypeFactory


class AbilityFactory(Factory):
    class Meta:
        model = ability

    primary_id = Sequence(lambda n: n)
    release_string = Faker("numerify", text="1.0.%##")  # Example: 1.0.42
    id = Faker("random_int", min=0, max=300)
    version = "1.0.0"
    name = Faker("word")
    title = Faker("sentence", nb_words=3)
    is_build = Faker("boolean")
    build_time = Faker("random_int", min=0, max=300)

    build_unit = SubFactory(UnitTypeFactory)  # Relates to unit_type
