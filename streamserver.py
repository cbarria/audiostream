#!/usr/bin/env python3

import pyaudio
import socket
import select

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

audio = pyaudio.PyAudio()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 4444))
serversocket.listen(5)

def main():

    def callback(in_data, frame_count, time_info, status):
        for s in read_list[1:]:
            s.send(in_data)
        return (None, pyaudio.paContinue)

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=callback)

    read_list = [serversocket]
    print("Grabando...")

    try:
        while True:
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is serversocket:
                    (clientsocket, address) = serversocket.accept()
                    read_list.append(clientsocket)
                    print("Conexión desde", address)
                else:
                    try:
                        data = s.recv(1024)
                        if not data:
                            # Cliente desconectado
                            print("Cliente desconectado:", s.getpeername())
                            read_list.remove(s)
                    except socket.error:
                        # Manejar error de socket (cliente desconectado)
                        print("Cliente desconectado:", s.getpeername())
                        read_list.remove(s)
  
    except KeyboardInterrupt:
        print("Interrupción de teclado recibida. Deteniendo...")
    finally:
        print("Grabación finalizada")
        serversocket.close()
        # Detener grabación
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    main()
