# SpeakerRecognition-SmartHome
This project is an attempt to provide secure and natural vway to interact with your smart home devices by adding Speaker Recognition system on top of Speech Recognition. This system provides voice biometric as a security layer which recognize the speaker from their voice commands. 

Both Speaker Recognition and Speech Recognition is implemented using Deep Learning Convolutional neural network. 

## Project Dependencies 
PyAudio <br />
SciPy <br />
Matplotlib <br />
PIL <br />

## Basic Model Training steps 
1.) Recorded the audio wave files using PyAudio and generated the Spectrogram images from audio wave files using matplotlib specgram. <br />
2.) Created a dataset text file of all the generated spectrogram images. The format of the file is same as used in Caffe for generating LMDB i.e. "file location"[SPACE]"ID". <br />
3.) Randomly Shuffled and  divided the dataset into train, validation and test sets. <br />
4.) Generated the LMDB and binary proto mean files. <br />
5.) Training and fine tuning of the model. <br />


