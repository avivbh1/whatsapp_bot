from selenium import webdriver
from bs4 import BeautifulSoup
from constants import constants


def start_chrome_page(url=None):
    """
    starting the chrome page
    :return: the driver of the chrome web-driver
    """
    driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH)
    if url is not None:
        driver.get(url)
    input("click enter after scanning the QR:")

    return driver


def get_current_html_document_of_source_page(html):
    """
    returns the html of the current page_source (in type str)
    :param html:
    :return: driver.page_source (str type)
    """

    return BeautifulSoup(html, "html.parser")


#https://web.whatsapp.com/