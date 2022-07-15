from analyze_responses.translation import is_translation_op_valid, get_translate
from analyze_responses.utils import trim_message

"""
    all operation will be written without spaces.
"""


def analyze_response(all_messages):
    all_responses = []
    fixed_message = ""
    for message in all_messages:
        message = trim_message(message)
        for char in message:  # getting rid of \n
            if char != "\n":
                fixed_message += char
            else:
                fixed_message += " "

        """ checks if the operation is translation """
        if is_translation_op_valid(fixed_message):
            all_responses.append(get_translate(fixed_message))
        else:
            all_responses.append(fixed_message)
    return all_responses
