from time import sleep
import threading

from whatsapp_web_api.start_whatsapp_page import start_home_whatsapp_page, get_current_html_document_of_source_page
from whatsapp_web_api.receiving_queries import get_all_user_box_objects, get_all_new_messages
from whatsapp_web_api.sending_queries import send_message_by_contact_name
from analyze_responses import analyze_responses
from navigate_in_page import navigate_in_page
from constants.my_queue import Queue
from analyze_responses.translation import set_language_db


def receive(html_document):
    global income_messages, receiving_web_driver
    contact_boxes = get_all_user_box_objects(html_document)

    contact_id_by_new_messages = get_all_new_messages(receiving_web_driver, contact_boxes)

    navigate_in_page.return_to_default(receiving_web_driver)

    for contact in contact_id_by_new_messages:
        income_messages.push([contact, contact_id_by_new_messages[contact]])
    sleep(0.05)


def checking_for_changes():
    global receiving_web_driver
    prev_html = receiving_web_driver.page_source  # getting the current state of the page
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
            response_content = analyze_responses.analyze_response(
                current_messages)  # sending list of all the messages of contact
            response = [contact_id, response_content]

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
    analyzing_thread.start()
    sending_thread.start()

    checking_for_changes()


if __name__ == '__main__':
    """ starting the page """
    receiving_web_driver = start_home_whatsapp_page()
    sending_web_driver = start_home_whatsapp_page()

    """ global variables """
    income_messages = Queue()
    all_responses = Queue()

    analyzing_thread = threading.Thread(target=analyzing, daemon=True)
    sending_thread = threading.Thread(target=sending, daemon=True)

    main()
