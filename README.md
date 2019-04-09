# kolava_node

Ventilation valve control node for ESP32 with MicroPython firmware.

## External libraries

aswitch https://github.com/peterhinch/micropython-async


## Install

1. Flash micropython firmware to your ESP32 (http://micropython.org/)
2. Modify at least wifi and mqtt server settings from settings-example.json
3. Upload files to ESP32 with adafruit-ampy by running put_files.sh (https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) 


## Implemented MQTT messages

**From node ->**
- kolava/node_online (client_name)
- kolava/client_name/valve_position (0-100)
- kolava/client_name/light_status (True/False)
- kolava/client_name/power_status (True/False)

**To node <-**
- kolava/client_name/blink_led ()
- kolava/client_name/set_valve (0-100)
- kolava/client_name/set_power (True/False)
- kolava/client_name/set_screen_row (string to be added at last row)
- kolava/client_name/set_screen_text (row 1;row 2;row 3;row 4)
