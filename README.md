# SpeakerRecognition-SmartHome
This project is an attempt to provide secure and natural vway to interact with your smart home devices by adding Speaker Recognition system on top of Speech Recognition. This system provides voice biometric as a security layer which recognize the speaker from their voice commands. 

Both Speaker Recognition and Speech Recognition is implemented using Deep Learning Convolutional neural network. 

## Python Project Dependencies 
PyAudio <br />
SciPy <br />
Matplotlib <br />
PIL <br />

## Deep Learning Platform
Caffe

## Basic Model Training steps 
1.) Recorded the audio wave files using PyAudio and generated the Spectrogram images of audio wave files using matplotlib specgram. <br />
2.) Created the dataset text file of all the generated spectrogram images. Format of the file is same as used in Caffe for generating LMDB i.e. ["file location"][SPACE]["ID"]. <br />
3.) Randomly Shuffled the dataset and divided it into train, validation and test sets. <br />
4.) Generated the LMDB and binary proto mean files. <br />
5.) Trained and fine tunned the model. <br />

## Inference
For inference, I have used Jetson Tx1 GPU embedded board. Both speaker recognition and speech recognition trained model is deployed on the board. IoT devices are connected to Jetson board via Arduino Uno Board. 

For more details, result and demo videos please refer to Presentation.ppt

## Python Files Description
voiceRecorder.py -- Records the voice commands in wave format, convert 44Khz to 16Khz audio wave and generates the spectrogram image. <br />

audioClient.py -- This program is the client side of the end-to-end pipeline which records the audio voice commmand and sends it frame by frame to the server program which is running on Jetson board using socket programming.

audioServer.py -- Running on Jetson Tx1 board, performs all the heavy lifting. This program creates the wav file, generates the spectrogram image, run both the speech and speaker recognition trained model and controls the smart home devices. 





