import os
from tensorflow import keras
import pandas as pd
import numpy as np
import cv2
import tensorflow as tf
import shutil

from PIL import Image

from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from tensorflow import Graph


labels = ['Airplane', 'Automobile', 'Bird', 'Cat',
          'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']

img_height, img_width = 32, 32


def remove():
    if os.path.exists('/result/input.png'):
        os.remove('/result/input.png')


def home(request):
    temp = 'default.png'
    context = {'temp': temp}
    return render(request, 'index.html', context)
    # return HttpResponse({'a':1})


def predict(request):
    if(os.path.isdir('result')):
        print('removed')
        shutil.rmtree('result')
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save('result/input.png', fileObj)
    filePathName = fs.url(filePathName)
    print(filePathName)
    img = np.array(Image.open('result/input.png').resize((32, 32)))
    img = img[:, :, :3]
    print(img.shape)
    x = img/255
    x.resize(1,32,32,3)
    print(x.shape)
    model = keras.models.load_model('final_model/content/final_model/cnn')
    p = (model.predict(x))[0].tolist()
    l = max(p)
    index_ = p.index(l)
    predictedLabel = labels[index_]
    print(predictedLabel)
    context = {'filePathName': filePathName, 'predictedLabel': predictedLabel}    
    return render(request, 'index.html', context)
