from constants import constants


def change_permission(operations_by_permissions, message):
    op_section = message.split(" ")
    if op_section[0] == constants.ENABLE:
        operations_by_permissions[op_section[-1]] = True
    elif op_section[0] == constants.DISABLE:
        operations_by_permissions[op_section[-1]] = False
    return operations_by_permissions
