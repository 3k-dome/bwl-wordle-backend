# bwl-wordle-backend
Repository for the flask backend of our main repository. See https://github.com/3k-dome/bwl-wordle.

Release version is served without the front end see main repository for a full release.

# build
```
pyinstaller --clean --distpath ./dist app.py --add-data "settings.json;." --add-data "assets/*.json;assets" --name "bwl-wordle-backend"
```

# install 

Python 3.10+ is required. To install simply run the following commands in the project root open.

```
python -m venv venv
./venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
```