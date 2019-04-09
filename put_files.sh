#!/bin/bash

ampy -p /dev/tty.SLAB_USBtoUART run install.py
ampy -p /dev/tty.SLAB_USBtoUART put settings-example.json settings.json
ampy -p /dev/tty.SLAB_USBtoUART put lib/aswitch.py lib/aswitch.py
ampy -p /dev/tty.SLAB_USBtoUART put lib/ssd1306.py lib/ssd1306.py
ampy -p /dev/tty.SLAB_USBtoUART put boot.py
ampy -p /dev/tty.SLAB_USBtoUART put button_period.py
ampy -p /dev/tty.SLAB_USBtoUART put button.py
ampy -p /dev/tty.SLAB_USBtoUART put ldr.py
ampy -p /dev/tty.SLAB_USBtoUART put led.py
ampy -p /dev/tty.SLAB_USBtoUART put mqtt.py
ampy -p /dev/tty.SLAB_USBtoUART put oled.py
ampy -p /dev/tty.SLAB_USBtoUART put period.py
ampy -p /dev/tty.SLAB_USBtoUART put relay.py
ampy -p /dev/tty.SLAB_USBtoUART put servo.py
ampy -p /dev/tty.SLAB_USBtoUART put settings.py
ampy -p /dev/tty.SLAB_USBtoUART put switch.py
ampy -p /dev/tty.SLAB_USBtoUART put wifi.py
ampy -p /dev/tty.SLAB_USBtoUART put main.py