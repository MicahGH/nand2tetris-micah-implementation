"""Main function for the VM translator."""

from pathlib import Path

from fire import Fire

from classes.code_writer import CodeWriter
from classes.parser import Parser
from utils import get_vm_files_to_process


def main(raw_input_vm_path: str) -> None:
    """Call the main function for the VM translator.

    Args:
    ----
    raw_input_vm_path (str): The path to the VM file / folder that requires translation.

    Returns:
    -------
    None

    Outputs
    -------
    An ".asm" file in the same path as the VM file / folder.

    """
    input_vm_path = Path(raw_input_vm_path)
    output_asm_file_path = Path(str(input_vm_path.parent) + "\\" + input_vm_path.stem + ".asm")
    vm_files_to_process = get_vm_files_to_process(input_vm_path)

    all_translated_lines = []
    for vm_file_to_process in vm_files_to_process:
        vm_parser = Parser(input_vm_file_path=vm_file_to_process)
        translated_lines = vm_parser.parse_file()
        all_translated_lines.extend(translated_lines)
    code_writer = CodeWriter(output_asm_file_path, all_translated_lines)
    code_writer.write_file()


if __name__ == "__main__":
    Fire(main)
