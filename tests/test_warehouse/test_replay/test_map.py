import pytest
from unittest.mock import AsyncMock, MagicMock

from starcraft_data_orm.warehouse.replay.map import map
from tests.test_warehouse.test_replay.map_factory import MapFactory

@pytest.mark.asyncio
async def test_process_map_exists():
    mock_replay = MagicMock()
    mock_replay.release_string = "1.23.4"

    mock_session = AsyncMock()
    mock_session.add_all = MagicMock()

    mock_execute_result = MagicMock()
    mock_execute_result.first.return_value = MapFactory()
    mock_session.execute.return_value = mock_execute_result

    result = await map.process_existence(mock_replay, mock_session)

    assert result is not None
    mock_session.add.assert_not_called()

@pytest.mark.asyncio
async def test_process_map_does_not_exist():
    mock_replay = MagicMock()
    mock_replay.release_string = "1.0.0"  # Match the factory's release_string

    mock_replay.map = MapFactory(filename="name.SC2Replay")
    mock_replay.load_map.return_value = None

    mock_session = AsyncMock()
    mock_session.add = MagicMock()

    mock_execute_result = MagicMock()
    mock_execute_result.scalar.return_value = None
    mock_session.execute.return_value = mock_execute_result

    await map.process(mock_replay, mock_session)

    mock_session.add.called_once()
    added_map = mock_session.add.call_args[0][0]

    assert added_map.filename == "name.SC2Replay"


