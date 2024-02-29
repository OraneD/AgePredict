#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 15:44:08 2024

@author: orane
"""

import csv
import os

def write_to_csv(predicted_age, real_age):
    file_exists = os.path.isfile('predictions.csv')
    with open('predictions.csv', 'a', newline='') as csvfile:
        fieldnames = ['predicted_age', 'real_age', 'correct']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        if real_age is not None:
           correct = (predicted_age == real_age_category(real_age))
        else:
           correct = 'N/A' 
        writer.writerow({'predicted_age': predicted_age, 'real_age': real_age if real_age is not None else 'N/A', 'correct': correct})

        
def calculate_model_score():
    if os.path.isfile('predictions.csv') :
        correct_predictions = 0
        total_comparable_predictions = 0
        with open('predictions.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['correct'] not in ['N/A', '']:  
                    total_comparable_predictions += 1
                    if row['correct'] == 'True':
                        correct_predictions += 1
        return (correct_predictions / total_comparable_predictions * 100) if total_comparable_predictions else 0, total_comparable_predictions
    else :
        return 0, 0


def real_age_category(real_age):
    if real_age < 30:
        return "- de 30 ans"
    elif real_age > 60:
        return "+ de 60 ans"
    else:
        return "30 à 60 ans"