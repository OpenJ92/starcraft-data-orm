import pytest
from unittest.mock import AsyncMock, MagicMock

from starcraft_data_orm.warehouse.datapack.ability import ability
from tests.test_warehouse.test_datapack.unit_type_factory import UnitTypeFactory
from tests.test_warehouse.test_datapack.ability_factory import AbilityFactory

@pytest.mark.asyncio
async def test_process_existence():
    # Arrange
    mock_replay = AsyncMock()
    mock_replay.release_string = "1.0.0"

    mock_session = AsyncMock()
    mock_execute_result = MagicMock()
    mock_execute_result.scalar.return_value = AbilityFactory()
    mock_session.execute.return_value = mock_execute_result

    # Act
    result = await ability.process_existence(mock_replay, mock_session)

    # Assert
    assert result is not None
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_process_dependancies():
    # Arrange
    mock_unit_type = UnitTypeFactory(primary_id=42)
    mock_ability = AbilityFactory(build_unit=mock_unit_type)

    mock_replay = AsyncMock()
    mock_replay.release_string = "1.0.0"

    mock_session = AsyncMock()
    mock_execute_result = MagicMock()
    mock_execute_result.scalar.return_value = mock_unit_type
    mock_session.execute.return_value = mock_execute_result

    # Act
    parents = await ability.process_dependancies(mock_ability, mock_replay, mock_session)

    # Assert
    assert parents == { "unit_type_id": 42 }
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_process():
    # Arrange
    mock_replay = AsyncMock()
    mock_replay.release_string = "1.0.0"

    unit_1 = UnitTypeFactory(primary_id=10)
    unit_2 = UnitTypeFactory(primary_id=20)

    mock_replay.datapack.abilities = {
        1: AbilityFactory(name="Build Barracks", build_unit=unit_1),
        2: AbilityFactory(name="Build Command Center", unit_type_id=unit_2),
    }

    mock_session = AsyncMock()
    mock_session.add_all = MagicMock()

    mock_execute_results = iter([
        MagicMock(scalar=MagicMock(return_value=None)),
        MagicMock(scalar=MagicMock(return_value=unit_1)),  # First call
        MagicMock(scalar=MagicMock(return_value=unit_2)),  # Second call
    ])

    mock_session.execute.side_effect = lambda *args, **kwargs: next(mock_execute_results)

    # Act
    await ability.process(mock_replay, mock_session)

    # Assert
    mock_session.add_all.assert_called_once()
    added_abilities = mock_session.add_all.call_args[0][0]
    assert len(added_abilities) == 2

    # Validate the added ability data
    assert added_abilities[0].name == "Build Barracks"
    assert added_abilities[0].unit_type_id == 10

    assert added_abilities[1].name == "Build Command Center"
    assert added_abilities[1].unit_type_id == 20


