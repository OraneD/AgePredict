#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 13:56:51 2024

@author: orane
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse
import os
import shutil
from age_prediction import predict_age
from pages import success_page, error_page
from score import write_to_csv, calculate_model_score

app = FastAPI()

"""
API et fonctions asynchrones
CSS directement inclus dans le code HTML
"""

@app.get("/", response_class=HTMLResponse)
async def main():
    score, nb_fichier = calculate_model_score()
    print(score)
    content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AgePredict</title>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
            font-family: Arial, sans-serif;
        }}
        form {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px; 
            background-color: #f2f2f2;
            padding: 20px;
            border-radius: 10px;
        }}
        .gender-selection {{
            display: flex;
            justify-content: center;
            gap: 20px; 
        }}
        .gender-selection label {{
            margin: 0; 
        }}
        input[type="file"] {{
            margin-top: 10px;
        }}
        input[type="submit"] {{
            margin-top: 20px;
            padding: 10px 20px;
            border: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            border-radius: 5px;
        }}
        input[type="submit"]:hover {{
            background-color: #45a049;
        }}
        h1 {{
            color: #333;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <h1>AgePredict</h1>
    <p>Score actuel du modèle : {score:.2f}% sur {nb_fichier} locuteurs</p>
    <div class="instructions">
        Veuillez entrer un fichier audio de 2 à 10 secondes.
    </div>
    <form id="uploadForm" action="/uploadfile/" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <div class="gender-selection">
            <div>
                <input type="radio" id="male" name="gender" value="homme" checked>
                <label for="male">Homme</label>
            </div>
            <div>
                <input type="radio" id="female" name="gender" value="femme">
                <label for="female">Femme</label>
            </div>
            <div>
            <input name="real_age" type="number" min="0" placeholder="Âge réel (optionnel)">
            </div>
        </div>
        <input type="submit">
    </form>
</body>
</html>
"""
    return HTMLResponse(content=content)

@app.post("/uploadfile/", response_class=HTMLResponse)
async def create_upload_file(file: UploadFile = File(...), gender: str = Form(...),  real_age: int = Form(None)):
    file_path=None
    try:
        print(f"Type MIME du fichier téléchargé: {file.content_type}")  
        allowed_types = ["audio/mpeg", "audio/wav", "audio/x-wav"]
        if file.content_type not in allowed_types :
            return HTMLResponse(content=error_page("Le fichier téléchargé n'est pas au bon format"))
        os.makedirs("uploaded_files", exist_ok=True)
        file_path = f"uploaded_files/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        age_category = predict_age(file_path, gender)
        write_to_csv(age_category, real_age)
        response_content = success_page(file.filename, gender, age_category)

    except Exception as e:
            return HTMLResponse(content=error_page(f"Une erreur est survenue : {str(e)}"), status_code=500)
    finally:
        if file_path and os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            
        
    return HTMLResponse(content=response_content)


