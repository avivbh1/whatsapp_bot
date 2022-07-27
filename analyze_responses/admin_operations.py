from constants import constants


def change_permission(operations_by_permissions, message):
    op_section = message.split(" ")

    if op_section[0] == constants.ENABLE:
        if op_section[-1] == constants.ALL_OPERATIONS:
            print("enabled all operations")
            for operation in operations_by_permissions:
                operations_by_permissions[operation] = True
        else:
            print(f"enabled {op_section[-1]} operation")
            operations_by_permissions[op_section[-1]] = True

    elif op_section[0] == constants.DISABLE:
        if op_section[-1] == constants.ALL_OPERATIONS:
            print("disabled all operations")
            for operation in operations_by_permissions:
                operations_by_permissions[operation] = False
        else:
            print(f"disabled {op_section[-1]} operation")
            operations_by_permissions[op_section[-1]] = False

    return operations_by_permissions
