import os
from keras.models import load_model
import tensorflow as tf
import numpy as np
from vggish_input import waveform_to_examples
import ubicoustics
import pyaudio
from pathlib import Path
import time
import wget
import facade

# Variables
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = RATE
MICROPHONES_DESCRIPTION = []
FPS = 60.0

###########################
# Check Microphone
###########################
print("=====")
print("1 / 2: Checking Microphones... ")
print("=====")

import microphones
desc, mics, indices = microphones.list_microphones()
if (len(mics) == 0):
    print("Error: No microphone found.")
    exit()

#############
# Read microphone selection
#############
MICROPHONE_INDEX = indices[0]
try:
    MICROPHONE_INDEX = int(os.environ['MICROPHONE_INDEX'])
except:
    print("Invalid microphone")
    exit()

# Find description that matches the mic index
mic_desc = ""
for k in range(len(indices)):
    i = indices[k]
    if (i==MICROPHONE_INDEX):
        mic_desc = mics[k]
print("Using mic: %s" % mic_desc)

###########################
# Download model, if it doesn't exist
###########################
MODEL_URL = "https://www.dropbox.com/s/cq1d7uqg0l28211/example_model.hdf5?dl=1"
MODEL_PATH = "models/example_model.hdf5"
print("=====")
print("2 / 2: Checking model... ")
print("=====")
model_filename = "models/example_model.hdf5"
ubicoustics_model = Path(model_filename)
if (not ubicoustics_model.is_file()):
    print("Downloading example_model.hdf5 [867MB]: ")
    wget.download(MODEL_URL,MODEL_PATH)

##############################
# Load Deep Learning Model
##############################
print("Using deep learning model: %s" % (model_filename))
model = load_model(model_filename)
graph = tf.get_default_graph()

context_label = os.environ.get("CONTEXT", "everything")
context = eval(f"ubicoustics.{context_label}")
print("Using context:", context_label)

label = dict()
for k in range(len(context)):
    label[k] = context[k]

##############################
# Setup Audio Callback
##############################
def audio_samples(in_data, frame_count, time_info, status_flags):
    global graph
    np_wav = np.fromstring(in_data, dtype=np.int16) / 32768.0 # Convert to [-1.0, +1.0]
    x = waveform_to_examples(np_wav, RATE)
    predictions = []
    with graph.as_default():
        if x.shape[0] != 0:
            x = x.reshape(len(x), 96, 64, 1)
            pred = model.predict(x)
            predictions.append(pred)

        for prediction in predictions:
            m = np.argmax(prediction[0])

            if (m < len(label)):
                p = label[m]
                facade.state.update(label=label[m], certainty=prediction[0,m])
                n_items = prediction.shape[1]
            else:
                print("KeyError: %s" % m)

    return (in_data, pyaudio.paContinue)

##############################
# Launch Application
##############################
while(1):
    ##############################
    # Setup Audio
    ##############################
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=audio_samples, input_device_index=MICROPHONE_INDEX)

    ##############################
    # Start Non-Blocking Stream
    ##############################
    print("# Live Prediction Using Microphone: %s" % (mic_desc))
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)
