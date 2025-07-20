import logging
from typing import Self

from pydantic import model_validator
from models.base import BaseCommand, CommandSpecifierType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseMemoryAccessCommand(BaseCommand):
    command_specifier: CommandSpecifierType  # type: ignore[reportGeneralTypeIssues]
    command_value: int  # type: ignore[reportGeneralTypeIssues]

    TEMP_SEGMENT_RAM_LOCATION: int = 5


class BasePointerCommand(BaseMemoryAccessCommand):
    POINTER_COMMAND_VALUE_COMMAND_SPECIFIER_MAP: dict[int, CommandSpecifierType] = {
        0: CommandSpecifierType.THIS,
        1: CommandSpecifierType.THAT,
    }

    @model_validator(mode="after")
    def check_pointer_value(self) -> Self:
        if (
            self.command_value
            not in self.POINTER_COMMAND_VALUE_COMMAND_SPECIFIER_MAP.keys()
        ):
            msg = f"Invalid push pointer command value: {self.command_value}. "
            msg = f"Valid values: {self.POINTER_COMMAND_VALUE_COMMAND_SPECIFIER_MAP.keys()}"
            raise ValueError(msg)
        return self


class PushCommand(BaseMemoryAccessCommand):
    def translate_to_asm(self) -> list[str]:
        select_value = f"""
        @{self.command_value}
        D=A
        """
        get_value_from_segment = f"""
        @{self.command_specifier.name}
        A=D+M
        D=M
        """
        get_current_pointer_addr = """
        @SP
        A=M
        """
        set_selected_pointer_addr = """
        M=D
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [
            select_value
            + get_value_from_segment
            + get_current_pointer_addr
            + set_selected_pointer_addr
            + increment_pointer_addr
        ]


class PushTempCommand(BaseMemoryAccessCommand):
    def translate_to_asm(self) -> list[str]:
        select_value = f"""
        @{self.command_value}
        D=A
        """
        get_value_from_segment = f"""
        @{self.TEMP_SEGMENT_RAM_LOCATION}
        A=D+M
        D=M
        """
        get_current_pointer_addr = """
        @SP
        A=M
        """
        set_selected_pointer_addr = """
        M=D
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [
            select_value
            + get_value_from_segment
            + get_current_pointer_addr
            + set_selected_pointer_addr
            + increment_pointer_addr
        ]

class PushConstantCommand(BaseMemoryAccessCommand):
    def translate_to_asm(self) -> list[str]:
        select_value = f"""
        @{self.command_value}
        D=A
        """
        get_current_pointer_addr = """
        @SP
        A=M
        """
        set_selected_pointer_addr = """
        M=D
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [
            select_value
            + get_current_pointer_addr
            + set_selected_pointer_addr
            + increment_pointer_addr
        ]

class PushPointerCommand(BasePointerCommand):
    def translate_to_asm(self) -> list[str]:
        segment = self.POINTER_COMMAND_VALUE_COMMAND_SPECIFIER_MAP[self.command_value]
        get_value_from_segment = f"""
        @{segment.name}
        D=M
        """
        get_current_pointer_addr = """
        @SP
        A=M
        """
        set_selected_pointer_addr = """
        M=D
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [
            get_value_from_segment
            + get_current_pointer_addr
            + set_selected_pointer_addr
            + increment_pointer_addr
        ]
    
class PushStaticCommand(BaseMemoryAccessCommand):
    def translate_to_asm(self) -> list[str]:
        get_value_from_segment = f"""
        @{self.input_vm_filename+"."+str(self.command_value)}
        D=M
        """
        get_current_pointer_addr = """
        @SP
        A=M
        """
        set_selected_pointer_addr = """
        M=D
        """
        increment_pointer_addr = """
        @SP
        M=M+1
        """
        return [
            get_value_from_segment
            + get_current_pointer_addr
            + set_selected_pointer_addr
            + increment_pointer_addr
        ]


class PopCommand(BaseMemoryAccessCommand):
    @model_validator(mode="after")
    def check_no_constant_pop(self) -> Self:
        if self.command_specifier == CommandSpecifierType.CONSTANT:
            msg = "Popping into a constant is not permitted."
            raise ValueError(msg)
        return self

    def translate_to_asm(self) -> list[str]:
        select_value = f"""
        @{self.command_value}
        D=A
        """
        get_ram_location = f"""
        @{self.command_specifier.name}
        D=M+D
        """
        save_ram_location = f"""
        @temp_{self.line_number}
        M=D
        """
        decrement_pointer_addr = """
        @SP
        M=M-1
        """
        get_value_in_pointer = """
        A=M
        D=M
        """
        pop_value_to_segment = f"""
        @temp_{self.line_number}
        A=M
        M=D
        """
        return [
            select_value
            + get_ram_location
            + save_ram_location
            + decrement_pointer_addr
            + get_value_in_pointer
            + pop_value_to_segment
        ]

class PopTempCommand(BaseMemoryAccessCommand):
    def translate_to_asm(self) -> list[str]:
        select_value = f"""
        @{self.command_value}
        D=A
        """
        get_ram_location = f"""
        @{self.TEMP_SEGMENT_RAM_LOCATION}
        M=A
        D=M+D
        """
        save_ram_location = f"""
        @temp_{self.line_number}
        M=D
        """
        decrement_pointer_addr = """
        @SP
        M=M-1
        """
        get_value_in_pointer = """
        A=M
        D=M
        """
        pop_value_to_segment = f"""
        @temp_{self.line_number}
        A=M
        M=D
        """
        return [
            select_value
            + get_ram_location
            + save_ram_location
            + decrement_pointer_addr
            + get_value_in_pointer
            + pop_value_to_segment
        ]

class PopPointerCommand(BasePointerCommand):
    def translate_to_asm(self) -> list[str]:
        segment = self.POINTER_COMMAND_VALUE_COMMAND_SPECIFIER_MAP[self.command_value]
        get_ram_location = f"""
        @{segment.name}
        D=A
        """
        save_ram_location = f"""
        @temp_{self.line_number}
        M=D
        """
        decrement_pointer_addr = """
        @SP
        M=M-1
        """
        get_value_in_pointer = """
        A=M
        D=M
        """
        pop_value_to_segment = f"""
        @temp_{self.line_number}
        A=M
        M=D
        """
        return [
            get_ram_location
            + save_ram_location
            + decrement_pointer_addr
            + get_value_in_pointer
            + pop_value_to_segment
        ]

class PopStaticCommand(BaseMemoryAccessCommand):
    def translate_to_asm(self) -> list[str]:
        get_ram_location = f"""
        @{self.input_vm_filename+"."+str(self.command_value)}
        M=A
        D=M
        """
        save_ram_location = f"""
        @temp_{self.line_number}
        M=D
        """
        decrement_pointer_addr = """
        @SP
        M=M-1
        """
        get_value_in_pointer = """
        A=M
        D=M
        """
        pop_value_to_segment = f"""
        @temp_{self.line_number}
        A=M
        M=D
        """
        return [
            get_ram_location
            + save_ram_location
            + decrement_pointer_addr
            + get_value_in_pointer
            + pop_value_to_segment
        ]