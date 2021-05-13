# Arduino CLI Docker



Dockerized [`arduino-cli`](https://github.com/arduino/arduino-cli) sketch 
compilation tool with per-project core and library dependencies support and with a feature to upload compiled binary to AMAZON S3.


## Getting Started

1.  Install [Docker Engine](https://docs.docker.com/install/) on your machine.

2.  Choose the Sketch Repository.

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

4.  Build the Dockerfile or use our image Bucket name Used for now is arduino-binaries-tattva-cloud (You can Specify your bucket name in compile.py comments are provided for your help)

5.  Run `sudo docker run -it -e GITHUB_REPOURL=https://github.com/XYZ(specify the url) -e AWS_ACCESS_KEY=(access key of S3) -e AWS_SECRET_KEY=(Secret key of S3) (DockerImageName) `.

6.  The compiled binary file will appear inside the specified bucket with the name sketch.bin.

7.  Here you go, you have successfully generated the binary of your sketch!
-*-
