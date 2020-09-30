FROM ubuntu:18.04

COPY . /app
WORKDIR /app


RUN apt-get update && apt-get -y install software-properties-common python3-pip && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.6 && \
    apt-get install -y portaudio19-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir -U -r requirements.txt && \
    pip3 install --global-option='build_ext' --global-option='-I/opt/local/include' --global-option='-L/opt/local/lib' pyaudio

CMD ["python3.6", "-u", "run.py"]
