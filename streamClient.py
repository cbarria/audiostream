#!/usr/bin/env python

import pyaudio
import socket
import sys
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
BUFFER_DURATION = 5  # Adjust this value as needed

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], 4444))
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    audio_buffer = b''  # Initialize an empty byte buffer

    try:
        while True:
            data = s.recv(CHUNK)  # Receive audio data
            audio_buffer += data  # Append received data to the buffer

            # Check if the buffer is filled with enough data for playback
            if len(audio_buffer) >= int(RATE * BUFFER_DURATION):
                stream.write(audio_buffer[:CHUNK])  # Play the first chunk of buffered data
                audio_buffer = audio_buffer[CHUNK:]  # Remove the played data from the buffer

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Stopping...")
    finally:
        print('Shutting down')
        s.close()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    main()
