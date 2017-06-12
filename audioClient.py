import socket
import pyaudio
import wave
import getch

#record
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

HOST = '192.168.2.5'    # The remote host
PORT = 50007              # The same port as used by the server

def recordAudio():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((HOST, PORT))

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("*recording")

    frames = []

    for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        data  = stream.read(CHUNK)
        frames.append(data)
        soc.sendall(data)

    print("*done recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()
    soc.close()

    print("*closed")

print "Please enter your name to save the recordings with your name."
username = raw_input()
#print username

while True:
    print "Press 'r' for start recording your 2 second voice. \nPress 'q' for exit."
    char = getch.getch()
    if char== 'r':
        recordAudio()
    elif char == 'q':
        exit()