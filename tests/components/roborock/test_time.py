"""Test Roborock Time platform."""

from datetime import time
from unittest.mock import patch

import pytest
import roborock

from homeassistant.components.time import SERVICE_SET_VALUE
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from tests.common import MockConfigEntry


@pytest.fixture
def platforms() -> list[Platform]:
    """Fixture to set platforms used in the test."""
    return [Platform.TIME]


@pytest.mark.parametrize(
    ("entity_id"),
    [
        ("time.roborock_s7_maxv_do_not_disturb_begin"),
        ("time.roborock_s7_maxv_do_not_disturb_end"),
    ],
)
async def test_update_success(
    hass: HomeAssistant,
    bypass_api_fixture,
    setup_entry: MockConfigEntry,
    entity_id: str,
) -> None:
    """Test turning switch entities on and off."""
    # Ensure that the entity exist, as these test can pass even if there is no entity.
    assert hass.states.get(entity_id) is not None
    with patch(
        "homeassistant.components.roborock.coordinator.RoborockLocalClientV1._send_command"
    ) as mock_send_message:
        await hass.services.async_call(
            "time",
            SERVICE_SET_VALUE,
            service_data={"time": time(hour=1, minute=1)},
            blocking=True,
            target={"entity_id": entity_id},
        )
    assert mock_send_message.assert_called_once


@pytest.mark.parametrize(
    ("entity_id"),
    [
        ("time.roborock_s7_maxv_do_not_disturb_begin"),
    ],
)
async def test_update_failure(
    hass: HomeAssistant,
    bypass_api_fixture,
    setup_entry: MockConfigEntry,
    entity_id: str,
) -> None:
    """Test turning switch entities on and off."""
    # Ensure that the entity exist, as these test can pass even if there is no entity.
    assert hass.states.get(entity_id) is not None
    with (
        patch(
            "homeassistant.components.roborock.coordinator.RoborockLocalClientV1._send_command",
            side_effect=roborock.exceptions.RoborockTimeout,
        ) as mock_send_message,
        pytest.raises(HomeAssistantError, match="Failed to update Roborock options"),
    ):
        await hass.services.async_call(
            "time",
            SERVICE_SET_VALUE,
            service_data={"time": time(hour=1, minute=1)},
            blocking=True,
            target={"entity_id": entity_id},
        )
    assert mock_send_message.assert_called_once
