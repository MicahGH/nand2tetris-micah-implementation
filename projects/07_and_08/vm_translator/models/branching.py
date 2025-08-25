from models.base import BaseCommand, BaseCommandType


class BranchingCommandType(BaseCommandType):
    LABEL = "label"
    GOTO = "goto"
    IF_GOTO = "if-goto"


class BaseBranchingCommand(BaseCommand):
    command: BranchingCommandType  # type: ignore[reportGeneralTypeIssues]
    # Branching command specifiers cannot be Enums as they are user-defined
    command_specifier: str  # type: ignore[reportGeneralTypeIssues]
    # This is never needed in branching commands
    # so it is set to always be None
    command_value: None  # type: ignore[reportGeneralTypeIssues]


class LabelCommand(BaseBranchingCommand):
    def translate_to_asm(self) -> list[str]:
        create_label = f"""
        ({self.command_specifier})
        """
        return [create_label]


class GoToCommand(BaseBranchingCommand):
    def translate_to_asm(self) -> list[str]:
        address_label = f"""
        @{self.command_specifier}
        """
        create_goto = """
        0;JMP
        """
        return [address_label + create_goto]


class IfGoToCommand(BaseBranchingCommand):
    def translate_to_asm(self) -> list[str]:
        decrement_pointer_addr = """
        @SP
        M=M-1
        """
        get_value_in_pointer = """
        A=M
        D=M
        """
        address_label = f"""
        @{self.command_specifier}
        """
        create_if_goto = """
        D;JNE
        """
        return [
            decrement_pointer_addr + get_value_in_pointer + address_label + create_if_goto,
        ]
