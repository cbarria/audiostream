# Audio Streaming

This is a simple project to stream audio from a Raspberry PI USB Microphone into anywhere on your network.

NOTE: pyaudio library for aarch64 is on the EPEL from fedora https://dl.fedoraproject.org/pub/epel/ this was tested on a Raspberry Pi 4B with almalinux 9.2 for aarch64 


## Installation steps

1. Clone this project:

   ```
   git clone git@github.com:cbarria/audiostream.git
   cd audio-stream
   ```

2. Build the application:

   ```
   make build
   ```

3. Install (will require sudo):
  
   ```
   sudo make install
   ```

4. Start the service:

   ```
   sudo systemctl start audioserver.service
   ```
   
5. Make an RPM:

   ```
   make package
   ```
   
6. Clean
   
   ```
   make clean
   ```
   
## Use

The server will listen for connections so use the client to connect to a server:

   ```
   streamclient.py (SERVER_IP_ADDRESS)
   ```
