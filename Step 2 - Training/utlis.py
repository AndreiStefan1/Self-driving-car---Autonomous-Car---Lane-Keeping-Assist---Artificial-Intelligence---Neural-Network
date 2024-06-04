import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import cv2

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Input
from tensorflow.keras.optimizers import Adam

import matplotlib.image as mpimg
from imgaug import augmenters as iaa

import random

#### STEP 1 - INITIALIZE DATA
def getName(filePath):
    if isinstance(filePath, str):  # Check if filePath is a string
        myImagePathL = filePath.replace("\\", "/").split('/')[-2:]
        folder_name = myImagePathL[0]  # Extract the folder name dynamically
        myImagePath = os.path.join(folder_name, myImagePathL[1])
        return myImagePath
    else:
        return None  # Return None for non-string values


def importDataInfo(path):
    columns = ['Center', 'Steering']
    data = pd.DataFrame()
    for file_name in os.listdir(path):
        if file_name.endswith('.csv'):
            data_new = pd.read_csv(os.path.join(path, file_name), names=columns)
            print(f'File: {file_name}, Rows: {data_new.shape[0]}')
            data_new['Center'] = data_new['Center'].apply(getName)
            # Remove rows with None values in 'Center'
            data_new.dropna(subset=['Center'], inplace=True)
            data = pd.concat([data, data_new], ignore_index=True)
    print('Total Images Imported:', data.shape[0])
    return data

#### STEP 2 - VISUALIZE AND BALANCE DATA
def balanceData(data, display=True):
    nBin = 30
    samplesPerBin = 100
    hist, bins = np.histogram(data['Steering'], nBin)
    print('hist=', hist)
    if display:
        center = (bins[:-1] + bins[1:]) / 2
        plt.bar(center, hist, width=3)
        plt.plot((np.min(data['Steering']), np.max(data['Steering'])), (samplesPerBin, samplesPerBin))
        plt.title('Data Visualization')
        plt.xlabel('Steering Angle')
        plt.ylabel('No of Samples')
        # Set custom x-axis limits
        plt.xlim(-100, 100)
        plt.show()
    removeindexList = []
    for j in range(nBin):
        binDataList = []
        for i in range(len(data['Steering'])):
            if data['Steering'][i] >= bins[j] and data['Steering'][i] <= bins[j + 1]:
                binDataList.append(i)
        binDataList = shuffle(binDataList)
        binDataList = binDataList[samplesPerBin:]
        removeindexList.extend(binDataList)

    print('Removed Images:', len(removeindexList))
    data.drop(data.index[removeindexList], inplace=True)
    print('Remaining Images:', len(data))
    if display:
        hist, _ = np.histogram(data['Steering'], (nBin))
        plt.bar(center, hist, width=3)
        plt.plot((np.min(data['Steering']), np.max(data['Steering'])), (samplesPerBin, samplesPerBin))
        plt.title('Balanced Data')
        plt.xlabel('Steering Angle')
        plt.ylabel('No of Samples')
        # Set custom x-axis limits
        plt.xlim(-100, 100)
        plt.show()
    return data

#### STEP 3 - PREPARE FOR PROCESSING
def loadData(path, data):
    imagesPath = []
    steering = []
    for i in range(len(data)):
        indexed_data = data.iloc[i]
        # Construct the full image path by concatenating the base directory path with the relative path from the CSV file
        imagePath = os.path.join(path, indexed_data['Center'])
        imagesPath.append(imagePath)
        steering.append(float(indexed_data['Steering']))
    imagesPath = np.asarray(imagesPath)
    steering = np.asarray(steering)
    return imagesPath, steering

#### STEP 5 - AUGMENT DATA
def augmentImage(imgPath, steering):
    img = mpimg.imread(imgPath)
    if np.random.rand() < 0.5:
        pan = iaa.Affine(translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)})
        img = pan.augment_image(img)
    if np.random.rand() < 0.5:
        zoom = iaa.Affine(scale=(1, 1.2))
        img = zoom.augment_image(img)
    if np.random.rand() < 0.5:
        brightness = iaa.Multiply((0.5, 1.2))
        img = brightness.augment_image(img)
    if np.random.rand() < 0.5:
        img = cv2.flip(img, 1)
        steering = -steering
    return img, steering

#### STEP 6 - PREPROCESS
def preProcess(img):
    img = img[54:120, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img

#### STEP 7 - CREATE MODEL
def createModel():
    input_shape = (66, 200, 3)
    model = Sequential()

    model.add(Conv2D(24, (5, 5), (2, 2), input_shape=input_shape, activation='elu'))
    model.add(Conv2D(36, (5, 5), (2, 2), activation='elu'))
    model.add(Conv2D(48, (5, 5), (2, 2), activation='elu'))
    model.add(Conv2D(64, (3, 3), activation='elu'))
    model.add(Conv2D(64, (3, 3), activation='elu'))

    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    model.add(Dense(1))

    optimizer = Adam(learning_rate=0.0001)
    model.compile(optimizer=optimizer, loss='mse')

    return model

#### STEP 8 - TRAINING
def dataGen(imagesPath, steeringList, batchSize, trainFlag):
    while True:
        imgBatch = []
        steeringBatch = []

        for i in range(batchSize):
            index = random.randint(0, len(imagesPath) - 1)
            if trainFlag:
                img, steering = augmentImage(imagesPath[index], steeringList[index])
            else:
                img = mpimg.imread(imagesPath[index])
                steering = steeringList[index]
            img = preProcess(img)
            imgBatch.append(img)
            steeringBatch.append(steering)
        yield (np.asarray(imgBatch), np.asarray(steeringBatch))

