
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
        try:
            # Retrieve all lights in the system
            lampen = [
                entity for entity in self.hass.states.async_all()
                if entity.domain == 'light' and entity.state == 'on'
            ]

            # Retrieve excluded lights
            zonder_stroom_state = self.hass.states.get('input_text.lampen_zonder_stroom')
            zonder_stroom = (
                map(str.strip, zonder_stroom_state.state.split(',')) if zonder_stroom_state else []
            )

            totaal_verbruik = 0

            for lamp in lampen:
                lamp_entity = lamp.entity_id
                brightness = lamp.attributes.get('brightness', 255)  # Default to 255 if not specified
                watt_search = re.findall(r'([1-9][0-9]?|100)(?=\s?[wW](?:att)?)', lamp.name)
                max_watt = float(watt_search[0]) if watt_search else 10

                if lamp_entity not in zonder_stroom:
                    verbruik = (float(brightness) / 255) * max_watt
                    totaal_verbruik += verbruik

            # Convert to kWh and round to 3 decimals
            self._state = round(totaal_verbruik / 1000, 3)
        except Exception as e:
            _LOGGER.error("Error updating Lamp Energy sensor: %s", e)
