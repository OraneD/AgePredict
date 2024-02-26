#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:25:48 2024

@author: orane
"""


import torch
import librosa
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from transformers import Wav2Vec2Processor
import numpy as np

"""
Ce script permet de transformer l'input de l'utilisateur en vecteur
"""
def extract_vectors(file,sexe):
    layer = 5 if sexe == "homme" else 0
    model_name = "facebook/wav2vec2-large-xlsr-53-french"
    tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name)
    model = Wav2Vec2ForCTC.from_pretrained(model_name)
    processor = Wav2Vec2Processor.from_pretrained(model_name)
    audio_input, sample_rate = torchaudio.load(file)
    if sample_rate != 16000:
        audio_input = torchaudio.functional.resample(audio_input, sample_rate, 16000)

    input_values = processor(audio_input, return_tensors="pt", sampling_rate=16000).input_values
    input_values = input_values.reshape(1, input_values.shape[2])

    with torch.no_grad():
        hidden_state = model(input_values, output_hidden_states=True).hidden_states

    embeddings = hidden_state[layer]
    speech_representation = embeddings[0].max(axis=0).values

    x = speech_representation.numpy()
    x = np.expand_dims(x, axis=0)
    print(x.shape)
        
    return x
