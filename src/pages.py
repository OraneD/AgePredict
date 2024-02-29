#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 15:19:47 2024

@author: orane
"""

"""
Fonctions qui envoient la réponse HTML en cas de succès (prédiction de l'âge)
ou dans le cas d'une éventuelle erreur (mauvais format de fichier..)
"""

def success_page(file, gender, age_category):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Résultat de la prédiction</title>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
        }}
        .result-container {{
            text-align: center;
            background-color: #f2f2f2;
            padding: 20px;
            border-radius: 10px;
        }}
        h1 {{
            color: #333;
            margin-bottom: 20px;
        }}
        p {{
            color: #666;
            font-size: 16px;
        }}
        a {{
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            border: none;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            cursor: pointer;
            border-radius: 5px;
        }}
        a:hover {{
            background-color: #45a049;
        }}
    </style>
</head>
<body>
    <div class="result-container">
        <h1>AgePredict</h1>
        <p>Nom du fichier : {file}</p>
        <p>Sexe : {gender}</p>
        <p>Prédiction de l'âge : {age_category}</p>
        <a href="/">Nouvelle prédiction</a>
    </div>
</body>
</html>
""" 

def error_page(message):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Erreur</title>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
        }}
        .result-container {{
            text-align: center;
            background-color: #f2f2f2;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
        }}
        p {{
            color: #666;
            font-size: 16px;
        }}
        a {{
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            border: none;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            cursor: pointer;
            border-radius: 5px;
        }}
        a:hover {{
            background-color: #45a049;
        }}
    </style>
</head>
<body>
    <div class="result-container">
        <h1>Erreur</h1>
        <p>{message}</p>
        <a href="/">Réessayer</a>
    </div>
</body>
</html>
"""