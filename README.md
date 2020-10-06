# Ubicoustics
Forked from https://github.com/FIGLAB/ubicoustics

Acoustic activity recognition to MQTT.

### Docker container configuration
```
git pull https://github.com/romanpeters/ubicoustics
cd ubicoustics
docker build . --tag ubicoustics:latest
docker-compose up
```
You'll see which microphones are available.
Edit the `MICROPHONE_INDEX` variable in `docker-compose.yml` to the one you want to use. 
You should also make sure you've specified your own MQTT broker, with `MQTT_HOST` and `MQTT_PORT`.  
Then, rerun docker-compose:
```
docker-compose up -d
```

### Home Assistant configuration
```
sensor:
  - platform: "mqtt"
    name: Ubicoustics
    state_topic: "ubicoustics/state"
```
