import skvideo.io
from skvideo.io import ffprobe
import os, sys, csv
import numpy as np
from os import listdir
from os.path import isfile, join, isdir, exists
from pprint import pprint
import pickle
import time

import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable

from PIL import Image

# Load Resnet-152 pre-trained model
resnet152 = models.resnet152(pretrained=True)
modules=list(resnet152.children())[:-1]
resnet152=nn.Sequential(*modules).cuda()
for p in resnet152.parameters():
    p.requires_grad = False



# Define image to tensor transformation (required for Resnet model)
img_size = 224
img_to_tensor = transforms.Compose([
    transforms.Resize(size=img_size),
    transforms.CenterCrop(size=(img_size,img_size)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

def get_img_feature(model, img_to_tensor, images):
    # Get features of images
    # images: (frame size, image_H, image_W)
    # return: (frame size, 2048)
    images_pillow = [Image.fromarray(image) for image in images]
    images_tensor = [img_to_tensor(img).unsqueeze(0) for img in images_pillow]
    t_img = Variable(torch.cat(images_tensor), volatile=True).cuda()

    embedding = model(t_img).view(-1, 2048)

    return embedding.data.cpu().numpy()

time_data_path = 'data/friendsnew.english.v4_gold_conll'
video_path = 'data/s08e01.avi'
output_scene_emb_path = 'data/f001.pickle'

time_list = []
f = open(time_data_path, 'r')
for line in f:
    if (len(line) > 3 and ('#begin' not in line) and ('#end' not in line)):
        items = line.strip().split()
        st_time = items[-4]
        en_time = items[-3]
        if (st_time != 'NOTIME' and en_time != 'NOTIME'):
            st_time = int(st_time)
            en_time = int(en_time)
            if (en_time - st_time >= 150 and en_time - st_time <= 10000):
                if (len(time_list) == 0 or (st_time != time_list[-1][0] or en_time != time_list[-1][1])):
                    time_list.append((st_time,en_time))
f.close()

print ('start...')
epi_sttime = int(time.time())
videodata = skvideo.io.vread(video_path)
elapsed = int(time.time()) - epi_sttime
print('video loaded', elapsed, 'sec elpased')

seg_list= []
index = 0
output_obj = []
for time_item in time_list:
    index += 1
    st = float(time_item[0])/1000
    nd = float(time_item[1])/1000

    st_frame = int(st*2997/125)#metadata['video']['@avg_frame_rate']))
    nd_frame = int(nd*2997/125)#metadata['video']['@avg_frame_rate']))

    seg_video = videodata[st_frame:nd_frame]
    if(st_frame >= nd_frame):
        print('something wrong with here')
        print (st,nd)
        print (st_frame, nd_frame)

    elapsed = int(time.time()) - epi_sttime
    if (index%10 == 0):
        print(index, 'units processed', elapsed, 'sec elpased')

    seg_video_feature = get_img_feature(resnet152, img_to_tensor, seg_video)
    scene_emb = np.mean(seg_video_feature, axis=0)

    output_obj.append({
        'st':time_item[0],
        'en':time_item[1],
        'vec':scene_emb
    })

    del seg_video
    del seg_video_feature

with open(output_scene_emb_path, 'wb') as handle:
    pickle.dump(output_obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

