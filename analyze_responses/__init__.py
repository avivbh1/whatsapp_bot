import os
import sys
from analyze_responses.translation import set_language_db
if not os.path.isfile('languages.db'):
    set_language_db()
