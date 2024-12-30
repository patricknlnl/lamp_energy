import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.const import ENERGY_KILO_WATT_HOUR
import re

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup the Lamp Energy sensor."""
    async_add_entities([LampEnergySensor(hass)])

class LampEnergySensor(SensorEntity):
    """Representation of a Lamp Energy Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.hass = hass
        self._state = None
        self._attr_name = "Lamp Energy Consumption"
        self._attr_unit_of_measurement = ENERGY_KILO_WATT_HOUR
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        lamp_states = self.hass.states.all("light")
        excluded_lamps = (
            self.hass.states.get("input_text.excluded_lamps").state.split(",")
            if self.hass.states.get("input_text.excluded_lamps")
            else []
        )
        total_consumption = 0

        for lamp in lamp_states:
            if lamp.state != "on":
                continue

            brightness = float(lamp.attributes.get("brightness", 255))
            watt_search = re.findall(r"([1-9][0-9]?|100)(?=\s?[wW](?:att)?)", lamp.name)
            max_watt = float(watt_search[0]) if watt_search else 10

            if lamp.entity_id not in excluded_lamps:
                consumption = (brightness / 255) * max_watt
                total_consumption += consumption

        self._state = round(total_consumption / 1000, 3)