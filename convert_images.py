import os
import cv2

images_path = os.path.join('data/VOC2007', 'JPEGImages')
ext = "jpg"
for root, dirs, files in os.walk(images_path):
    for filename in files:
        if filename.endswith(".jpeg"):
            image = cv2.imread(os.path.join(root, filename))
            new_fname = "{}.{}".format(os.path.splitext(filename)[0], ext)
            small_fname = os.path.join(root, new_fname)
            cv2.imwrite(small_fname, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
