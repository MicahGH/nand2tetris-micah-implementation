"""Main function for the VM translator."""

from fire import Fire
from classes.code_writer import CodeWriter
from classes.parser import Parser


def main(input_vm_file_path: str) -> None:
    """
    Main function for the VM translator.

    Args
    ----
    input_vm_file_path (str): The full path to the VM file that requires translation.

    Returns
    -------
    None

    Outputs
    -------
    An ".asm" file in the same path as the VM file.

    """
    vm_parser = Parser(input_vm_file_path=input_vm_file_path)
    translated_lines = vm_parser.parse_file()
    output_asm_file_path = input_vm_file_path.replace(".vm", ".asm")
    code_writer = CodeWriter(output_asm_file_path, translated_lines)
    code_writer.write_file()


if __name__ == "__main__":
    Fire(main)
