def is_echo_op_valid(message):
    op_sections = message.split(" ")
    if op_sections[0] == "!echo":
        for section in op_sections:
            if section != "":  # at least one character that wont be ""
                return True
    return False


def get_echo_data(message):
    op_sections = message.split(" ")
    return " ".join(op_sections[1:])
