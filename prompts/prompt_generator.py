import json
from PIL import Image
import os
import pyperclip
import numpy as np

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
    '0':      (0, 0, 0),
    '1':      (0, 0, 255),
    '2':      (255, 0, 0),
    '3':      (0, 128, 0),
    '4':      (255, 255, 0),
    '5':      (128, 128, 128),
    '6':      (255, 192, 203),
    '7':      (255, 165, 0),
    '8':      (0, 128, 128),
    '9':      (165, 42, 42),
    0:      (0, 0, 0),
    1:      (0, 0, 255),
    2:      (255, 0, 0),
    3:      (0, 128, 0),
    4:      (255, 255, 0),
    5:      (128, 128, 128),
    6:      (255, 192, 203),
    7:      (255, 165, 0),
    8:      (0, 128, 128),
    9:      (165, 42, 42),
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

    file = open(os.path.join("evaluation",puzzle_id+".json"))
    data = json.load(file)
    file.close()

    if type == "transform":
        text_file = open(os.path.join("prompts","transform_prompt.txt"))
    elif type == "constraints":
        text_file = open(os.path.join("prompts","constraint_prompt.txt"))
    elif type == "code":
        text_file = open(os.path.join("prompts","programmed_constraint_prompt.txt"))
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
        constraints_file = open(os.path.join("prompts","constraints.json"))
        text += json.load(constraints_file)[type][puzzle_id]
        constraints_file.close()
        text += text_stencil[3]
    
    return text,data['test'][0]['input']

def display(claude_grid,grid_type,is_transform,input):
    if is_transform:
        grid_lst = []
        exec("import numpy as np\n"+claude_grid+f"\ngrid_lst.append(transform(np.array({input})).tolist())")
        grid = [[str(pixel) for pixel in row] for row in grid_lst[0]]
    elif grid_type != "JSON":
        grid = [row.strip().split(' ') for row in claude_grid.strip().split('\n')]
    else:
        grid = list(eval(claude_grid))
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

def prompt_with_logs(puzzle_id):
    for type,grids in [("constraints","JSON")]:#("transform","words"),("transform","numbers"),("transform","JSON"),("constraints","words"),("constraints","numbers"),,("code","JSON")
        text,first_input = prompt(puzzle_id,type,grids)
        with open(os.path.join('prompts','generated_prompt.txt'), 'w') as prompt_file:
            prompt_file.write(text)
        input("Press enter when result is in clipboard")
        result = pyperclip.paste()
        try:
            display(result,grids,type=="transform", first_input)
        except:
            print("display failed")
        with open(os.path.join('prompts','logs','log.txt'), 'r') as logs_file:
            num = int(logs_file.read().split(' ')[-1]) + 1
        with open(os.path.join('prompts','logs','log.txt'), 'a') as logs_file:
            logs_file.write(f"\nattempt {num} start\n{puzzle_id}:{type}, {grids}\nresult:\n{result}\nend attempt {num}")
        with open(os.path.join('prompts','logs','prompt_log.txt'), 'a') as prompt_logs_file:
            prompt_logs_file.write(f"\nattempt {num} start\nprompt:\n{text}\nend attempt {num}")

def clear_logs():
    logs_file = open(os.path.join('prompts','logs','log.txt'), 'w')
    prompt_logs_file = open(os.path.join('prompts','logs','prompt_log.txt'), 'w')
    logs_file.write("0")
    prompt_logs_file.write("0")
    logs_file.close()
    prompt_logs_file.close()

clear_logs()
prompt_with_logs("16b78196")