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

def print_shape(grid):
    output = ''
    for row in grid:
        for pixel in row:
            output += COLORS[pixel] + ' '
        output += '\n'
    return output

def prompt(puzzle_id,type):

    file = open("evaluation/"+puzzle_id+".json")
    data = json.load(file)
    file.close()

    if type == "transform":
        text_file = open("prompts/transform_prompt.txt")
    if type == "constraints":
        text_file = open("prompts/constraint_prompt.txt")
    if type == "code":
        text_file = open("prompts/programmed_constraint_prompt.txt")
    text_stencil = text_file.read().split("@SPLIT_POINT")

    text = text_stencil[0]
    for idx,case in enumerate(data['train']):
        text += 'Pair ' + str(idx) + '\n'
        input = case['input']
        output = case['output']
        text += "Input:\n"+print_shape(input) +"Output:\n"+ print_shape(output)
    text += text_stencil[1]
    for idx,case in enumerate(data['test']):
        input = case['input']
        output = case['output']
        text += "Input:\n"+print_shape(input)
    text += text_stencil[2]
    if type != "transform":
        constraints_file = open("prompts/constraints.json")
        text += json.load(constraints_file)[type][puzzle_id]
        constraints_file.close()
        text += text_stencil[3]

    print(text)

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

display(claude_grid)
# prompt("16b78196","code")