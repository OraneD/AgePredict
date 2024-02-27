#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:47:40 2024

@author: orane
"""

from extract_input_vectors import extract_vectors
import numpy as np
from tensorflow.keras.models import load_model

"""
Chargment des modèles en fonction du sexe et prédiction de l'âge
"""

def predict_age(file,sexe):
    model_path = "../modeles/best_women_24loc.h5" if sexe == "femme" else "..modeles/best_men_24loc.h5"
    model = load_model(model_path) 
    predictions = model.predict(extract_vectors(file,sexe))
    predictions = np.argmax(predictions, axis = 1)
    print((predictions))
    
    age = "- de 30 ans" if predictions == [0] else "+ de 60 ans"
    return age
