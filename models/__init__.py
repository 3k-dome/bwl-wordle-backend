from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# all our models rely on this 'db' object so we import them after its
# creation to prevent circular imports, this also associates the 'db'
# with all our models, see model definitions

from .difficulty_model import Difficulty
from .score_model import Score
from .user_model import User
from .word_model import Word

# this makes 'from models import *' import all models

__all__ = ["Difficulty", "Score", "User", "Word"]
