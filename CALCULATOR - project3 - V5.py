# ==========================================
# PROJECT 3 - CALCULATOR
# ==========================================
# Version 5
# - Differentiates between negetive numbers and subtraction operations.
# - Implemented math imports
# - Improved formatting and added docstrings in functions to improve readability.
# ==========================================


# ==========================================
# IMPORTS
# ==========================================
from re import split as regex_split
import math as m


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
    'MATH_IMPORT': {
        'sqrt': lambda x: m.sqrt(x),
        'exp': lambda x: m.exp(x),
        'sin': lambda x: m.sin(x),
        'cos': lambda X: m.cos(X),
        'tan': lambda x: m.tan(x),
        'log10': lambda x: m.log10(x),
        'log2': lambda x: m.log2(x),
        'radians': lambda x: m.radians(x),
        'degrees': lambda x: m.degrees(x),
        'fabs': lambda x: m.fabs(x)
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
    """
    Checks if the value is a number.

    Args:
        value (str): An index of an equation input.
        
    Returns:
        bool: Weather or not the value is a number.
    """
    valid = True

    try:
        float(value)
    except ValueError:
        valid = False

    return valid


def is_operation(value):
    """
    Checks if the value is an operation.

    Args:
        value (str): An index of an equation input.
        
    Returns:
        bool: Weather or not the value is a operation.
    """
    valid = True

    if not any(value in OPERATION_DICT[category] for category in OPERATION_DICT):
        valid = False

    return valid


def valid_equation():
    """
    Gets user input and checks its validity while converting it into an equation ready for calculation.

    Returns:
        bool: False if the input is invalid.
        list: A prepaired equation ready for calculation.
    """
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

                if current_segment in OPERATION_DICT['MATH_IMPORT'] and (next_segment in OPERATION_DICT['PARENTHESES'] or is_number(next_segment)):
                    continue

                if next_segment is not None and is_operation(next_segment) and next_segment != '-' and current_segment not in ['(', ')'] and next_segment not in ['(', ')']:
                    if any(next_segment in OPERATION_DICT[category] for category in OPERATION_DICT if category != 'PARENTHESES'):
                        print(f'Invalid equation sequence.\nError at: {segments[position + 1]}')
                        is_valid = False
                        break

        if is_valid:   
            cleaned_equation = []
            skip_next = False

            for i in range(len(equation)):
                if skip_next:
                    skip_next = False
                    continue

                current_segment = equation[i]
                next_segment = equation[i + 1] if i + 1 < len(equation) else None
                is_after_op = len(cleaned_equation) == 0 or is_operation(cleaned_equation[-1])

                if current_segment == '-' and next_segment is not None and is_number(next_segment) and is_after_op:
                    cleaned_equation.append(float(f"-{next_segment}"))
                    skip_next = True
                else:
                    cleaned_equation.append(current_segment)
            
            return cleaned_equation


def perform_operation(target_list, dictionary):
    """
    Checks each index of a list and solves each operation if its in the specified dictionary.

    Args:
        target_list (list): The equation or segment of equation ready for calculation.
        dictionary (dict): The dictionary containing the operation functions for calculation.
        
    Returns:
        bool: Weather or not an operation is performed.
    """
    for index in range(len(target_list)):
        command = target_list[index]

        if command in dictionary:
            next_position = target_list[index + 1] if index + 1 < len(target_list) else None
            operation = dictionary[command]

            if command in OPERATION_DICT['MATH_IMPORT']:
                target_list[index : index + 2] = [operation(next_position)]
                return True
            
            previous_position = target_list[index - 1]
            target_list[index - 1 : index + 2] = [operation(previous_position, next_position)]
            return True
        
    return False


def calculate(target_list):
    """
    Puts a list through ordered calculations (PEMDAS) until all operations are solved.

    Args:
        target_list (list): The equation or segment of equation ready for calculation.
        
    Returns:
        list: The last remaining index of a completed equation or segment of equation.
    """
    while len(target_list) > 1:
        try:
            if perform_operation(target_list, OPERATION_DICT['MATH_IMPORT']):
                continue

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
    """
    Checks through an equation for parentheses isolates them, then converts them to a single index.

    Args:
        equation (list): A validated equation ready for calculation.
        
    Returns:
        None: If parentheses are out of order.
        bool: Weather or not a parentheses is solved.
    """
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
    """
    Continuously cycles the equation through parentheses checks untill there are none remaining.
    Calculates the final result.

    Returns:
        list: The last remaining index of the whole eqation after all operations are solved.
    """
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
    """
    Continuously prompts the user for a valid equation.
    Prints the final result of a valid equation.

    """
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
