import sqlite3
from googletrans import Translator

from constants import constants

ALL_LANGUAGES = {}  # setting it in the set_language_db function
TRANSLATER = Translator()


def set_language_db():
    """
    setting the db file with all the languages and their shortcuts if it wasn't already existed
    :return: None
    """
    global ALL_LANGUAGES
    """
        creating the data base of the languages so it will be created and 'remembered'
    """
    conn = sqlite3.connect('languages.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE languages (
        full_name text,
        shortcut text
        )""")

    with open("languages.txt", "r") as file:
        languages = file.read().split("\n")
        for language in languages:
            full_name, shortcut = language.split(" ")
            cursor.execute(f"INSERT INTO languages VALUES ('{full_name.lower()}' , '{shortcut}')")

            cursor.execute("SELECT * FROM languages")
            ALL_LANGUAGES = dict(cursor.fetchall())

    conn.commit()
    conn.close()


def is_translation_op_valid(message: str) -> bool:
    global ALL_LANGUAGES
    """
    checking if the the given message is a valid translate operation according the bot_protocol.txt
    :param message:
    :return: 
    """
    op_sections = message.split(" ")
    if op_sections[0] == "!translate":
        if len(op_sections) == 3:
            if op_sections[1].lower() in ALL_LANGUAGES:
                return True
        elif len(op_sections) == 2:  # direct translate. english->hebrew or hebrew->english
            return True
    return False


def get_translate(message):
    """
    translating the sentence according to sl, tl parameters
    :param message:
    :param language_dest: the way we need to parse the data
    :return: translation of the sentence.
    """
    op_sections = message.split(" ")
    text = op_sections[-1]

    if len(op_sections) == 2:
        language_dest = "en"

    elif len(op_sections) == 3:
        with sqlite3.connect(constants.LANGUAGES_DB_PATH) as conn:
            cursor = conn.cursor()
            # getting the shortcuts of the destination language
            cursor.execute(f"SELECT shortcut FROM languages WHERE full_name = '{op_sections[1].lower()}'")
            language_dest = cursor.fetchone()

    return TRANSLATER.translate(text, dest=language_dest).text
