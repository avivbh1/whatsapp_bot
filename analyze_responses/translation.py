import sqlite3
from googletrans import Translator

from constants import constants

ALL_LANGUAGES = []  # setting it in the set_language_db function
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
    conn = sqlite3.connect(constants.LANGUAGES_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS languages (
        full_name text,
        shortcut text
        )""")

    with open(r"C:\Users\avivb\PycharmProjects\whatsapp_bot\analyze_responses\languages.txt", "r") as file:
        languages = file.read().split("\n")
        for language in languages:
            full_name, shortcut = language.split(" ")
            cursor.execute(f"INSERT INTO languages VALUES ('{full_name.lower()}' , '{shortcut}')")

    cursor = conn.cursor()
    cursor.execute("SELECT full_name FROM languages")
    ALL_LANGUAGES = cursor.fetchall()

    conn.commit()
    conn.close()


def is_translation_op_valid(message: str) -> bool:
    global ALL_LANGUAGES
    """
    checking if the the given message is a valid translate operation according the bot_protocol.txt
    :param message:
    :return: 
    """
    if len(ALL_LANGUAGES) == 0:  # setting the languages list
        set_language_db()
        print(ALL_LANGUAGES)

    op_sections = message.split(" ")
    if op_sections[0] == "!translate":
        if len(op_sections) >= 2:  # direct translate. <any language> -> english
            if len(op_sections[1]) >= 1:
                return True
    return False


def get_translate(message):
    """
    translating the sentence according to sl, tl parameters
    :param message:
    :return: translation of the sentence.
    """
    op_sections = message.split(" ")
    text = ""
    if op_sections[1][0] != "[" or op_sections[1][-1] != "]":  # means there wasn't a given language to translate to
        language_dest = "en"  # default translation (english)
        for i in range(1, len(op_sections)):  # running over all the words except the first one
            text += op_sections[i]

    else:
        with sqlite3.connect(constants.LANGUAGES_DB_PATH) as conn:
            cursor = conn.cursor()

            # running over all the words except the first 2
            for i in range(2, len(op_sections)):
                text += op_sections[i]

            # getting the shortcuts of the destination language
            chosen_language = op_sections[1][1:-1]  # cutting the brackets []
            cursor.execute(f"SELECT shortcut FROM languages WHERE full_name = '{chosen_language}'")
            language_dest = cursor.fetchone()[0]  # it returns as a tuple of one variable

    return TRANSLATER.translate(text, dest=language_dest).text
