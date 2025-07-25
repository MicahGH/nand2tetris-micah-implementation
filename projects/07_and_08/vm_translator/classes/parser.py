"""Parser for a '.vm' file."""

import logging

from pathlib import Path

from models.base import BaseCommand, CommandSpecifierType, CommandType
from models.mapping import COMMAND_TYPE_COMMAND_CLASS_MAP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Parser:
    def __init__(self, input_vm_file_path: str) -> None:
        """Initialise the Parser class."""
        self.input_vm_file_path = input_vm_file_path
        self.input_vm_filename = self.get_input_vm_filename()

    def get_input_vm_filename(self) -> str:
        """Get the VM filename from the input file path."""
        return Path(self.input_vm_file_path).stem

    def is_command_line(self, current_line: str) -> bool:
        """Determine if the current line has a command."""
        if current_line.startswith("//") or current_line == "":
            return False
        return True

    def get_command_class(
        self, command: CommandType, command_specifier: CommandSpecifierType | None
    ) -> type[BaseCommand]:
        """Get the command class for the command in the current line."""
        command_class = COMMAND_TYPE_COMMAND_CLASS_MAP.get(command)
        if command_class is None:
            msg = f"No class found in the command type-class map for command type: {command}"
            raise ValueError(msg)
        elif isinstance(command_class, dict):
            if not command_specifier:
                msg = "'command_specifier' must be provided if the value of the mapping is a dict."
                raise ValueError(msg)
            return command_class.get(command_specifier, command_class["default"])
        else:
            return command_class

    def get_command_type(self, command: str) -> CommandType:
        """Get the command type for the command in the current line."""
        try:
            return CommandType(command)
        except Exception:
            msg = f"No CommandType found for command type: {command}"
            raise ValueError(msg)

    def get_command_specifier_type(
        self, command_specifier: str
    ) -> CommandSpecifierType:
        """Get the command specifier type for the command specifier in the current line."""
        try:
            return CommandSpecifierType(command_specifier)
        except Exception:
            msg = f"No CommandSpecifierType found for command specifier type: {command_specifier}"
            raise ValueError(msg)

    def split_command_line(
        self, command_line: str
    ) -> tuple[str, str | None, int | None]:
        """Split the command line into its parts and return the data as a tuple."""
        command_line_parts = command_line.split(" ")
        match len(command_line_parts):
            case 1:
                command = command_line_parts[0]
                return command, None, None
            case 2:
                command, command_specifier = command_line_parts
                return command, command_specifier if command_specifier else None, None
            case 3:
                command, command_specifier, command_value = command_line_parts
                return command, command_specifier, int(command_value)
            case _:
                msg = f"Command line: {command_line} has more than 3 parts."
                raise ValueError(msg)

    def parse_file(self) -> list[str]:
        """Parse and translate the VM file."""
        translated_lines = []
        line_number = 0

        with open(self.input_vm_file_path, mode="r") as vm_file:
            logger.info("Opened VM file.")
            for raw_line in vm_file:
                current_line: str = raw_line.strip()

                if not self.is_command_line(current_line):
                    continue

                command, command_specifier, command_value = self.split_command_line(
                    current_line
                )
                command = self.get_command_type(command)
                command_specifier = None if not command_specifier else command_specifier
                if command_specifier is not None:
                    command_specifier = self.get_command_specifier_type(
                        command_specifier
                    )

                CommandClass = self.get_command_class(command, command_specifier)
                parsed_command = CommandClass(
                    command=command,
                    command_specifier=command_specifier,
                    command_value=command_value,
                    unparsed_command_line=current_line,
                    line_number=line_number,
                    input_vm_filename=self.input_vm_filename,
                )
                translated_lines.extend(
                    parsed_command.get_line_comment()
                    + parsed_command.translate_to_asm()
                    + ["\n"]
                )
                line_number += 1
        logger.info("Finished parsing VM file.")
        return translated_lines
