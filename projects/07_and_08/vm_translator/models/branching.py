from models.base import BaseCommand, BaseCommandType


class BranchingCommandType(BaseCommandType):
    LABEL = "label"
    GOTO = "goto"
    IF_GOTO = "if-goto"


class BaseBranchingCommand(BaseCommand):
    command: BranchingCommandType  # type: ignore[reportGeneralTypeIssues]
    # This is never needed in branching commands
    # so it is set to always be None
    command_value: None  # type: ignore[reportGeneralTypeIssues]


class LabelCommand(BaseBranchingCommand):
    def translate_to_asm(self):
        create_label = f"({self.command_specifier})"
        return [create_label]


class GotoCommand(BaseBranchingCommand):
    def translate_to_asm(self):
        address_label = f"@{self.command_specifier}"
        create_goto = "0;JMP"
        return [address_label + create_goto]
