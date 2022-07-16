from colorama import Fore
import threading
from time import sleep

from analyze_responses import analyze_responses
from constants import constants
from constants.my_queue import Queue
from navigate_in_page import navigate_in_page
from whatsapp_web_api.receiving_queries import get_all_user_box_objects, get_all_new_messages, get_contact_id
from whatsapp_web_api.sending_queries import send_message_by_contact_name
from whatsapp_web_api.start_whatsapp_page import start_home_whatsapp_page, get_current_html_document_of_source_page
from analyze_responses.analyze_responses import set_all_operation_as_allow


def clear_chats_while_offline(driver, contact_boxes):
    """
    entering all chats in order to clear all the new messages spans.
    :param driver:
    :param contact_boxes:
    """
    for current_contact_box in contact_boxes:
        """ iterates for each html-contact-box """
        span_of_new_message = current_contact_box.find(["span"], class_=constants.NEW_MESSAGE_SPAN_CLASS_NAME)
        if span_of_new_message is not None:  # means there is a new message in this chat
            contact_id = get_contact_id(current_contact_box)  # getting the id of this contact
            navigate_in_page.enter_chat_by_contact_id(driver, contact_id)
    navigate_in_page.return_to_default(driver)


def receive(html_document):
    global income_messages, receiving_web_driver
    contact_boxes = get_all_user_box_objects(html_document)

    contact_id_by_new_messages = get_all_new_messages(receiving_web_driver, contact_boxes)

    navigate_in_page.return_to_default(receiving_web_driver)

    for contact in contact_id_by_new_messages:
        new_messages = contact_id_by_new_messages[contact]
        print(Fore.GREEN + f"{contact} just sent: {new_messages}\n")  # logger
        income_messages.push([contact, new_messages])
    sleep(0.05)


def checking_for_changes():
    global receiving_web_driver
    prev_html = receiving_web_driver.page_source  # getting the current state of the page

    #clear_chats_while_offline(prev_html, receiving_web_driver)

    # and starting since then
    while True:
        html = receiving_web_driver.page_source

        if html != prev_html:
            receive(get_current_html_document_of_source_page(html))
        prev_html = html
        sleep(0.5)


def analyzing():
    global income_messages
    while True:
        if income_messages.len() > 0:  # if there is a message to analyze
            contact_id, current_messages = income_messages.pop()
            # print(current_messages)
            response_content = analyze_responses.analyze_response(
                contact_id, current_messages)  # sending list of all the messages of contact
            response = [contact_id, response_content]

            print(Fore.RED + f"WE sending {contact_id}: {response_content}\n")
            all_responses.push(response)
        sleep(0.2)


def sending():
    global sending_web_driver
    while True:
        if all_responses.len() > 0:
            contact_id, responses_list = all_responses.pop()
            send_message_by_contact_name(sending_web_driver, contact_id, responses_list)
            navigate_in_page.return_to_default(sending_web_driver)
        sleep(0.5)


def main():
    """ starting the threads """
    analyzing_thread.start()
    sending_thread.start()

    """setting all operations as allow """
    set_all_operation_as_allow()
    """ starting main thread """
    checking_for_changes()


""" initializing the drivers """
receiving_web_driver = start_home_whatsapp_page()
sending_web_driver = start_home_whatsapp_page()

""" initializing the main queues """
income_messages = Queue()
all_responses = Queue()

""" initializing the threads """
analyzing_thread = threading.Thread(target=analyzing, daemon=True)
sending_thread = threading.Thread(target=sending, daemon=True)

if __name__ == '__main__':
    main()
