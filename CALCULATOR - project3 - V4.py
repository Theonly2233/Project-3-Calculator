# ==========================================
# PROJECT 3 - CALCULATOR
# ==========================================
# Version 4
# - Removed nested functions to improve readability.
# - Created a calculate function to reduce WET code.
# - Fixed stacks longer than 2 raising an error.
# - Implemented the prompt() function into the valid_equation() function.
# - Catches and returns a costom message when a ZeroDivisionError occures.
# - Recognizes numbers adjacent to parentheses as multiplication.
# ==========================================


# ==========================================
# IMPORTS
# ==========================================
from re import split as regex_split


# ==========================================
# CONSTANTS
# ==========================================
OPERATION_DICT = {
    'ADD_SUBTRACT': {
        '+': lambda x, y: x + y, 
        '-': lambda x, y: x - y
    },
    'MULTIPLY_DIVIDE': {
        '%': lambda x, y: x % y,
        '*': lambda x, y: x * y, 
        '//': lambda x, y: x // y, 
        '/': lambda x, y: x / y
    },
    'POWER_MODULO': {
        '**': lambda x, y: x ** y
    },
    'PARENTHESES': {
        '(': None,
        ')': None
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

    if not any(value in OPERATION_DICT[category] for category in OPERATION_DICT):
        valid = False

    return valid


def valid_equation():
    while True:
        get_input = input('Equation: ')
        get_input = get_input.strip().replace(' ', '')
        pattern = r'(\d+\.?\d*|//|\*\*|\*|\+|\-|/|\(|\)|\%)'
        segments = [seg for seg in regex_split(pattern, get_input) if seg]
        equation = []
        is_valid = True

        for position in range(len(segments)):
            current_segment = segments[position]
            next_segment = segments[position + 1] if position + 1 < len(segments) else None
            
            if is_number(current_segment):
                current_segment = float(current_segment)
                equation.append(current_segment)

                if next_segment is not None and next_segment in '(':
                    equation.append('*')

                if next_segment is not None and is_number(next_segment):
                    print(f'Invalid equation sequence.\nError at: {segments[position + 1]}')
                    is_valid = False
                    continue
            
            elif is_operation(current_segment):
                equation.append(current_segment)

                if current_segment == ')' and next_segment is not None and is_number(next_segment):
                    equation.append('*')

                if next_segment is not None and is_operation(next_segment) and current_segment not in ['(', ')'] and next_segment not in ['(', ')']:

                    if any(next_segment in OPERATION_DICT[category] for category in OPERATION_DICT if category != 'PARENTHESES'):
                        print(f'Invalid equation sequence.\nError at: {segments[position + 1]}')
                        is_valid = False
                        continue

        if is_valid:       
            return equation


def perform_operation(target_list, dictionary):
    for index in range(len(target_list)):
        command = target_list[index]

        if command in dictionary:
            previous_position = target_list[index - 1]
            next_position = target_list[index + 1] if index + 1 < len(target_list) else None
            operation = dictionary[command]
            target_list[index - 1 : index + 2] = [operation(previous_position, next_position)]
            return True
        
    return False


def calculate(target_list):
    while len(target_list) > 1:
        try:
            if perform_operation(target_list, OPERATION_DICT['POWER_MODULO']):
                continue

            if perform_operation(target_list, OPERATION_DICT['MULTIPLY_DIVIDE']):
                continue
            
            if perform_operation(target_list, OPERATION_DICT['ADD_SUBTRACT']):
                continue
        
        except ZeroDivisionError:
            print('Invalid equation sequence.\nError at: Cannot divide by 0')
            return None
        
    return target_list[0]


def parentheses_check(equation):
    if equation.count('(') >= 1:

        if equation.count(')') != equation.count('('):
            print('Invalid equation sequence.\nError at: (N/A)')
            return None
        
        else:
            start = None
            stop = None

            for index, segment in enumerate(equation):
                if segment == '(':
                    start = index
                elif segment == ')':
                    stop = index
                    break

            if start is None or stop is None or stop < start:
                print(f'Invalid equation sequence.\nError at: {equation[stop]}')
                return None
            
            stack = equation[start + 1 : stop]
            inner_result = calculate(stack)

            if inner_result is None:
                return None

            equation[start : stop + 1] = [inner_result]
            return True
                            
    else:
        return False


def execution():
    equation = valid_equation()

    while True:
        parenthesis_result = parentheses_check(equation)
        if parenthesis_result is True:
            continue
        if parenthesis_result is None:
            return None
        break

    return calculate(equation)

def main():
    while True:
        result = execution()

        if result == 0:
            pass
        elif result is None:
            continue

        print(f'Result: {result}')

        while True:
            continue_prompt = input('Do you want to continue? (y/n): ')

            if continue_prompt.strip().lower() in ['n', 'no']:
                exit = True
                break
            elif continue_prompt.strip().lower() in ['y', 'yes']:
                exit = False
                break
            else:
                print('Invalid input. Please enter "y" or "n".')

        if exit:
            break


# ==========================================
# MAIN PROGRAM
# ==========================================
main()
