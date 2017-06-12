import pyaudio
import wave
import getch
#import matplotlib
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
#matplotlib.use('Agg')
import os.path
from PIL import Image, ImageChops

plt.switch_backend('agg')

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 128
RECORD_SECONDS = 2
#WAVE_OUTPUT_FILENAME = "file4.wav"
#FILE_COUNT = 0

def record(filename, filecount):
    
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK,input_device_index=10)
    print "recording..."

    frames = []
     
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "finished recording"
    stream.stop_stream()
    stream.close()
    audio.terminate()

    while os.path.isfile("recorded_wavfiles/"+filename):
        filecount+=1
        filename = username+str(filecount)+".wav"

    waveFile = wave.open("recorded_wavfiles/"+filename, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    
    filename16k = filename.split(".")[0]+"_16kHz.wav"
    #---Converting the 44100Hz to 16000Hz
    os.system("sox " + "recorded_wavfiles/"+filename + " -r 16000 " + "recorded_wavfiles/"+filename16k)

    getSpectrogram(filename16k)

def getSpectrogram(filename):
    ##----Reading the wav file---
    print "Generating Spectrogram."
    sample_rate, samples = wav.read("recorded_wavfiles/"+filename)
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
    imagename = filename.split(".")[0]+".png";
    print imagename
    plt.savefig("spectrograms/"+imagename,transparent=False,bbox_inches='tight')
    plt.clf()
    print "successfully saved the spectrogram."
    
    #---Removing the white border arounf the spectrogram.
    im = Image.open("spectrograms/"+imagename)
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)
        im.save("spectrograms/"+imagename)


filename = " "
filecount = 0
print "Please enter your name to save the recordings with your name."
username = raw_input()
#print username

while True:
    
    print "Press 'r' for start recording your 2 second voice. \nPress 'q' for exit."
    char = getch.getch()
    if char== 'r':
        filename = username+str(filecount)+".wav"
        record(filename,filecount)
        filecount += 1
    elif char == 'q':
        exit()



 
# stop Recording

