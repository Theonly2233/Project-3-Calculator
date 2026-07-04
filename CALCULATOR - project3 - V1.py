# ==========================================
# PROJECT 3 - CALCULATOR
# ==========================================
# Version 1
# - Initial version of the project.
# ==========================================

# ==========================================
# CONSTANTS
# ==========================================
OPERATION_LIST = ['+', '-', '*', '/']


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
    if not value in OPERATION_LIST:
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

    result = equation[0]

    for position in range(1, len(equation), 2):
        current_position = equation[position]
        next_position = equation[position + 1]
    
        if current_position == '+':
            result = result + next_position
        elif current_position == '-':
            result = result - next_position
        elif current_position == '*':
            result = result * next_position
        elif current_position == '/':
            result = result / next_position
        
    return result


def main():
    print(execution())

    
# ==========================================
# MAIN PROGRAM
# ==========================================
main()
