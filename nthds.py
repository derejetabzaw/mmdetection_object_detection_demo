import os
from os.path import exists, join, basename, splitext

import sys
import time
import matplotlib
import matplotlib.pylab as plt
plt.rcParams["axes.grid"] = False
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import re

git_repo_url = 'https://github.com/derejetabzaw/mmdetection_object_detection_demo.git'


project_name = os.path.abspath(splitext(basename(git_repo_url))[0])
mmdetection_dir = os.path.join(project_name, "mmdetection")
anno_path = os.path.join(project_name, "data/VOC2007/Annotations")
voc_file = os.path.join(mmdetection_dir, "mmdet/datasets/voc.py")
sys.path.append(mmdetection_dir)




classes_names = []
xml_list = []

# if not exists(project_name):
#     !git clone -q --recurse-submodules --depth 1 $git_repo_url
#     print("Update mmdetection repo")
#     !cd {mmdetection_dir} && git checkout master && git pull
#     #dependencies
#     !pip install -q mmcv terminaltables
#     # #build
#     !cd {mmdetection_dir} && python setup.py install
#     !pip install -r {os.path.join(mmdetection_dir, "requirements.txt")}



MODELS_CONFIG = {
    'faster_rcnn_r50_fpn_1x': {
        'config_file': 'configs/pascal_voc/faster_rcnn_r50_fpn_1x_voc0712.py'
    },
    'cascade_rcnn_r50_fpn_1x': {
        'config_file': 'configs/cascade_rcnn_r50_fpn_1x.py',
    },
    'retinanet_r50_fpn_1x': {
        'config_file': 'configs/retinanet_r50_fpn_1x.py',
    }
}

selected_model = 'faster_rcnn_r50_fpn_1x'  

# Total training epochs.
total_epochs = 8

# Name of the config file.
config_file = MODELS_CONFIG[selected_model]['config_file']

for xml_file in glob.glob(anno_path + "/*.xml"):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for member in root.findall("object"):
        classes_names.append(member[0].text)
classes_names = list(set(classes_names))
classes_names.sort()
classes_names


fname = voc_file
with open(fname) as f:
    s = f.read()
    s = re.sub('CLASSES = \(.*?\)',
               'CLASSES = ({})'.format(", ".join(["\'{}\'".format(name) for name in classes_names])), s, flags=re.S)
with open(fname, 'w') as f:
    f.write(s)


config_fname = os.path.join(project_name, 'mmdetection', config_file)
assert os.path.isfile(config_fname), '`{}` not exist'.format(config_fname)


fname = config_fname
with open(fname) as f:
    s = f.read()
    work_dir = re.findall(r"work_dir = \'(.*?)\'", s)
    # Update `num_classes` including `background` class.
    s = re.sub('num_classes=.*?,',
               'num_classes={},'.format(len(classes_names) + 1), s)
    s = re.sub('ann_file=.*?\],',
               "ann_file=data_root + 'VOC2007/ImageSets/Main/trainval.txt',", s, flags=re.S)
    s = re.sub('total_epochs = \d+',
               'total_epochs = {} #'.format(total_epochs), s)
    if "CocoDataset" in s:
        s = re.sub("dataset_type = 'CocoDataset'",
                   "dataset_type = 'VOCDataset'", s)
        s = re.sub("data_root = 'data/coco/'",
                   "data_root = 'data/VOCdevkit/'", s)
        s = re.sub("annotations/instances_train2017.json",
                   "VOC2007/ImageSets/Main/trainval.txt", s)
        s = re.sub("annotations/instances_val2017.json",
                   "VOC2007/ImageSets/Main/test.txt", s)
        s = re.sub("annotations/instances_val2017.json",
                   "VOC2007/ImageSets/Main/test.txt", s)
        s = re.sub("train2017", "VOC2007", s)
        s = re.sub("val2017", "VOC2007", s)
    else:
        s = re.sub('img_prefix=.*?\],',
                   "img_prefix=data_root + 'VOC2007/',".format(total_epochs), s)
with open(fname, 'w') as f:
    f.write(s)


# python tools/train.py {config_fname}