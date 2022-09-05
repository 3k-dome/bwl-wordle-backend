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

# settings

```
{
    "host": "0.0.0.0",                <- host ip as string
    "port": "8000",                   <- port as string
    "secret": "QmllckJpZXJCaWVy=",    <- jwt secret as string
    "token_expires" : 3600,           <- number of seconds it takes for the jwt to expire as integer
    "daily": true,                    <- wether the cycle should update daily or not as boolean
    "interval": 900,                  <- length of a cycle in seconds as integer, requires daily = false
    "difficulties": [                 <- a list of difficulties, only red on first server start, delete database folder to reset
        {
            "name": "Easy",           <- name of the difficilty
            "tries": 9                <- number of allowed tries
        },
        {
            "name": "Normal",
            "tries": 6
        },
        {
            "name": "Hard",
            "tries": 3
        }
    ]
}
```
