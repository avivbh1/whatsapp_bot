from selenium import webdriver
from bs4 import BeautifulSoup


def start_home_whatsapp_page():
    """

    :return: the html source of the whatsapp web home page
    """
    url = "https://web.whatsapp.com/"

    driver = webdriver.Chrome(r"C:\Users\avivb\PycharmProjects\whatsapp_bot\chromedriver.exe")
    driver.get(url)

    input("click enter after scanning the QR:")

    return driver


def get_current_html_document_of_source_page(driver):
    """
    returns the html of the current page_source (in type str)
    :param driver:
    :return: driver.page_source (str type)
    """

    return BeautifulSoup(driver.page_source, "html.parser")

