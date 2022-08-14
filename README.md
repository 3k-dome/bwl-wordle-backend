# bwl-wordle-backend
Repository for the flask backend of our main repository. See https://github.com/3k-dome/bwl-wordle.

# build
``pyinstaller --clean --distpath ./dist app.py --add-data "settings.json;." --add-data "assets/*.json;assets" --name "bwl-wordle-backend"``