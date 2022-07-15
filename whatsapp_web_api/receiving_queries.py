from constants import constants
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from navigate_in_page import navigate_in_page


def get_all_user_box_objects(html_document):
    """
    :param html_document: the html source of the whatsapp web home page
    :return: all the div objects of each contact in the right side of the home page
    :rtype: bs4.element.type
    """
    contact_boxes_objects = html_document.find_all(["div"],
                                                   class_=constants.CONTACT_BOX_OBJECT_CLASS_NAME)  # gets me a list of all the contact_box objects
    return contact_boxes_objects


def get_contact_id(contact_box_html):
    """
    gets the html of a contact box (in bs4 type) and returns the contact name/phone number (id) of this contact box
    :param contact_box_html:
    :return: contact_id: the name/phone number of the contact
    """
    span_of_contact_name = contact_box_html.find(["span"],
                                                 attrs={"class": constants.CONTACT_ID_SPAN_CLASS_NAME, "title": True})
    return span_of_contact_name.text


def get_new_messages_by_contact_id(driver, contact_id, num_of_new_messages):
    """
    gets all the messages in a list for the specific contact
    :param driver:
    :param contact_id: contact's name/phone number
    :param num_of_new_messages:
    :return all_new_messages: list of strings
    """
    navigate_in_page.enter_chat_by_contact_id(driver, contact_id)
    current_html_source = driver.page_source
    html_doc = BeautifulSoup(current_html_source, "html.parser")

    chat_frame = html_doc.find(["div"], attrs={"class": constants.CLASS_NAME_OF_CHAT_FRAME})
    all_messages = chat_frame.find_all(["span"], class_=constants.CLASS_NAME_OF_MESSAGE_IN_CHAT)[
                   ::-1]  # from most to less recent

    all_new_messages = []
    for i in range(num_of_new_messages):
        all_new_messages.append(str(all_messages[i].text))
    return all_new_messages[::-1]


def get_all_new_messages(driver, contact_boxes):
    """
    gets all the the new messages for each contact.
    :param driver:
    :param contact_boxes:
    :return contact_id_by_new_messages: contact's id's as keys and new messages as values(list of all the messages)
    """
    contact_id_by_new_messages = {}
    for current_contact_box in contact_boxes:
        """ iterates for each html-contact-box """
        span_of_new_message = current_contact_box.find(["span"], class_=constants.NEW_MESSAGE_SPAN_CLASS_NAME)
        if span_of_new_message is not None:  # means there is a new message in this chat
            num_of_new_messages = int(span_of_new_message.text)
            contact_id = get_contact_id(current_contact_box)  # getting the id of this contact

            all_new_messages_of_contact = get_new_messages_by_contact_id(driver, contact_id, num_of_new_messages)
            contact_id_by_new_messages[contact_id] = all_new_messages_of_contact

    return contact_id_by_new_messages
