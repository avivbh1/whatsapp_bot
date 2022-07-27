import sqlite3
from time import sleep
import requests
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome import webdriver

from constants import constants
from whatsapp_web_api.start_chrome_page import get_current_html_document_of_source_page

ALL_LANGUAGES = []  # setting it in the set_language_db function


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

    op_sections = message.split(" ")
    if op_sections[0] == constants.TRANSLATE_OP:
        if len(op_sections) >= 2:  # direct translate. <any language> -> english
            if len(op_sections[1]) >= 1:
                return True
    return False


def get_translate(driver: webdriver, message):
    """
    translating the sentence in the message using google translate
    :param message:
    :param driver: the web driver
    :return: translation of the sentence.
    """
    op_sections = message.split(" ")
    text = ""
    if op_sections[1][0] != "[" or op_sections[1][-1] != "]":  # means there wasn't a given language to translate to
        language_dest = "en"  # default translation (english)
        text = " ".join(op_sections[1:])

    else:
        with sqlite3.connect(constants.LANGUAGES_DB_PATH) as conn:
            cursor = conn.cursor()

            # running over all the words except the first 2
            text = " ".join(op_sections[2:])

            # getting the shortcuts of the destination language
            chosen_language = op_sections[1][1:-1]  # cutting the brackets []
            cursor.execute(f"SELECT shortcut FROM languages WHERE full_name = '{chosen_language}'")
            try:
                language_dest = cursor.fetchone()[0].lower()  # it returns as a tuple of one variable
            except TypeError:
                return constants.FALSE_LANGUAGE_MSG

    # https://translate.google.com/?hl=iw&tl=es&text=whats%20up&op=translate - how the full url looks like

    translate_page_url = f"https://translate.google.com/?hl=iw&tl={language_dest}&text={text}&op=translate"
    if driver.current_url != constants.WHATSAPP_WEB_URL:
        driver.get(translate_page_url)
    sleep(3)
    try:
        return driver.find_element(By.XPATH, constants.XPATH_OF_TRANSLATED_SENTENCE).text  # returning the translated text
    except:
        return constants.TIMEOUT_ERROR_MSG
