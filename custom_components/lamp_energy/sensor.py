import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import Entity
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

DOMAIN = "lamp_energy"
SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Lamp Energy sensor."""
    sensor = LampEnergySensor(hass)
    async_add_entities([sensor], True)

class LampEnergySensor(SensorEntity):
    """Representation of a Lamp Energy sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self._hass = hass
        self._state = 0.0
        self._unit_of_measurement = "kWh"

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Lamp Energy Consumption"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    async def async_update(self):
        """Update the sensor."""
        total_consumption = 0.0

        for entity_id, state in self._hass.states.async_all("light"):
            if state.state == "on":
                brightness = state.attributes.get("brightness", 255)
                watt_search = state.attributes.get("friendly_name", "").lower()
                max_watt = 10  # Default wattage if not specified
                if "w" in watt_search:
                    watt_search = watt_search.split("w")[0]
                    try:
                        max_watt = float(watt_search)
                    except ValueError:
                        pass

                consumption = (brightness / 255) * max_watt
                total_consumption += consumption

        self._state = round(total_consumption / 1000, 3)
        _LOGGER.info(f"Total lamp energy consumption: {self._state} kWh")