from analyze_responses.translation import is_translation_op_valid, get_translate
from analyze_responses.utils import trim_message
from constants import constants
from analyze_responses.echo import is_echo_op_valid, get_echo_data
from analyze_responses.admin_operations import change_permission
from analyze_responses.tag_all import is_tag_all_op_valid
"""
    all operation will be written without spaces.
"""

operations_by_permissions = {}  # this dict will contain all kinds of operations the user can do and if they're allow currently


def set_all_operation_as_allow():
    global operations_by_permissions
    operations_by_permissions[constants.TRANSLATE_OP] = True
    operations_by_permissions[constants.ECHO_OP] = True
    operations_by_permissions[constants.TAG_ALL_OP] = True


def analyze_response(analyze_driver, contact_id, all_messages):
    global operations_by_permissions
    all_responses = []
    print(f"all messages are: {all_messages}")
    for message in all_messages:
        fixed_message = ""
        for char in message:  # getting rid of \n
            if char != "\n":
                fixed_message += char
            else:
                fixed_message += " "
        # checks if the operation is sent by admin
        if contact_id == constants.ADMIN and (fixed_message[:6] == constants.ENABLE or fixed_message[:7] == constants.DISABLE):
            operations_by_permissions = change_permission(operations_by_permissions, trim_message(fixed_message))

        # checks if the operation is translation
        elif operations_by_permissions[constants.TRANSLATE_OP] and is_translation_op_valid(trim_message(fixed_message)):
            fixed_message = trim_message(message)
            all_responses.append(get_translate(analyze_driver, fixed_message))

        # checks if the operation is echo
        elif operations_by_permissions[constants.ECHO_OP] and is_echo_op_valid(trim_message(fixed_message)):
            all_responses.append(get_echo_data(fixed_message))

        # checks if the operation is tag all
        elif operations_by_permissions[constants.TAG_ALL_OP] and is_tag_all_op_valid(trim_message(fixed_message)):
            #tag all function
            pass
    print(f"all responses are: {all_responses}")
    return all_responses
