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
<body>
<form action="/uploadfile/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<label for="male">Homme</label>
<input type="radio" id="male" name="gender" value="homme" checked>
<label for="female">Femme</label>
<input type="radio" id="female" name="gender" value="femme">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), gender: str = Form(...)):
    try:
        os.makedirs("uploaded_files", exist_ok=True)
        file_path = f"uploaded_files/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        age_category = predict_age(file_path, gender)  # Utilisez l'information sur le sexe ici
        return {"filename": file.filename, "gender": gender, "age_prediction": age_category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))