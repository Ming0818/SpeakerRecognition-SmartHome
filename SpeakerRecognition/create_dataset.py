import os, sys
dir = "Dataset"
speakers = os.listdir(dir)

num = 0
f_dataset = open('dataset.txt', 'w')
#f_synset = open("Speaker_synset.txt","w")
for speaker in speakers:
    print speaker
    if speaker == ".DS_Store":
        continue
    spectrograms = os.listdir(dir+"/"+speaker)

    for spectrogram in spectrograms:
        if spectrogram != ".DS_Store" and spectrogram.endswith(".png") :
            f_dataset.write(dir+"/"+speaker+"/"+spectrogram +" "+str(num)+"\n")
    num+=1
            