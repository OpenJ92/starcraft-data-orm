import pytest
from unittest.mock import AsyncMock, MagicMock

from starcraft_data_orm.warehouse.replay.info import info
from tests.test_warehouse.test_replay.info_factory import InfoFactory
from tests.test_warehouse.test_replay.map_factory import MapFactory
from starcraft_data_orm.exceptions import ReplayExistsError

@pytest.mark.asyncio
async def test_process_existence():
    mock_replay = InfoFactory()

    mock_session = AsyncMock()
    mock_session.add = MagicMock()

    mock_execute_result = MagicMock()
    mock_execute_result.scalar.return_value = mock_replay
    mock_session.execute.return_value = mock_execute_result

    result = await info.process_existence(mock_replay, mock_session)

    assert result is not None
    mock_session.add.assert_not_called()

@pytest.mark.asyncio
async def test_process_info_does_not_exist():
    mock_map = MapFactory()
    mock_replay = InfoFactory(map=mock_map)

    mock_session = AsyncMock()
    mock_session.add = MagicMock()

    mock_execute_results = iter([
        MagicMock(scalar=MagicMock(return_value=None)),
        MagicMock(scalar=MagicMock(return_value=mock_map)),
    ])

    mock_session.execute.side_effect = lambda *args, **kwargs: next(mock_execute_results)

    await info.process(mock_replay, mock_session)

    mock_session.add.assert_called_once()

    added_replay = mock_session.add.call_args[0][0]
    assert added_replay.filehash == mock_replay.filehash
    assert added_replay.map_name == mock_replay.map.name

@pytest.mark.asyncio
async def test_process_info_does_exist():
    mock_map = MapFactory()
    mock_replay = InfoFactory(map=mock_map)

    mock_session = AsyncMock()
    mock_session.add = MagicMock()

    mock_execute_result = MagicMock()
    mock_execute_result.scalar.return_value = mock_replay
    mock_session.execute.return_value = mock_execute_result

    with pytest.raises(ReplayExistsError):
        await info.process(mock_replay, mock_session)

    mock_session.add.assert_not_called()
