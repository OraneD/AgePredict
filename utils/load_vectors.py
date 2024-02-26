#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 14:52:31 2024

@author: orane
"""
import pandas as pd
import glob
import csv
import numpy as np

def get_basename(directory):
    print(directory.split("/")[-1])
    return directory.split("/")[-1]

def load_vectors_csv(directories,layer):
    all_vectors = []
    all_labels = []
    all_filenames = []
    basenames = [get_basename(directory) for directory in directories]
    #csv_paths = [f"{directory}_{get_basename(directory)}_{layer}.csv" for directory in directories]
    csv_paths = [f"{directories[i]}/{basenames[i]}_{layer}.csv" for i in range(len(directories))]
    for csv_path in csv_paths:
        df = pd.read_csv(csv_path)
        
        vectors = df.iloc[:, 2:].to_numpy()
        labels = df['label'].to_numpy()
        filenames = df["filename"].to_list()
        
        all_vectors.append(vectors)
        all_labels.append(labels)
        all_filenames.extend(filenames)

    X = np.concatenate(all_vectors, axis=0)
    y = np.concatenate(all_labels, axis=0)
    
    return X, y, all_filenames

def load_vectors_csv_file(file_lst):
    all_vectors = []
    all_labels = []
    all_filenames = []
    for csv_path in file_lst:
        df = pd.read_csv(csv_path)
        
        vectors = df.iloc[:, 2:].to_numpy()
        labels = df['label'].to_numpy()
        filenames = df["filename"].to_list()
        
        all_vectors.append(vectors)
        all_labels.append(labels)
        all_filenames.extend(filenames)

    X = np.concatenate(all_vectors, axis=0)
    y = np.concatenate(all_labels, axis=0)
    
    return X, y, all_filenames

def load_vectors_csv_files(files):
    all_vectors = []
    all_labels = []
    all_filenames = []
    #csv_paths = [f"{directory}_{get_basename(directory)}_{layer}.csv" for directory in directories]

    for file in files:
        df = pd.read_csv(file)
        
        vectors = df.iloc[:, 2:].to_numpy()
        labels = df['label'].to_numpy()
        filenames = df["filename"].to_list()
        
        all_vectors.append(vectors)
        all_labels.append(labels)
        all_filenames.extend(filenames)

    X = np.concatenate(all_vectors, axis=0)
    y = np.concatenate(all_labels, axis=0)
    
    return X, y, all_filenames

def main():
    x_train,y_train, filename_train = load_vectors_csv(["../corpus_cross_val/femme/old/ESLO2_ENT_1015", "../corpus_cross_val/femme/old/ESLO2_ENT_1030", "../corpus_cross_val/femme/old/ESLO2_ENT_1069"], 2)
    print(x_train.shape)
    print(y_train.shape)


if __name__ == "__main__":
    main()