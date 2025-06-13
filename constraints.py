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
        #the divider is a list containing a shape and a string in ['horizontal','vertical'] that states whether the divider is horizontal or vertical
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

def puzzle_71e489b6(input,output):
    
    #Definition: An irregularity is a pixel that is part of a one-colored shape of connectivity 8 containing less than 4 pixels or a pixel that doesn’t have at least 2 orthogonal neighbors that are the same color as itself, or 1 if it is adjacent to the border.
    blue_black_input_shapes = find_shapes(input,8,[COLOR_mapping['blue']])+find_shapes(input,8,[COLOR_mapping['black']])
    irregularities = []
    for input_shape in blue_black_input_shapes:
        pixels = 0
        for row in input_shape.grid:
            for pixel in row:
                if pixel != -1:
                    pixels += 1
        if pixels < 4:
            for i in range(len(input_shape.grid)):
                for k in range(len(input_shape.grid[0])):
                    if input_shape.grid[i][k] != -1:
                        irregularities.append([i,k])
    padded_input = [[input[i][k] if (i in range(len(input)) and k in range(len(input[0]))) else -1 for k in range(-1,len(input[0])+1)] for i in range(-1,len(input)+1)]
    for i in range(len(input)):
        for k in range(len(input[0])):
            if [i,k] not in irregularities:
                same_neighbors = 0
                for neighbor in [[0,1],[1,0],[0,-1],[-1,0]]:
                    if padded_input[i+neighbor[0]+1][k+neighbor[1]+1] == input[i][k]:
                        same_neighbors += 1
                if same_neighbors < 2-(i in [0,len(input)-1] or k in [0,len(input[0])-1]):
                    irregularities.append([i,k])

    constraints = []

    #Constraint: The output is of the same dimensions as the input.
    constraints.append(len(input)==len(output) and len(input[0])==len(output[0]))

    #Constraint: A pixel is orange in the output if and only if is is orthogonally or diagonally adjacent to a black irregularity in the input and it is not a black irregularity in the input.
    is_correct = True
    for i in range(len(input_shape.grid)):
        for k in range(len(input_shape.grid[0])):
            if (output[i][k] == COLOR_mapping['orange']) != (True in [[i+neighbor[0],k+neighbor[1]] in irregularities and input[i+neighbor[0]][k+neighbor[1]] == COLOR_mapping['black'] for neighbor in [[0,1],[1,0],[0,-1],[-1,0],[1,1],[-1,1],[1,-1],[-1,-1]]] and not([i,k] in irregularities and input[i][k] == COLOR_mapping['black'])):
                is_correct = False
    constraints.append(is_correct)

    #Constraint: Unless it is orange in the output, each pixel that is a blue irregularity in the input is black in the output.
    is_correct = True
    for i in range(len(input_shape.grid)):
        for k in range(len(input_shape.grid[0])):
            if output[i][k] != COLOR_mapping['orange']:
                if (input[i][k]==COLOR_mapping['blue'] and [i,k] in irregularities) and not (output[i][k]==COLOR_mapping['black']):
                    is_correct = False
    constraints.append(is_correct)

    #Constraint: Unless it is orange or it is a blue irregularity in the input, each pixel in the output is of the same color as in the input.
    is_correct = True
    for i in range(len(input_shape.grid)):
        for k in range(len(input_shape.grid[0])):
            if not(output[i][k] == COLOR_mapping['orange'] or (input[i][k]==COLOR_mapping['blue'] and [i,k] in irregularities)):
                if input[i][k] != output[i][k]:
                    is_correct = False
    constraints.append(is_correct)

    return False not in constraints

def puzzle_78332cb0(input,output):

    constraints = []

    #Constraint: Each shape of connectivity 4 and of non-pink colors in the input is translationally equal to a shape of connectivity 4 and of non-pink colors in the output.
    input_shapes = find_shapes(input,4,[color for color in COLORS if color != COLOR_mapping['pink']])
    output_shapes = find_shapes(output,4,[color for color in COLORS if color != COLOR_mapping['pink']])
    constraints.append(False not in [True in [input_shape.translationally_equals(output_shape) for output_shape in output_shapes] for input_shape in input_shapes])

    #Constraint: The number of shapes of connectivity 4 and of non-pink colors is the same in the input and the output.
    constraints.append(len(input_shapes)==len(output_shapes))

    #Constraint: In the output, each pink pixel in the output is orthogonally adjacent to exactly two non-pink pixels: either they are both of the color of the background or neither of them is.
    _,background_color = find_background(output)
    padded_output = [[output[i][k] if (i in range(len(output)) and k in range(len(output[0]))) else -1 for k in range(-1,len(output[0])+1)]for i in range(-1,len(output)+1)]
    is_correct = True
    for i in range(len(output)):
        for k in range(len(output[0])):
            if output[i][k] == COLOR_mapping['pink']:
                neighbors = [padded_output[i+neighbor[0]+1][k+neighbor[1]+1] for neighbor in [[0,1],[1,0],[0,-1],[-1,0]]]
                if not(neighbors.count(COLOR_mapping['pink']) + neighbors.count(-1) == 2 and (neighbors.count(background_color) == 2 or neighbors.count(background_color) == 0)):
                    is_correct = False
    constraints.append(is_correct)

    #Constraint: In the output, in each pink shape of connectivity 4, there is exactly one pixel that is orthogonally adjacent to exactly two non-pink pixels that both aren’t of the color of the background.
    pink_shapes = find_shapes(output,4,[COLOR_mapping['pink']])
    is_correct = True
    for pink_shape in pink_shapes:
        neighbors = []
        for i in range(len(output)):
            for k in range(len(output[0])):
                if pink_shape.grid[i][k] == COLOR_mapping['pink']:
                    neighbors.append([padded_output[i+neighbor[0]+1][k+neighbor[1]+1] for neighbor in [[0,1],[1,0],[0,-1],[-1,0]]].count(background_color))
        if neighbors.count(0) != 1:
            is_correct = False
    constraints.append(is_correct)

    return False not in constraints

def puzzle_7b5033c1(input,output):

    constraints = []

    #Constraint: The dimensions of the output are (1, number of non-background pixels in the input).
    background,background_color = find_background(input)
    num_pixels = 0
    for row in background:
        for pixel in row:
            if pixel == -1:
                num_pixels += 1
    constraints.append(len(output)==num_pixels and len(output[0])==1)

    #Constraint: A pixel in the input and a pixel in the output that are both in the shape of non-background colours and of connectivity 4 and that have the same distance this shape from the highest non-background pixel that only has one non-background neighbor are of the same color.
    is_correct = True
    input_shape = find_shapes(input,4,[color for color in COLORS if color != background_color])[0]
    output_shape = find_shapes(output,4,[color for color in COLORS if color != background_color])[0]
    padded_input_shape = [[input_shape.grid[i][k] if (i in range(len(input_shape.grid)) and k in range(len(input_shape.grid[0]))) else -1 for k in range(-1,len(input_shape.grid[0])+1)]for i in range(-1,len(input_shape.grid)+1)]
    padded_output_shape = [[output_shape.grid[i][k] if (i in range(len(output_shape.grid)) and k in range(len(output_shape.grid[0]))) else -1 for k in range(-1,len(output_shape.grid[0])+1)]for i in range(-1,len(output_shape.grid)+1)]
    input_pixels_one_neighbor = []
    output_pixels_one_neighbor = []
    for i in range(len(input)):
        for k in range(len(input[0])):
            if input_shape.grid[i][k] != -1:
                if [padded_input_shape[i+neighbor[0]+1][k+neighbor[1]+1] != -1 for neighbor in [[0,1],[1,0],[0,-1],[-1,0]]].count(True) == 1:
                    input_pixels_one_neighbor.append([i,k])
    for i in range(len(output)):
        for k in range(len(output[0])):
            if output_shape.grid[i][k] != -1:
                if [padded_output_shape[i+neighbor[0]+1][k+neighbor[1]+1] != -1 for neighbor in [[0,1],[1,0],[0,-1],[-1,0]]].count(True) == 1:
                    output_pixels_one_neighbor.append([i,k])
    if len(output_pixels_one_neighbor)>0:
        highest_input_pixel = [point for point in input_pixels_one_neighbor if min([point_[0] for point_ in input_pixels_one_neighbor])==point[0]][0]
        highest_output_pixel = [point for point in output_pixels_one_neighbor if min([point_[0] for point_ in output_pixels_one_neighbor])==point[0]][0]
        input_pixel_distance = []
        output_pixel_distance = []
        for i in range(len(input)):
            for k in range(len(input[0])):
                if input_shape.grid[i][k] != -1:
                    input_pixel_distance.append([input_shape.grid[i][k],input_shape.distance([i,k],highest_input_pixel)])
        for i in range(len(output)):
            for k in range(len(output[0])):
                if output_shape.grid[i][k] != -1:
                    output_pixel_distance.append([output_shape.grid[i][k],output_shape.distance([i,k],highest_output_pixel)])
        constraints.append(set(frozenset(sublist) for sublist in input_pixel_distance)==set(frozenset(sublist) for sublist in output_pixel_distance))
        for sublist in input_pixel_distance:
            if sublist not in output_pixel_distance:
                is_correct = False
        constraints.append(is_correct and len(input_pixel_distance)==len(output_pixel_distance))
    else:
        constraints.append(False)

    return False not in constraints

# print(test_constraints(puzzle_16b78196,"16b78196",0.001,10000)) returned True
# print(test_constraints(puzzle_6e453dd6,"6e453dd6",0.001,10000)) returned True
# print(test_constraints(puzzle_71e489b6,"71e489b6",0.004,10000)) returned True
# print(test_constraints(puzzle_78332cb0,"78332cb0",0.004,10000)) returned True
# print(test_constraints(puzzle_7b5033c1,"7b5033c1",0.050,10000)) returned True