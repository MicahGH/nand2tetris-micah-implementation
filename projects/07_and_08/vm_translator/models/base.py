from abc import abstractmethod
from enum import Enum

from pydantic import BaseModel


class CommandType(str, Enum):
    """Enum for the distinct VM command types."""

    # Arithmetic command types
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"
    # Memory access command types
    PUSH = "push"
    POP = "pop"


class CommandSpecifierType(str, Enum):
    CONSTANT = "constant"
    LCL = "local"
    ARG = "argument"
    THIS = "this"
    THAT = "that"
    TEMP = "temp"
    POINTER = "pointer"
    STATIC = "static"


class BaseCommand(BaseModel):
    """Abstract base class for the VM commands."""

    command: CommandType
    command_specifier: CommandSpecifierType | str | None = None
    command_value: int | None = None
    unparsed_command_line: str
    line_number: int
    input_vm_filename: str

    @abstractmethod
    def translate_to_asm(self) -> list[str]:
        """Translate the VM command into ASM code."""
        msg = "'translate_to_asm()' must be implemented in each subclass."
        raise NotImplementedError(msg)

    def get_line_comment(self) -> list[str]:
        """Get the unparsed line as a comment for debugging purposes in the '.asm' file."""
        return ["// " + self.unparsed_command_line]
