# Lamp Energy Integration

This Home Assistant integration calculates the energy consumption of lamps and detects lamps without power.

## Features
- **Energy Consumption Sensor**: Tracks the total energy consumption of all lamps in kWh.
- **Lamps Without Power Sensor**: Detects lamps that are offline or without power.

## Installation
1. Add this repository to HACS:
   - Go to **HACS > Integrations > Custom Repositories**.
   - Add the URL: `https://github.com/patricknlnl/lamp_energy`.
2. Install the integration via HACS.
3. Restart Home Assistant.

## Usage
- The sensor `sensor.lamp_energy_consumption` will automatically be created.
- The sensor `sensor.lamps_without_power` will show lamps that are offline or without power.

## Support
For issues or feature requests, please open an issue on [GitHub](https://github.com/patricknlnl/lamp_energy/issues).