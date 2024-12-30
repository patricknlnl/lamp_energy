
import logging
import re
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup the Lampen Verbruik sensor and Lampen Zonder Stroom sensor."""
    async_add_entities([LampenVerbruikSensor(hass), LampenZonderStroomSensor(hass)])

class LampenVerbruikSensor(SensorEntity):
    """Sensor to calculate total lamp energy consumption."""

    def __init__(self, hass):
        self.hass = hass
        self._state = 0.0
        self._attr_name = "Lamp Verbruik"
        self._attr_unit_of_measurement = "Watt"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Update the state of the sensor."""
        lampen = [
            entity for entity in self.hass.states.async_all()
            if entity.domain == "light" and entity.state == "on"
        ]
        zonder_stroom = self.hass.states.get("input_text.lampen_zonder_stroom")
        zonder_stroom_list = (
            zonder_stroom.state.split(",") if zonder_stroom else []
        )

        totaal_verbruik = 0.0

        for lamp in lampen:
            lamp_entity = lamp.entity_id
            if lamp_entity in zonder_stroom_list:
                verbruik = 0
            else:
                brightness = lamp.attributes.get("brightness", 255)
                watt_search = re.findall(r"([1-9][0-9]?|100)(?=\\s?[wW](?:att)?)", lamp.name)
                max_watt = float(watt_search[0]) if watt_search else 10
                verbruik = (brightness / 255) * max_watt

            totaal_verbruik += verbruik

        self._state = round(totaal_verbruik, 2)


class LampenZonderStroomSensor(SensorEntity):
    """Sensor to track lights without power."""

    def __init__(self, hass):
        self.hass = hass
        self._state = ""
        self._attr_name = "Lampen Zonder Stroom"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Update the state of the sensor."""
        fs_lampen = [
            entity.entity_id for entity in self.hass.states.async_all()
            if "FS" in entity.attributes.get("friendly_name", "") and entity.domain == "light"
        ]

        zonder_stroom = []

        for lamp_entity in fs_lampen:
            lamp_state = self.hass.states.get(lamp_entity)
            if not lamp_state:
                continue

            current_brightness = lamp_state.attributes.get("brightness", 0)
            test_brightness = current_brightness + 1 if current_brightness < 254 else 254

            # Simulate brightness adjustment and validate
            adjusted_brightness = test_brightness  # Simulate success for now

            if adjusted_brightness != test_brightness:
                zonder_stroom.append(lamp_entity)

        self._state = ", ".join(zonder_stroom)
    