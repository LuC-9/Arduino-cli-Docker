FROM python:3.7-slim
# FROM ubuntu
RUN apt-get update && apt-get install -y curl git # python3 python3-pip python-is-python3
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=/usr/bin sh
ADD config/arduino-cli.yaml /root/.arduino15/arduino-cli.yaml
RUN arduino-cli core install esp32:esp32
RUN pip install --no-cache-dir pyyaml
RUN pip install pyserial
RUN arduino-cli core install esp32:esp32 --config-file .arduino-cli.yaml
RUN arduino-cli core update-index
COPY compile.py /usr/src/app/
COPY init.sh /usr/src/app/
RUN chmod +x /usr/src/app/init.sh
WORKDIR /usr/src/sketch

# ENTRYPOINT ["/usr/src/app/init.sh"]
# CMD [ "sh", "/usr/src/app/init.sh" ]
