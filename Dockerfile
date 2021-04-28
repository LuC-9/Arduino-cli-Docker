FROM python:3.7-slim
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=/usr/bin sh
ADD config/arduino-cli.yaml /root/.arduino15/arduino-cli.yaml
RUN arduino-cli core install esp32:esp32
RUN pip install --no-cache-dir pyyaml
RUN pip install pyserial
RUN arduino-cli core install esp32:esp32 --config-file .arduino-cli.yaml
RUN arduino-cli core update-index
COPY compile.py /usr/src/app/
WORKDIR /usr/src/sketch
CMD [ "python", "-u", "/usr/src/app/compile.py" ]
