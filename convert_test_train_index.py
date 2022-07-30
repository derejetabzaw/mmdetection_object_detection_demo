import os 
from sklearn.model_selection import train_test_split
images_path = os.path.join('dataset', 'JPEGImages')
text_path = os.path.join('dataset', 'ImageSets/Main')
test_path = os.path.join(os.getcwd(),os.path.join(text_path, 'test.txt').replace("\\","/")).replace("\\","/")
train_path =  os.path.join(os.getcwd(),os.path.join(text_path, 'trainval.txt').replace("\\","/")).replace("\\","/")
files_list = []
for root, dirs, files in os.walk(images_path):
    for filename in files:
        files_list.append(os.path.splitext(filename)[0])

training_data, testing_data = train_test_split(files_list, test_size=0.2, random_state=25)




with open(test_path, 'w') as f:
    for element in testing_data:
        f.write(element + ",")
with open(train_path, 'w') as f:
    for element in testing_data:
        f.write(element + ",")

