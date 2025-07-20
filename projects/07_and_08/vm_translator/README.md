## Project Information
This project implements the Hack VM language to Hack assembly language described in the Project 7 of Nand2Tetris Part 2.

I decided to write it in Python as, at the time of writing, it is the programming language I am most familiar with.

I am very happy with the implementation as I think it is easy to understand, easy to extend and well structured.

However, there are some DRY violations in the `translate_to_asm()` functions of the command models. I did it this way because it is much easier to debug the assembly code when you have all the code on the screen instead of importing certain parts from parent models.

## Usage
First, make sure you have the package "poetry" installed on your machine: https://github.com/python-poetry/poetry.

Next, execute `cd nand2tetris\projects\07\vm_translator`.

Then, execute these commands to install the virtual environment, the dependencies and activate it.

```
poetry install
poetry shell
```

Finally, execute:
```
python main.py {full_path_to_vm_file}
```

If successful, it will output a translated `.asm` file to the same path as the `.vm` file.