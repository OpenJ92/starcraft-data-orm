import pytest
from unittest.mock import AsyncMock, MagicMock

from starcraft_data_orm.warehouse.datapack.unit_type import unit_type
from tests.test_warehouse.test_datapack.unit_type_factory import UnitTypeFactory


@pytest.mark.asyncio
async def test_process_existence():
    # Arrange
    mock_replay = MagicMock()
    mock_replay.release_string = "1.23.4"

    mock_session = AsyncMock()
    mock_session.add_all = MagicMock()

    mock_execute_result = MagicMock()
    mock_execute_result.first.return_value = UnitTypeFactory()
    mock_session.execute.return_value = mock_execute_result

    # Act
    result = await unit_type.process_existence(mock_replay, mock_session)

    # Assert
    assert result is not None
    mock_session.add_all.assert_not_called()  # Nothing should be added


@pytest.mark.asyncio
async def test_process():
    mock_replay = MagicMock()
    mock_replay.release_string = "1.0.0"  # Match the factory's release_string

    # Use the factory to generate realistic unit data
    mock_replay.datapack.units = {
        1: UnitTypeFactory(name="Marine", race="Terran"),
        2: UnitTypeFactory(name="Zealot", race="Protoss"),
    }

    mock_session = AsyncMock()
    mock_session.add_all = MagicMock()

    # Mocking session.execute().first() to return None (no rows found)
    mock_execute_result = MagicMock()
    mock_execute_result.first.return_value = None
    mock_session.execute.return_value = mock_execute_result

    # Act
    await unit_type.process(mock_replay, mock_session)

    # Assert
    mock_session.add_all.assert_called_once()  # Ensure units are added
    added_units = mock_session.add_all.call_args[0][0]  # Extract the added units
    assert len(added_units) == 2

    # Validate the added unit data
    assert added_units[0].name == "Marine"
    assert added_units[0].race == "Terran"

    assert added_units[1].name == "Zealot"
    assert added_units[1].race == "Protoss"
