API hébergée à cette adresse : http://13.53.175.163:8000/
## Pour faire fonctionner localement :
* cloner le dépôt
* création d'un nouvel environnement virtuel (fortemment recommandé)
```
python -m venv <environment name>
source env_path/bin/activate
```
* installer les dépendances
```
pip install -r requirements.txt
```
* lancer l'api :
```
cd src/
uvicornn main:app --reload
```
