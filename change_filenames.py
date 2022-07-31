import os
import cv2
count = 0
anno_path = os.path.join('data/VOC2007', 'Annotations')
for root, dirs, files in os.walk(anno_path):
    for filename in files:
        oldext = os.path.splitext(filename)[1]
        os.rename(os.path.join(root, filename),os.path.join(root, str(count) + oldext))
        count += 1
