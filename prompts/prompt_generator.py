import json
from PIL import Image
import os

COLOR_mapping = {
    'black': 0, 'blue': 1, 'red': 2, 'green': 3, 'yellow': 4,
    'gray': 5, 'pink': 6, 'orange': 7, 'teal': 8, 'brown': 9,
}

COLORS = [
    'black', 'blue', 'red', 'green', 'yellow',
    'gray', 'pink', 'orange', 'teal', 'brown'
]

color_map = {
    'black':  (0, 0, 0),
    'blue':   (0, 0, 255),
    'red':    (255, 0, 0),
    'green':  (0, 128, 0),
    'yellow': (255, 255, 0),
    'gray':   (128, 128, 128),
    'pink':   (255, 192, 203),
    'orange': (255, 165, 0),
    'teal':   (0, 128, 128),
    'brown':  (165, 42, 42),
}

def print_shape(grid,format):
    output = ''
    if format == "words":
        for row in grid:
            for pixel in row:
                output += COLORS[pixel] + ' '
            output += '\n'
    if format == "numbers":
        for row in grid:
            for pixel in row:
                output += str(pixel) + ' '
            output += '\n'
    return output

def prompt(puzzle_id,type,grids):

    file = open("evaluation/"+puzzle_id+".json")
    data = json.load(file)
    file.close()

    if type == "transform":
        text_file = open("prompts/transform_prompt.txt")
    elif type == "constraints":
        text_file = open("prompts/constraint_prompt.txt")
    elif type == "code":
        text_file = open("prompts/programmed_constraint_prompt.txt")
    text_stencil = text_file.read().split("@SPLIT_POINT")

    text = text_stencil[0]
    if grids in ["words", "numbers"]:
        if grids == "words":
            text += "The grids are represented as rows of colors (as words) separated by new lines. Newlines separate rows.\nHere are the input and output grids for the task:\n"
        elif grids == "numbers":
            text += "The grids are represented as rows of colors represented by the integers 0-9 separated by new lines. Newlines separate rows. You cannot perform arithmetic on these integers.\nHere are the input and output grids for the task:\n"
        for idx,case in enumerate(data['train']):
            text += 'Pair ' + str(idx) + '\n'
            input = case['input']
            output = case['output']
            text += "Input:\n"+print_shape(input,grids) +"Output:\n"+ print_shape(output,grids)
        text += text_stencil[1]
        for idx,case in enumerate(data['test']):
            input = case['input']
            output = case['output']
            text += "Input:\n"+print_shape(input,grids)
        text += text_stencil[2]
    elif grids == "JSON":
        text += "The grids are represented as a JSON object containing 2D arrays of colors represented by the integers 0-9. You cannot perform arithmetic on these integers.\nHere are the input and output grids for the task:"
        new_dict = data.copy()
        for idx in range(len(new_dict['test'])):
            new_dict['test'][idx]['output'] = ""
        text += str(new_dict)
        text += text_stencil[2]
    if type != "transform":
        constraints_file = open("prompts/constraints.json")
        text += json.load(constraints_file)[type][puzzle_id]
        constraints_file.close()
        text += text_stencil[3]
    
    with open('prompts/generated_prompt.txt', 'w') as file:
        file.write(text)

claude_grid = """
black black black black black black black black black green green green green green green green black black black black black black black black black black black black black black 
black black black black black black black black black green green green green green green green black black black black black black black black black black black black black black 
black black black black black black black black black black green green green green green black black black black black black black black black black black black black black black 
black black black black black black black black black black black green green green green green black teal teal teal teal black black black black black black black black black 
black black black yellow yellow yellow yellow black black green green green green green green green black teal teal teal teal black black black black black black black black black 
black black black yellow black black black black black green green green green green green green black teal teal teal teal black black black black black black black black black 
black black yellow yellow yellow black black black black black green green green green green green black teal teal teal teal black black black black black black black black black 
black black black yellow yellow yellow yellow black black green green green green green green green black black black black black black black black black black black black black black 
black black black black black black black black black green green green green green green green black black black black black black black black black black black black black black 
black black black black black black black black black green green green green green green green black black black black black black black black black black black black black black 
black black black black black black black black black green green green green green green green black black black black black black black black black black black black black black 
black black black black black black black black black green green green green green green black black black black black black black black black black black black black black black 
black black black black black black black black black green green green green green green black black black black black black black black black black black black black black black 
pink black black black black black black black black black green green green green green black black black black black black black black black black black black black black black 
pink pink black black black black black black black black green green green green green green black black black black black black black black black black black black black black 
pink pink pink black black black black black black green green green green green green green black black black black black black black black black black black black black black 
pink pink pink pink black black black black black green green green green green green green black red red red red black black black black black black black black black 
black black black black black black black black black green green green green green green black black red red red red black black black black black black black black black 
black black black black black black black black black black green green green green green black black red red red red black black black black black black black black black 
black black black black black black black black black black black green green green green green black red red red red black black black black black black black black black 
black black black black black black black black black black green green green green green green black black black black black black black black black black black black black black 
black black black black black black black black black green green green green green green green black black black black black black black black black black black black black black 
black black black black black black black black black green green green green green green green black black black black black black black black black black black black black black 
black black black black black black black black black green green green green green green green black black black black black black black black black black black black black black 
black black black black black black black black black black green green green green green green black blue blue blue black black black black black black black black black black 
black black black black black black black black black green green green green green green green black blue blue blue black black black black black black black black black black 
black black black black black black black black black green green green green green green green black blue blue blue black black black black black black black black black black 
black black black black black black black black black green green green green green green black black blue black black black black black black black black black black black black 
black black black black black black black black black green green green green green green green black black black black black black black black black black black black black black 
black black black black black black black black black green green green green green green green black black black black black black black black black black black black black black
"""

def display(claude_grid):
    grid = [row.strip().split(' ') for row in claude_grid.strip().split('\n')]
    expected_size_1 = len(grid)
    expected_size_2 = len(grid[0])
    cell_size = 20  # pixels per cell
    img = Image.new("RGB", (expected_size_1 * cell_size, expected_size_2 * cell_size))

    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            rgb = color_map[color]
            for dy in range(cell_size):
                for dx in range(cell_size):
                    img.putpixel((x * cell_size + dx, y * cell_size + dy), rgb)

    img.show()

# display(claude_grid)
prompt("16b78196","code","numbers")