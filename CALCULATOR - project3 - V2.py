# ==========================================
# PROJECT 3 - CALCULATOR
# ==========================================
# Version 1
# - Initial version of the project.
# ==========================================

# ==========================================
# CONSTANTS
# ==========================================
OPERATION_DICT = {
    'ADD_SUBTRACT': {
        '+': lambda x, y: x + y, 
        '-': lambda x, y: x - y
    },
    'MULTIPLY_DIVIDE': {
        '*': lambda x, y: x * y, 
        '/': lambda x, y: x / y
    },
    'POWER_MODULO': {
        '**': lambda x, y: x ** y, 
        '//': lambda x, y: x // y, 
        '%': lambda x, y: x % y
    }
}


# ==========================================
# FUNCTIONS
# ==========================================
def is_number(value):
    valid = True
    try:
        float(value)
    except ValueError:
        valid = False
    return valid


def is_operation(value):
    valid = True
    if not value in OPERATION_DICT['ADD_SUBTRACT'] and not value in OPERATION_DICT['MULTIPLY_DIVIDE'] and not value in OPERATION_DICT['POWER_MODULO']:
        valid = False
    return valid


def valid_equation():
    get_input = input('Equation: ')
    segments = get_input.split()
    equation = []
    
    if len(segments) % 2 == 0:
            print(f'Invalid equation sequence.\nError at: {segments[-1]}, {segments[0]}')
            return None
    
    for position in range(len(segments)):
        current_segment = segments[position]

        if position % 2 == 0:
            if not is_number(current_segment):
                print(f'Invalid equation sequence.\nError at: {current_segment}')
                return None
            else:
                current_segment = float(current_segment)
                equation.append(current_segment)

        elif position % 2 != 0:
            if not is_operation(current_segment):
                print(f'Invalid equation sequence.\nError at: {current_segment}')
                return None
            else:
                equation.append(current_segment)
    
    return equation


def prompt():   
    while True:
        result = valid_equation()

        if result is None:
            continue
        
        return result



def execution():
    equation = prompt()

    while len(equation) > 1:
        for index in range(1, len(equation), 2):
            command = equation[index]

            if command in OPERATION_DICT['POWER_MODULO']:
                previous_position = equation[index - 1]
                next_position = equation[index + 1]
                operation = OPERATION_DICT['POWER_MODULO'][command]
                equation[index - 1 : index + 2] = [operation(previous_position, next_position)]
                complete = True
            complete = False
        if complete:
            continue

        for index in range(1, len(equation), 2):
            command = equation[index]

            if command in OPERATION_DICT['MULTIPLY_DIVIDE']:
                previous_position = equation[index - 1]
                next_position = equation[index + 1]
                operation = OPERATION_DICT['MULTIPLY_DIVIDE'][command]
                equation[index - 1 : index + 2] = [operation(previous_position, next_position)]
                complete = True
            complete = False
        if complete:
            continue

        for index in range(1, len(equation), 2):
            previous_position = equation[index - 1]
            next_position = equation[index + 1]
            command = equation[index]

            if command in OPERATION_DICT['ADD_SUBTRACT']:
                previous_position = equation[index - 1]
                next_position = equation[index + 1]
                operation = OPERATION_DICT['ADD_SUBTRACT'][command]
                equation[index - 1 : index + 2] = [operation(previous_position, next_position)]
                complete = True
            complete = False
        if complete:
            continue

    result = equation[0]
    return result


def main():
    print(execution())

    
# ==========================================
# MAIN PROGRAM
# ==========================================
main()
