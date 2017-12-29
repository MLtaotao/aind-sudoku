assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    return [a+b for a in A for b in B]
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
normal_unitlist = row_units + column_units + square_units
normal_units = dict((s, [u for u in normal_unitlist if s in u]) for s in boxes)
normal_peers = dict((s, set(sum(normal_units[s],[]))-set([s])) for s in boxes)

# add diagonal unit to the unitlist, units and peers
diagonal1 = []
diagonal2 = []
for i in range(len(rows)):
    diagonal1.append(rows[i] + cols[i])
    diagonal2.append(rows[i] + cols[-i-1])
diagonal_unitlist = normal_unitlist + [diagonal1] + [diagonal2]
diagonal_units = dict((s, [u for u in diagonal_unitlist if s in u]) for s in boxes)
diagonal_peers = dict((s, set(sum(diagonal_units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    unsolved_value = [box for box in boxes if len(values[box])>1]

    for box in unsolved_value:
        for unit in normal_units[box]:
            twins = []
            for box1 in unit:
                if box1 in unsolved_value and values[box1] == values[box]:
                    twins.append(box1)
            if len(twins) > 1:
                if len(twins) == len(values[twins[0]]):
                    #print(twins)
                    for digit in values[twins[0]]:
                        for box2 in unit:
                            if box2 not in twins and len(values[box2]) > 1:
                                #print(values[box2], digit , twins)
                                values = assign_value(values, box2, values[box2].replace(digit, ''))
    return values

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    all_digits = '123456789'

    for c in grid:
        if c == '.':
            chars.append(all_digits)
        elif c in all_digits:
            chars.append(c)

    return dict(zip(boxes,chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    assert values
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    '''
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
    Keys: The boxes, e.g., 'A1'
    Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    '''
    solved_values = [box for box in boxes if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in diagonal_peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.

    """
    for unit in diagonal_unitlist:
        for digit in '123456789':
            dplace = [box for box in unit if digit in values[box]]
            if len(dplace) == 1:
                values = assign_value(values, dplace[0], digit)
    return values

def reduce_puzzle(values):
    '''
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.

    '''

    stalled = False

    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)

        values = only_choice(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."

    values = reduce_puzzle(values)

    if values is False:
        return False

    if all(len(values[box]) == 1 for box in values):
        return values

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = search(grid_values(grid))

    if values is False:
        print("No solution exists.")
        return
    else:
        return values



if __name__ == '__main__':
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
