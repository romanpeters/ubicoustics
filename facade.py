import os
import paho.mqtt.client as mqtt
import ubicoustics

THRESHOLD = os.environ.get('THRESHOLD', 0.97)
CYCLE_LENGTH = os.environ.get('CYCLE_LENGTH', 3)  # number of consecutive cycles a sound needs to be heard before the state changes
SUSTAIN = os.environ.get('SUSTAIN', 3)  # number of cycles to keep the state after it has been detected
MQTT_HOST = os.environ['MQTT_HOST']
MQTT_PORT = int(os.environ['MQTT_PORT'])
MQTT_TOPIC = os.environ.get('MQTT_TOPIC', "ubicoustics")

client = mqtt.Client()
client.connect(MQTT_HOST, MQTT_PORT)


class State(object):
    """Represents the context that is being predicted"""
    def __init__(self):
        self.certainty: float = float()
        self.label: str = str()
        self.previous: tuple = tuple()
        self.cycle: int = 0  # consecutive cycles a sound is predicted
        self.sustain: int = 0 # consecutive cycles a different sound is predicted
        self.not_recognized: int = 0
        self.clear: bool = True  # indicates there's no current prediction

    def human_label(self) -> str:
        """Converts label to pretty label"""
        return ubicoustics.to_human_labels[self.label]

    def update(self, label, certainty):
        """Updates state if needed"""
        if certainty >= THRESHOLD:
            # sound recognised
            self.previous = (self.label, self.certainty)
            self.label = label
            self.certainty = certainty
        else:
            # sound not recognised
            self.sustain += 1
            if self.sustain >= SUSTAIN:
                self.reset()
            return

        if self.previous[0] == self.label:
            self.cycle += 1
        else:
            if self.cycle >= CYCLE_LENGTH:
                self.reset()
            self.cycle = 1

        if self.cycle == CYCLE_LENGTH:  # if reached a certain number of consecutive cycles
            self.clear = False
            self.sustain = 0
            state.show()  # print prediction
            send_state(state=self)  # MQTT

        if self.sustain >= SUSTAIN:
            self.reset()

    def reset(self):
        """Clears the current state"""
        if not self.clear:
            self.cycle = 0
            self.clear = True
            clear_state()  # MQTT

    def show(self):
        """Prints the current state"""
        print(f"Prediction: {self.human_label()}")


def send_state(state: State):
    print("[MQTT] Updating state")
    client.publish(f"{MQTT_TOPIC}/state", state.human_label())

def clear_state():
    print("[MQTT] Clearing state")
    client.publish(f"{MQTT_TOPIC}/state", "")

state = State()
