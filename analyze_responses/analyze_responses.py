from analyze_responses.translation import is_translation_op_valid, get_translate
"""
    all operation will be written without spaces.
"""


def analyze_response(message):
    fixed_message = ""
    for char in message:  # getting rid of \n
        if char != "\n":
            fixed_message += char
        else:
            fixed_message += " "

    """ checks if the operation is translation """
    if is_translation_op_valid(fixed_message):
        return get_translate(fixed_message)

    else:
        return message
