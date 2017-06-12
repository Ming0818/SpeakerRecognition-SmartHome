#from flask import Flask, jsonify, request, make_response
from flask import *
from flask_cors import CORS
import json 
import re
import datetime
import string
import os
import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageChops
import serial
import subprocess

# ser = serial.Serial('/dev/ttyACM0',9600)

plt.switch_backend('agg')

app = Flask(__name__,static_url_path='')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
threshold = 0.5

commandsObj = {
    '0':"close",
    '1':"open",
    '2':"0",
    '3':"1"
}


caffe_root = '../'

def trim(imagename):
    im = Image.open(imagename)
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def recognizeUser(input_spectrogram):
    speaker_model = 'SpeakerRecognition_trainedModels/speakerRecognition_v1_24MB.caffemodel'
    print input_spectrogram
#     input_spectrogram = "spectrograms/Nishank2_16kHz.png"
    cmd=[caffe_root+"build/examples/cpp_classification/classification.bin", caffe_root+"SpeakerRecognition_trainedModels/deploy.prototxt", caffe_root+speaker_model, caffe_root+"SpeakerRecognition_trainedModels/new_validation_256_gray_mean.binaryproto", caffe_root+"SpeakerRecognition_trainedModels/Speaker_synset.txt", caffe_root+input_spectrogram]
    #print("command: ")
    #print(cmd)
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    print "program output:", out
    print "err: "
    print err
    #print(cmd)
    
    results = out.split("\n")[1]
    print results
    accuracy,name = results.split(" - ")
    print name, accuracy
    return name, accuracy

def recognizeCommand(input_spectrogram):
    speech_model = 'speechRecognition/SR__iter_3074.caffemodel'
    print input_spectrogram
    
    deploy_file = "speechRecognition/speech_deploy.prototxt"
    
    binaryproto_file = "speechRecognition/train_gray_mean.binaryproto"
    
    synset_file = "speechRecognition/speech_synset.txt"
    
    cmd=[caffe_root+"build/examples/cpp_classification/classification.bin",caffe_root+deploy_file, caffe_root+speech_model, caffe_root+binaryproto_file, caffe_root+synset_file, caffe_root+input_spectrogram]
    
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    print "program output:", out
    
    results = out.split("\n")[1]
    print results
    accuracy,command = results.split(" - ")
    print command, accuracy
    return command, accuracy

def getSpectrogram(audioFiles):
    for audio in audioFiles:
        ##----Reading the wav file---
        print "Generating Spectrogram."
        sample_rate, samples = wav.read(audio)

        # samples = samples[:,0]
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
        im5 = cropped_image.resize((615, 480), Image.ANTIALIAS)
        im5.save(imagename,"")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save/wavfile', methods=['POST'])
def savewavfile():
    print("Saving audio file")
    f = request.files['file']
    app.logger.debug(request.files['file'].filename)
    f.save("testAudio.wav")
    filename ="testAudio.wav"
    filename16k = filename.split(".")[0]+"_16kHz.wav"
    os.system("sox " + filename + " -r 16000 " + filename16k)
    getSpectrogram([filename16k])
    
    # spectrogram = "spectrograms/"+ filename16k.split(".")[0]+".png";
    
    # print("spectrogram location:")
    # print(spectrogram)
    
    # username, accuracy = recognizeUser(spectrogram)
    
    # if float(accuracy)>threshold:
    #     command, cmd_accuracy = recognizeCommand(spectrogram)
    #     cmd_number = command.split()[1][0]
    #     print("cmd_number:")
    #     print(cmd_number)
	# print("speaker: "+username.split(" ")[0][1:])
	# speaker = username.split(" ")[0][1:]
	# if speaker == "Mitul":
    #        ser.write(cmd_number)
	# else:
	#    print("Unauthorized User...")
    # else:
	# print("User not identified")
    resp = make_response(json.dumps(["true", 0]))
    return resp


if __name__ == '__main__':
    print("environment LD_LIBRARY_PATH:")
    print os.environ.get("LD_LIBRARY_PATH")
    if os.environ.get("LD_LIBRARY_PATH")==None:
	os.environ['LD_LIBRARY_PATH'] = "/usr/local/cuda/lib64"
    print("environment LD_LIBRARY_PATH AFTER:")
    print os.environ.get("LD_LIBRARY_PATH")
    app.run(debug=True,host='0.0.0.0')
