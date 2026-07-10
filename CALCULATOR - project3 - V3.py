# ==========================================
# PROJECT 3 - CALCULATOR
# ==========================================
# Version 3
# - Added parentheses support.
# - Added imported regex_split to split at opperations.
# - Used .strip() and .replace() to remove spaces.
# - Made execution() accept lists.
# - Added a loop to allow for multiple equations each session and an exit feture.
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
        '*': lambda x, y: x * y, 
        '/': lambda x, y: x / y
    },
    'POWER_MODULO': {
        '**': lambda x, y: x ** y, 
        '//': lambda x, y: x // y, 
        '%': lambda x, y: x % y
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
    get_input = input('Equation: ')
    get_input = get_input.strip().replace(' ', '')
    pattern = r'(\d+\.?\d*|\*\*|//|\+|\-|\*|/|\(|\)|\%)'
    segments = [seg for seg in regex_split(pattern, get_input) if seg]
    equation = []

    for position in range(len(segments)):
        current_segment = segments[position]
        next_segment = segments[position + 1] if position + 1 < len(segments) else None
        
        if is_number(current_segment):
            current_segment = float(current_segment)
            equation.append(current_segment)

            if next_segment is not None and is_number(next_segment):
                print(f'Invalid equation sequence.\nError at: {segments[position + 1]}')
                return None
        
        elif is_operation(current_segment):
            equation.append(current_segment)

            if next_segment is not None and is_operation(next_segment):
                if current_segment not in ['(', ')'] and next_segment not in ['(', ')']:
                    if any(next_segment in OPERATION_DICT[category] for category in OPERATION_DICT if category != 'PARENTHESES'):
                        print(f'Invalid equation sequence.\nError at: {segments[position + 1]}')
                        return None
                
    return equation


def prompt():   
    while True:
        result = valid_equation()

        if result is None:
            continue
        
        return result


def execution():
    equation = prompt()

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
    
    def parentheses_check(equation):
        if equation.count('(') >= 1:
            if equation.count(')') != equation.count('('):
                print('Invalid equation sequence.\nError at: (N/A)')
                return None
            
            else:
                stack = []
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

                while len(stack) > 1:
                    if perform_operation(stack, OPERATION_DICT['POWER_MODULO']):
                        continue
                    if perform_operation(stack, OPERATION_DICT['MULTIPLY_DIVIDE']):
                        continue
                    if perform_operation(stack, OPERATION_DICT['ADD_SUBTRACT']):
                        continue
                    break
                
                equation[start : stop + 1] = [stack[0]]
                return True
                             
        else:
            return False
            
    while True:            
        if parentheses_check(equation):
            continue
        else:
            break

    if parentheses_check(equation) is None:
        return False
    
    while len(equation) > 1:
        if perform_operation(equation, OPERATION_DICT['POWER_MODULO']):
            continue
        if perform_operation(equation, OPERATION_DICT['MULTIPLY_DIVIDE']):
            continue
        if perform_operation(equation, OPERATION_DICT['ADD_SUBTRACT']):
            continue
    result = equation[0]
    return result


def main():
    while True:
        result = execution()

        if result == 0:
            pass
        elif not result:
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
