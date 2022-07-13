from selenium import webdriver
from bs4 import BeautifulSoup
from constants import constants


def start_home_whatsapp_page():
    """

    :return: the html source of the whatsapp web home page
    """
    driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH)
    driver.get(constants.WHATSAPP_WEB_URL)

    input("click enter after scanning the QR:")

    return driver


def get_current_html_document_of_source_page(html):
    """
    returns the html of the current page_source (in type str)
    :param html:
    :return: driver.page_source (str type)
    """

    return BeautifulSoup(html, "html.parser")
