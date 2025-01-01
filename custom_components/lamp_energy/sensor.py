
import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)

DOMAIN = "lamp_energy"
SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Lamp Energy sensor."""
    async_add_entities([LampEnergySensor(hass)], True)

class LampEnergySensor(SensorEntity):
    """Representation of a Lamp Energy sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self._hass = hass
        self._state = 0.0
        self._attr_name = "Lamp Energy Consumption"
        self._attr_unit_of_measurement = "kWh"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Update the sensor."""
        total_consumption = 0.0

        for entity_id, state in self._hass.states.async_all("light"):
            if state.state == "on":
                brightness = state.attributes.get("brightness", 255)
                watt_search = state.attributes.get("friendly_name", "").lower()
                max_watt = 10  # Default wattage if not specified

                if "w" in watt_search:
                    try:
                        max_watt = float(watt_search.split("w")[0])
                    except ValueError:
                        _LOGGER.warning(f"Could not parse wattage from {watt_search}")

                consumption = (brightness / 255) * max_watt
                total_consumption += consumption

        self._state = round(total_consumption / 1000, 3)
        _LOGGER.debug(f"Updated lamp energy consumption: {self._state} kWh")
