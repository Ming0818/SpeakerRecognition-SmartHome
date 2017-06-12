import random

with open("dataset.txt", "rb") as f:
    data = f.read().split('\n')

random.shuffle(data)

print "length of data"
print len(data)

train_data = data[:2000]
validation_data =data[2000:2500]
test_data = data[2500:]

f_train = open("train_set.txt","w")

for data in train_data:
    f_train.write(data + '\n')

f_validation = open("validation_set.txt","w")

for data in validation_data:
    f_validation.write(data + '\n')

f_test = open("test_set.txt","w")

for testdata in test_data:
    f_test.write(testdata + '\n')
