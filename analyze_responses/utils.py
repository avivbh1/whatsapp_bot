def trim_message(message):
    is_start_trimmed = False
    is_end_trimmed = False

    while not is_start_trimmed:
        if message[0] != " ":
            is_start_trimmed = True
        else:
            message = message[1:]

    while not is_end_trimmed:
        if message[-1] != " ":
            is_end_trimmed = True
        else:
            message = message[:-1]
    return message


