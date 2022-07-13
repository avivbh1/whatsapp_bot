from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By

from constants import constants
from navigate_in_page import navigate_in_page


def send_message_by_contact_name(driver: webdriver, contact_id: str, list_of_responses: List[str]):
    """
    sends all of them seperatly it to the contact.
    :param driver: web driver by selenium ( the window )
    :param contact_id: the contact's name/phone number
    :param list_of_responses: list of messages (string)
    :return: None
    """
    navigate_in_page.enter_chat_by_contact_id(driver, contact_id)
    msg_box = driver.find_element(By.XPATH, constants.MSG_BOX_RELATABLE_XPATH)  #

    for response in list_of_responses:
        msg_box.send_keys(response)
        send_button = driver.find_element(By.XPATH, constants.SEND_BUTTON_XPATH)  # after we send the msg to the msg box we can locate the send button
        send_button.click()
