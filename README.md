# kolava_node
Ventilation node

Ventilation valve control for ESP32 with MicroPython firmware.

Uses umqtt library (https://github.com/micropython/micropython-lib/tree/master/umqtt.simple)

1. Flash micropython firmware to your ESP32 (http://micropython.org/)
2. Rename settings-example.json to settings.json and modify at least wifi and mqtt server settings.
3. Upload files to ESP32 with adafruit-ampy (https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy)


## Implemented MQTT messages

**From node ->**
- kolava/node_online (client_name)
- kolava/client_name/valve_position (0-100)
- kolava/client_name/light_status (True/False)

**To node <-**
- kolava/clinet_name/blink_led ()
- kolava/client_name/set_valve (0-100)