

from models.base import BaseCommand, BaseCommandType


class FunctionCommandType(BaseCommandType):
    FUNCTION = "function"
    CALL = "call"
    RETURN = "return"


class BaseFunctionCommand(BaseCommand):
    command: FunctionCommandType  # type: ignore[reportGeneralTypeIssues]
    # Function command specifiers cannot be Enums as they are user-defined
    command_specifier: str # type: ignore[reportGeneralTypeIssues]
    command_value: int # type: ignore[reportGeneralTypeIssues]

class FunctionCommand(BaseFunctionCommand):
    pass

class CallCommand(BaseFunctionCommand):
    pass

class ReturnCommand(BaseFunctionCommand):
    # Return commands don't have a specifier or a value
    command_specifier: None # type: ignore[reportGeneralTypeIssues]
    command_value: None # type: ignore[reportGeneralTypeIssues]