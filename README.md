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

### State labels
"Dog Barking", "Drill In-Use", "Hazard Alarm", "Phone Ringing", "Person Talking", "Vacuum In-Use", "Baby Crying", "Chopping", "Coughing", "Door In-Use", "Water Running", "Knocking", "Microwave In-Use", "Shaver In-Use", "Toothbrushing", "Blender In-Use", "Dishwasher In-Use", "Doorbel In-Use", "Toilet Flushing", "Hair Dryer In-Use", "Laughing", "Snoring", "Typing", "Hammering", "Car Honking", "Vehicle Running", "Saw In-Use", "Cat Meowing", "Alarm Clock", "Utensils and Cutlery".

