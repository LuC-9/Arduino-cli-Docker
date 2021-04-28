# Arduino CLI Compile

[![https://img.shields.io/docker/pulls/macroyau/arduino-cli-compile](https://img.shields.io/docker/pulls/macroyau/arduino-cli-compile)](https://hub.docker.com/r/macroyau/arduino-cli-compile)

Dockerized [`arduino-cli`](https://github.com/arduino/arduino-cli) sketch 
compilation tool with per-project core and library dependencies support.


## Getting Started

1.  Install [Docker Engine](https://docs.docker.com/install/) on your machine.

2.  Go to your Arduino sketch folder which contains the main `.ino` file.

3.  Create `project.yaml` with the following content:
```yaml
# Filename of the project's main sketch
sketch: EspTest.ino
# Sketch version (optional; appended to filename of compiled binary file)
version: 1.0.0

# Compilation target
target:
  
  # Arduino core name
  core: esp32:esp32      # Installs the latest version; or
  # Arduino board FQBN string (obtained from `arduino-cli board list`)
  board: esp32:esp32:esp32
  # Additional board manager URL for core installation (optional)
  url: https://dl.espressif.com/dl/package_esp32_index.json

# Libraries to be included for compilation
libraries:
  - ArduinoJson
  - EspMQTTClient
  - Adafruit MPU6050
  - Adafruit SSD1306
  - MPU6050_tockn
  - PubSubClient
  - WiFi
  
  # - Arduino Low Power==1.2.1  # Installs v1.2.1
```

4.  Download `arduino-cli-compile` to a `PATH` directory and make it executable.

5.  Run `arduino-cli-compile path/to/sketch/folder`.

6.  The compiled binary file will appear inside the current sketch folder with the name sketch.ino.bin.



    ```bash
    arduino-cli upload -p /dev/ttyUSB0 -b esp32:esp32:esp32 -i path/to/bin/file
    ```

7.  Watch your board blinking!
