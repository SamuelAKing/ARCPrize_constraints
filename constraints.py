from definitions import *

def puzzle_16b78196(input,output):

    #Definition: All shapes are considered to consist of only one colour (not black) and to be of connectivity 4.
    input_shapes = []
    output_shapes = []
    for color in COLORS:
        if color != COLOR_mapping['black']:
            [input_shapes.append(shape) for shape in find_shapes(input,4,[color])]
            [output_shapes.append(shape) for shape in find_shapes(output,4,[color])]

    #Definition: The divider is the shape that contains a full column or a full row. If it contains a full row, it is horizontal, and if it contains a full column, it is vertical.
    def divider(shapes):
        #the divider is a list containing a shape and a string from ['horizontal','vertical'] that states whether the divider is horizontal or vertical
        for shape in shapes:
            if True in [-1 not in row for row in shape.grid]:
                return [shape,'horizontal']
            if True in [-1 not in row for row in shape.rotate(1).grid]:
                return [shape,'vertical']
        return [shapes[0],None]
    input_divider = divider(input_shapes)
    output_divider = divider(output_shapes)
    
    constraints = []

    #Constraint: The output is of the same dimensions as the input.
    constraints.append(len(input)==len(output) and len(input[0])==len(output[0]))

    #Constraint: The input and output dividers are exactly equal.
    constraints.append(input_divider[0].equals(output_divider[0]))
        
    #Constraint: Each shape in the input is translationally equal to a shape in the output.
    constraints.append(False not in [True in [input_shape.translationally_equals(output_shape) for output_shape in output_shapes] for input_shape in input_shapes])
    
    #Constraint: There is the same number of shapes in the input and in the output.
    constraints.append(len(input_shapes)==len(output_shapes))
    
    #Used for the following two constraints
    def num_partitions(lst, splitter):
        count = 0
        segment = False
        for item in lst:
            if item == splitter:
                if segment:
                    count += 1
                segment = False
            else:
                segment = True
        if segment:
            count += 1
        return count

    #Constraint: In the output, if the divider is vertical, in all rows, there are no black pixels between two non-black pixels.
    if output_divider[1] == 'vertical':
        constraints.append(False not in [num_partitions(row,0)<=1 for row in output])
    else:
        constraints.append(True)

    #Constraint: In the output, if the divider is horizontal, in all columns, there are no black pixels between two non-black pixels.
    if output_divider[1] == 'horizontal':
        constraints.append(False not in [num_partitions(column,0)<=1 for column in [[output[k][i] for k in range(len(output))]for i in range(len(output[0]))]])
    else:
        constraints.append(True)

    return False not in constraints

def puzzle_6e453dd6(input,output):
    constraints = []

    #Constraint: The output is of the same dimensions as the input.
    constraints.append(len(input)==len(output) and len(input[0])==len(output[0]))

    #Constraint: All grey pixels in the input are grey in the output
    constraints.append(True not in [True in [input[i][k] == COLOR_mapping['gray'] and output[i][k] != COLOR_mapping['gray'] for k in range(len(input[0]))] for i in range(len(input))])

    #Constraint: Each black shape of connectivity 4 in the output is translationally equal to a black shape in the input, occupying exactly the same rows, and it has at least one pixel directly to the left of a grey pixel.
    input_black_shapes = find_shapes(input,4,[COLOR_mapping['black']])
    output_black_shapes = find_shapes(output,4,[COLOR_mapping['black']])

    tests = []
    for output_black_shape in output_black_shapes:
        is_correct = False
        for input_black_shape in input_black_shapes:
            if output_black_shape.translationally_equals(input_black_shape) and [True in [pixel!=-1 for pixel in row] for row in output_black_shape.grid] == [True in [pixel!=-1 for pixel in row] for row in input_black_shape.grid]:
                for i in range(len(input)):
                    for k in range(len(input[0])):
                        if output_black_shape.grid[i][k]==COLOR_mapping['black'] and output[i][k+1]==COLOR_mapping['gray']:
                            is_correct = True
        tests.append(is_correct)
    constraints.append(False not in tests)

    #Constraint: The input and output have the same number of black shapes of connectivity 4.
    constraints.append(len(input_black_shapes)==len(output_black_shapes))

    #Constraint: In the output, each pixel is red if and only if it is to the left of a grey pixel and it is in the same row as a pixel that has a grey pixel two spaces to the right and that is in a pink shape of connectivity 4 that is orthogonally adjacent to a black shape of connectivity 4 and whose pixels are all orthogonally adjacent to four pixels that are either black or pink.
    output_pink_shapes = find_shapes(output,4,[COLOR_mapping['pink']])
    pink_shapes_fitting_criteria = []
    padded_output = [[output[i][k] if (i in range(len(output)) and k in range(len(output[0]))) else -1 for k in range(-1,len(output[0])+1)]for i in range(-1,len(output)+1)]
    for output_black_shape in output_black_shapes:
        adjacent_pink_shapes = []
        for pink_shape in output_pink_shapes:
            for i in range(1,len(input)-1):
                for k in range(1,len(input[0])-1):
                    if pink_shape not in adjacent_pink_shapes:
                        if pink_shape.grid[i][k] != -1:
                            if True in [output_black_shape.grid[i+neighbor[0]][k+neighbor[1]] != -1 for neighbor in [[0,1],[1,0],[0,-1],[-1,0]]]:
                               adjacent_pink_shapes.append(pink_shape)
        for adjacent_pink_shape in adjacent_pink_shapes:
            keep_shape = True
            for i in range(len(input)):
                for k in range(len(input[0])):
                    if keep_shape:
                        if adjacent_pink_shape.grid[i][k] != -1:
                            if False in [padded_output[i+neighbor[0]+1][k+neighbor[1]+1] in [COLOR_mapping['black'],COLOR_mapping['pink']] for neighbor in [[0,1],[1,0],[0,-1],[-1,0]]]:
                                keep_shape = False
            if keep_shape:
                pink_shapes_fitting_criteria.append(adjacent_pink_shape)
    rows_with_red = []
    for pink_shape_fitting_criteria in pink_shapes_fitting_criteria:
        for row_idx in range(len(pink_shape_fitting_criteria.grid)):
            if row_idx not in rows_with_red:
                for pixel_idx in range(len(pink_shape_fitting_criteria.grid[row_idx])-2):
                    if pink_shape_fitting_criteria.grid[row_idx][pixel_idx] != -1:
                        if output[row_idx][pixel_idx+2] == COLOR_mapping['gray']:
                            rows_with_red.append(row_idx)
                            if row_idx == 0:
                                i = row_idx
                                k = pixel_idx
    tests = []
    for i in range(len(input)):
        for k in range(len(input[0])):
            tests.append((COLOR_mapping['gray'] in output[i][0:k] and i in rows_with_red) is (output[i][k] == COLOR_mapping['red']))
    constraints.append(False not in tests)

    #Constraint: In the output, each pixel is pink, unless it is grey in the input, it is red, or it is black.
    is_correct = True
    for i in range(len(input)):
        for k in range(len(input[0])):
            if input[i][k] != COLOR_mapping['gray'] and output[i][k] != COLOR_mapping['red'] and output[i][k] != COLOR_mapping['black'] and output[i][k] != COLOR_mapping['pink']:
                is_correct = False
    constraints.append(is_correct)

    return False not in constraints

# print(test_constraints(puzzle_16b78196,"16b78196",0.001,10000)) returned True
# print(test_constraints(puzzle_6e453dd6,"6e453dd6",0.001,10000)) returned True