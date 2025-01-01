import logging
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_automation(hass):
    """Set up the Lamp Energy automation."""

    async def check_lamp_power(event=None):
        """Check lamps without power."""
        lamps_without_power = []

        for entity_id, state in hass.states.async_all("light"):
            if "fs" in state.attributes.get("friendly_name", "").lower():
                brightness = state.attributes.get("brightness", 0)
                if brightness == 0:
                    lamps_without_power.append(state.attributes.get("friendly_name"))

        if lamps_without_power:
            hass.states.async_set("sensor.lamps_without_power", ", ".join(lamps_without_power))
            _LOGGER.info(f"Lamps without power: {lamps_without_power}")
        else:
            hass.states.async_set("sensor.lamps_without_power", "None")

    async_track_time_interval(hass, check_lamp_power, SCAN_INTERVAL)