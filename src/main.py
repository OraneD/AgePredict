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

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def main():
    content = """
<!DOCTYPE html>
<html>
<head>
    <title>Prédiction d'âge</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
            font-family: Arial, sans-serif;
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
            background-color: #f2f2f2;
            padding: 20px;
            border-radius: 10px;
        }
        input[type="file"] {
            margin-top: 10px;
        }
        input[type="submit"] {
            margin-top: 20px;
            padding: 10px 20px;
            border: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            border-radius: 5px;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        label {
            margin-right: 10px;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>AgePredict</h1>
    <div class="instructions">
        Veuillez entrer un fichier audio de 2 à 10 secondes.
    </div>
    <form id="uploadForm" action="/uploadfile/" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <div>
            <label for="male">Homme</label>
            <input type="radio" id="male" name="gender" value="homme" checked>
            <label for="female">Femme</label>
            <input type="radio" id="female" name="gender" value="femme">
        </div>
        <input type="submit">
    </form>
</body>
</html>
    """
    return HTMLResponse(content=content)

@app.post("/uploadfile/", response_class=HTMLResponse)
async def create_upload_file(file: UploadFile = File(...), gender: str = Form(...)):
    try:
        os.makedirs("uploaded_files", exist_ok=True)
        file_path = f"uploaded_files/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        age_category = predict_age(file_path, gender)
        response_content =  f"""
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
        <p>Nom du fichier : {file.filename}</p>
        <p>Sexe : {gender}</p>
        <p>Prédiction de l'âge : {age_category}</p>
        <a href="/">Nouvelle prédiction</a>
    </div>
</body>
</html>
""" 

    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    finally:
        if file_path and os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            
        
    return HTMLResponse(content=response_content)

