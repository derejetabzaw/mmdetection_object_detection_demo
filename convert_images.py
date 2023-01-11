import os
import cv2
import argparse
from pathlib import Path


parser = argparse.ArgumentParser(description='Image Converter')
parser.add_argument('-i', "--curves_folder_path", type=Path)
args = parser.parse_args()
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
images_path = dir_path(args.curves_folder_path)
print (images_path)
# images_path = os.path.join('../tapes', '')
desired_ext = "png"
convert_ext = [".tif" , ".tiff"] 
for root, dirs, files in os.walk(images_path):
    for filename in files:
        if filename.endswith(tuple(convert_ext)):
            print ("filename:", filename)
            image = cv2.imread(os.path.join(root, filename))
            print ("Converting...")
            new_fname = "{}.{}".format(os.path.splitext(filename)[0], desired_ext)
            small_fname = os.path.join(root, new_fname)
            cv2.imwrite(small_fname, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            print ("Converted")
            print ("\n")
print ("Done!")