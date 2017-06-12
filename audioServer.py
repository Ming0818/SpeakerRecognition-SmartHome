import socket
import pyaudio
import wave
import time
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import os
import os.path
from scipy import signal
from PIL import Image, ImageChops
import serial
import subprocess

ser = serial.Serial('/dev/ttyACM0',9600)

ser.write('0')
ser.write('2')

plt.switch_backend('agg')


threshold = 0.5

commandsObj = {
    '0':"close",
    '1':"open",
    '2':"0",
    '3':"1"
}


caffe_root = '../'


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "server_output.wav"
WIDTH = 2

plt.switch_backend('agg')

#frames = []

HOST = '0.0.0.0'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

def recognizeUser(input_spectrogram):
    speaker_model = 'SpeakerRecognition_trainedModels/speakerRecognition_v1_24MB.caffemodel'
    print input_spectrogram
    
    deploy_file = "SpeakerRecognition/deploy.prototxt"
    
    binaryproto_file = "SpeakerRecognition/validation_256_gray_mean.binaryproto"
    
    synset_file = "SpeakerRecognition/Speaker_synset.txt"
    
    cmd=["build/examples/cpp_classification/classification.bin", deploy_file, speaker_model, binaryproto_file, synset_file, input_spectrogram]

    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    print "program output:", out
    print "err: "
    print err
    #print(cmd)
    
    results = out.split("\n")[1]
    #print results
    accuracy,name = results.split(" - ")
    print name, accuracy
    return name, accuracy

def recognizeCommand(input_spectrogram):
    speech_model = 'speechRecognition/SR__iter_3074.caffemodel'
#    print input_spectrogram
    
    deploy_file = "speechRecognition/speech_deploy.prototxt"
    
    binaryproto_file = "speechRecognition/train_gray_mean.binaryproto"
    
    synset_file = "speechRecognition/speech_synset.txt"
    
    cmd=["build/examples/cpp_classification/classification.bin",deploy_file, speech_model, binaryproto_file, synset_file, input_spectrogram]
    
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    print "program output:", out
    
    results = out.split("\n")[1]
    #print results
    accuracy,command = results.split(" - ")
    print command, accuracy
    return command, accuracy


def trim(imagename):
    im = Image.open(imagename)
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def getSpectrogram(audio):
    print audio
    ##----Reading the wav file---
    print "Generating Spectrogram."
    sample_rate, samples = wav.read(audio)
    print "---Sample_rate-----"
    print sample_rate
    
    print "samples"
    #print samples
    print samples.shape
    
    #---Generating the window and hop length----
    window = 20
    step = 10
    fft_length = int(0.001 * window * sample_rate)
    print fft_length
    hop_length = int(0.001 * step * sample_rate)
    print hop_length
    
    #---plotting and saving the spectrogram
    plt.axis("off")
    Pxx,freq,time,a = plt.specgram(samples,NFFT = fft_length,Fs = sample_rate,noverlap=hop_length,cmap='jet',detrend="none",mode="psd")
    imagename = audio.split(".")[0]+".png";
    print imagename
    plt.savefig(imagename,transparent=False)
    plt.clf()
    print "successfully saved the spectrogram."
    cropped_image = trim(imagename)
    cropped_image.save(imagename,"")

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((HOST, PORT))

while True:
    print("Socket is ready to recieve the data.")
    soc.listen(1)
    conn, addr = soc.accept()
    frames = []
    print 'Connected by', addr
    
    data = conn.recv(1024)

    i=1
    while data != '':
        data = conn.recv(1024)
    #    i=i+1
    #    print i
        frames.append(data)

    print("Data recieved")

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(WIDTH)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    if os.environ.get("LD_LIBRARY_PATH")==None:
        os.environ['LD_LIBRARY_PATH'] = "/usr/local/cuda/lib64"
    print("environment LD_LIBRARY_PATH AFTER:")
    print os.environ.get("LD_LIBRARY_PATH")

    filename16k = WAVE_OUTPUT_FILENAME.split(".")[0]+"_16kHz.wav"
    os.system("sox " + WAVE_OUTPUT_FILENAME + " -r 16000 " + filename16k)

    getSpectrogram(filename16k)

    spectrogram = filename16k.split(".")[0]+".png";
        
    print("spectrogram location:")
    print(spectrogram)

    username, accuracy = recognizeUser(spectrogram)

    if float(accuracy)>threshold:
        command, cmd_accuracy = recognizeCommand(spectrogram)
        cmd_number = command.split()[1][0]
        print("cmd_number:")
        print(cmd_number)
        print("IDENTIFIED SPEAKER: "+username.split(" ")[0][1:])
        speaker = username.split(" ")[0][1:]
        if speaker == "Mitul":
            ser.write(cmd_number)
        else:
            print("UNAUTHORIZED USER...")
    else:
        print("User not identified")


conn.close()
