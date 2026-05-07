import os, io, sys
import nbformat as nbf
import mdutils
import json


def ktx_to_dict(input_file: str, keystarter='<') -> dict:
    """ parsing keyed text to a python dictionary. """
    answer = dict()

    with open(input_file, 'r+', encoding='utf-8') as f:
        lines = f.readlines()

    k, val = '', ''
    for line in lines:
        if line.startswith(keystarter):
            k = line.replace(keystarter, '').strip()
            val = ''
        else:
            val += line

        if k:
            answer.update({k: val.strip()})

    return answer


def dict_to_ktx(input_dict: dict, output_file: str, keystarter='<') -> None:
    """ Store a python dictionary to a keyed text"""
    with open(output_file, 'w+') as f:
        for k, val in input_dict.items():
            f.write(f'{keystarter} {k}\n')
            f.write(f'{val}\n\n')


def create_expected_ouputs() -> dict:
    expected_outputs = {}
    for n in range(1, 101):
        buffer = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buffer

        try:
            exec("import numpy as np\n" + QHA[f'a{n}'], globals())
        except Exception as e:
            expected_outputs[str(n)] = f"Error in a{n}: {e}"
        else:
            expected_outputs[str(n)] = buffer.getvalue().strip()
        finally:
            sys.stdout = old_stdout
        
    return expected_outputs


HEADERS = ktx_to_dict(os.path.join('source', 'headers.ktx'))
QHA = ktx_to_dict(os.path.join('source', 'exercises100.ktx'))
expected_outputs = create_expected_ouputs()

with open("expected_outputs.json", 'w') as f:
    json.dump(expected_outputs, f, indent=4) 



output_checker = """

import io, sys
import json
from IPython.core.magic import register_cell_magic

with open("expected_outputs.json", 'r') as f:
    expected_outputs = json.load(f)
@register_cell_magic
def check_output(line, cell):
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    try: 
        exec(cell, globals())
    finally:
        sys.stdout = old_stdout

    user_output = buffer.getvalue().strip()
    expected_output = expected_outputs[line.strip()]

    try:
        assert user_output == expected_output
        print(user_output)
        print("✅ Great job!")
    except AssertionError:
        print("❌ Not quite right — try again ")
        print("your output:")
        print(user_output)
        print("expected ouput: ")
        print(expected_output)
"""

def create_jupyter_notebook(destination_filename='100_Numpy_exercises.ipynb', within_solved=0):
    """ Programmatically create jupyter notebook with the questions (and hints and solutions if required)
    saved under source files """

    
    # Create cells sequence
    nb = nbf.v4.new_notebook()
    
    
    nb['cells'] = []

    # - Use Magic for check answers
    nb['cells'].append(nbf.v4.new_markdown_cell("## Magic Output Checker (RUN IT!!)"))
    nb['cells'].append(nbf.v4.new_code_cell(output_checker))

    # - Add header:
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["header"]))
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["sub_header"]))
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["jupyter_instruction"]))

    # - Add initialisation
    nb['cells'].append(nbf.v4.new_code_cell('%run initialise.py'))

    # - Add questions and empty spaces for answers
    for n in range(1, 101):
        nb['cells'].append(nbf.v4.new_markdown_cell(f'#### {n}. ' + QHA[f'q{n}']))

        # Set up the first within_solved answers
        init_code = str(QHA[f'a{n}']) if n <= within_solved else "%%check_output " + str(n) + "\n"

        nb['cells'].append(nbf.v4.new_code_cell(init_code))
            
    # Delete file if one with the same name is found
    if os.path.exists(destination_filename):
        os.remove(destination_filename)

    # Write sequence to file
    nbf.write(nb, destination_filename)


def create_jupyter_notebook_random_question(destination_filename='100_Numpy_random.ipynb'):
    """ Programmatically create jupyter notebook with the questions (and hints and solutions if required)
    saved under source files """

    # Create cells sequence
    nb = nbf.v4.new_notebook()

    nb['cells'] = []

    # - Add header:
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["header"]))
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["sub_header"]))
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["jupyter_instruction_rand"]))
    
    # - Add initialisation
    nb['cells'].append(nbf.v4.new_code_cell('%run initialise.py'))
    nb['cells'].append(nbf.v4.new_code_cell("pick()"))

    # Delete file if one with the same name is found
    if os.path.exists(destination_filename):
        os.remove(destination_filename)

    # Write sequence to file
    nbf.write(nb, destination_filename)


def create_markdown(destination_filename='100_Numpy_exercises', with_hints=False, with_solutions=False):
    # Create file name
    if with_hints:
        destination_filename += '_with_hints'
    if with_solutions:
        destination_filename += '_with_solutions'

    # Initialise file
    mdfile = mdutils.MdUtils(file_name=destination_filename)

    # Add headers
    mdfile.write(HEADERS["header"] + '\n')
    mdfile.write(HEADERS["sub_header"] + '\n')

    # Add questions (and hint or answers if required)
    for n in range(1, 101):
        mdfile.new_header(title=f"{n}. {QHA[f'q{n}']}", level=4, add_table_of_contents="n")
        if with_hints:
            mdfile.write(f"`{QHA[f'h{n}']}`")
        if with_solutions:
            mdfile.insert_code(QHA[f'a{n}'], language='python')

    # Delete file if one with the same name is found
    if os.path.exists(destination_filename):
        os.remove(destination_filename)

    # Write sequence to file
    mdfile.create_md_file()


def create_rst(destination_filename, with_ints=False, with_answers=False):
    # TODO: use rstdoc python library.
    #  also see possible integrations with https://github.com/rougier/numpy-100/pull/38
    pass


if __name__ == '__main__':
    create_jupyter_notebook()
    create_jupyter_notebook_random_question()
    create_markdown()
    create_markdown(with_hints=False, with_solutions=True)
    create_markdown(with_hints=True, with_solutions=False)
    create_markdown(with_hints=True, with_solutions=True)
