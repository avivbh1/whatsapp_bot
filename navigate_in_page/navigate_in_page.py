import selenium
from selenium.webdriver.common.by import By
from constants import constants


def get_msg_box_object_by_xpath(driver):
    driver.find_element(By.XPATH, constants.MSG_BOX_RELATABLE_XPATH)


def enter_chat_by_contact_id(driver, contact_id):
    """
    entering the chat with contact by his name/phone number (id)
    :param driver:
    :param contact_id:
    :return:
    """
    xpath = f"//span[@title='{contact_id}']"
    element = driver.find_element(By.XPATH, xpath)  # entering the chat
    element.click()


def return_to_default(driver):
    """
    returns to a blocked chat, because we're sure this chat wont get any new messages
    :param driver:
    :return:
    """
    element = driver.find_element(By.XPATH, constants.DEFAULT_CHAT_XPATH)
    element.click()
