#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 12:48:56 2024

@author: orane
"""

import os
import pandas as pd
import numpy as np
import glob
import torch
import librosa
import torchaudio
import numpy as np
from sklearn.utils import shuffle
from keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from transformers import Wav2Vec2Processor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import itertools
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.regularizers import l1, l2, l1_l2
from sklearn.model_selection import train_test_split
from load_vectors import get_basename, load_vectors_csv, load_vectors_csv_files
import csv
from sklearn.metrics import classification_report
print(tf.__version__)
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)

def scheduler(epoch, lr):
    if epoch < 3:
        return lr
    else:
        return lr * tf.math.exp(-0.01)


model_name = "facebook/wav2vec2-large-xlsr-53-french"
tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)
processor = Wav2Vec2Processor.from_pretrained(model_name)
lst_femme_homme = ["femme", "homme"]


for sexe in lst_femme_homme:
    

    if sexe == "femme":

             checkpoint = ModelCheckpoint('../modeles/best_women_24loc.h5', monitor='val_accuracy',verbose=1,save_best_only=True, mode='max' )
             file_lst = glob.glob("femme/*/*.csv")
             x_train,y_train, train_filenames = load_vectors_csv_files(file_lst)
             x_train, x_test, y_train, y_test, train_filenames, test_filenames = train_test_split(x_train, y_train, train_filenames, test_size=0.2, random_state=42)
             nombre_jeunes = np.sum(y_train == 0)
             nombre_vieux = np.sum(y_train == 1)  

             x_train, y_train = shuffle(x_train, y_train)
                
             feature_vector_lenght = 1024
             x_train = x_train.reshape(x_train.shape[0], 1024)
             x_test = x_test.reshape(x_test.shape[0], 1024)
             y_train_1_hot = to_categorical(y_train,num_classes=2)
             y_test_1_hot = to_categorical(y_test, num_classes=2)
             print(f"x_train : {x_train.shape}")
             print(f"x_test : {x_test.shape}")
             test_size = y_test.shape[0]
            
             model = Sequential()
             feature_vector_length = 1024
             input_shape=(feature_vector_length,)
             model.add(Dense(64, input_shape=input_shape, activation='relu',kernel_regularizer=l2(0.01)))
             model.add(Flatten())
             model.add(Dropout(0.2))
             model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.01)))
             model.add(Dense(2, activation='softmax'))
            
            
             lr_scheduler = LearningRateScheduler(scheduler)
             early_stopping = EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)
             reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=0.00001)
             checkpoint = ModelCheckpoint('../modeles/best_men.h5', monitor='val_accuracy',verbose=1,save_best_only=True, mode='max' )
             model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
             resume = model.fit(x_train, y_train_1_hot, epochs=500, batch_size=100, verbose=1, validation_data=(x_test,y_test_1_hot),callbacks=[early_stopping,lr_scheduler,checkpoint])
            
             predictions = model.predict(x_test)
             binary_predictions = np.argmax(predictions, axis=1)
             evaluation = model.evaluate(x_test, y_test_1_hot)
             print(f"Test Accuracy: {evaluation[1] * 100:.2f}%")
             print(f"Nb samples Old in train : {nombre_vieux}")
             print(f"Nb samples Young in trrain : {nombre_jeunes}")
    elif sexe == "homme":
            checkpoint = ModelCheckpoint('../modeles/best_men_24loc.h5', monitor='val_accuracy',verbose=1,save_best_only=True, mode='max' )
            file_lst = glob.glob("homme/*/*.csv")
            x_train,y_train, train_filenames = load_vectors_csv_files(file_lst)
            x_train, x_test, y_train, y_test, train_filenames, test_filenames = train_test_split(x_train, y_train, train_filenames, test_size=0.2, random_state=42)
            nombre_jeunes = np.sum(y_train == 0)
            nombre_vieux = np.sum(y_train == 1)  
            
            x_train, y_train = shuffle(x_train, y_train)
            
            feature_vector_lenght = 1024
            x_train = x_train.reshape(x_train.shape[0], 1024)
            x_test = x_test.reshape(x_test.shape[0], 1024)
            y_train_1_hot = to_categorical(y_train,num_classes=2)
            y_test_1_hot = to_categorical(y_test, num_classes=2)
            print(f"x_train : {x_train.shape}")
            print(f"x_test : {x_test.shape}")
            test_size = y_test.shape[0]
            
            model = Sequential()
            feature_vector_length = 1024
            input_shape=(feature_vector_length,)
            model.add(Dense(64, input_shape=input_shape, activation='relu',kernel_regularizer=l2(0.01)))
            model.add(Flatten())
            model.add(Dropout(0.2))
            model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.01)))
            model.add(Dense(2, activation='softmax'))
            
            
            lr_scheduler = LearningRateScheduler(scheduler)
            early_stopping = EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)
            reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=0.00001)
            checkpoint = ModelCheckpoint('../modeles/best_men.h5', monitor='val_accuracy',verbose=1,save_best_only=True, mode='max' )
            model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
            resume = model.fit(x_train, y_train_1_hot, epochs=500, batch_size=100, verbose=1, validation_data=(x_test,y_test_1_hot),callbacks=[early_stopping,lr_scheduler,checkpoint])
            
            predictions = model.predict(x_test)
            binary_predictions = np.argmax(predictions, axis=1)
            evaluation = model.evaluate(x_test, y_test_1_hot)
            print(f"Test Accuracy: {evaluation[1] * 100:.2f}%")
            print(f"Nb samples Old in train : {nombre_vieux}")
            print(f"Nb samples Young in trrain : {nombre_jeunes}")